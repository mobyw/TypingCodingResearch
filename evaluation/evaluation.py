#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import re
import argparse
import numpy as np
from io import StringIO
from io import open
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from xpinyin import Pinyin

parser = argparse.ArgumentParser(description='Evaluate a PDF file.')
parser.add_argument('input_filename', metavar='input_file', type=str,
                    help='the name of the file to process')
args = parser.parse_args()


def read_pdf(pdf):
    # resource manager
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()

    # device
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    process_pdf(rsrcmgr, device, pdf)
    device.close()
    content = retstr.getvalue()
    retstr.close()

    # 获取文本并提取汉字
    lines = str(content)
    chinese = ''.join(re.findall('[\u4e00-\u9fef]', lines))
    return chinese


def main():
    # 文本暂存位置
    file_text = './data/text.txt'
    # 字母使用统计结果
    stat = {}
    stat_H = {}
    stat_L = {}

    # 解析参数
    file_input = args.input_filename
    if file_input is None:
        parser.error('Please specify the filename of the PDF file to process.')

    # 读取 PDF
    with open(file_input, 'rb') as my_pdf:
        text = read_pdf(my_pdf)

    # 解析并存储拼音
    result = Pinyin().get_pinyin(text, '')
    with open(file_text, 'w') as f:
        f.write(result)

    # 统计字母出现频次
    for i in range(ord('a'), ord('z') + 1):
        stat[chr(i)] = result.count(chr(i))
    stat = sorted(stat.items(), key=lambda a: a[1], reverse=True)
    print(stat)

    # 计算输入效率
    len_ch = len(text)
    len_ty = len(result)
    eta = len_ch / len_ty
    print('Lenth of Chinese characters: %d' % len_ch)
    print('Lenth of type coding: %d' % len_ty)
    print('Input efficiency: %.4f' % eta)

    # 计算均衡性
    stat_list = []
    for i in range(0, 26):
        stat_list.append(stat[i][1] / len_ty)
    stat_std = np.std(stat_list, ddof=1)
    print('Balance: %.4f' % stat_std)

    # 计算重配列均衡性
    stat_H = stat_list[:7]
    stat_L = stat_list[7:]
    # print(stat_H)
    # print(stat_L)
    stat_H_std = np.std(stat_H, ddof=1)
    stat_L_std = np.std(stat_L, ddof=1)
    stat_R_std = np.sqrt(stat_H_std * stat_H_std + stat_L_std * stat_L_std)
    print('Balance_r: %.4f' % stat_R_std)


if __name__ == '__main__':
    main()
