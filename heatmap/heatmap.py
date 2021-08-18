#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import os
import re
import argparse
from io import StringIO
from io import open
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from xpinyin import Pinyin

parser = argparse.ArgumentParser(description='Generate a keyboard heatmap from a PDF file.')
parser.add_argument('input_filename', metavar='input_file', type=str,
                    help='the name of the file to process')
parser.add_argument('output_filename', metavar='output_file', type=str,
                    help='the name of the image file to output')
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
    chinese = ''.join(re.findall('[\u4e00-\u9fa5]', lines))
    return chinese


def main():

    # 文本暂存位置
    file_text = './data/text.txt'
    # 字母使用统计结果
    stat = {}

    # 解析参数
    file_input = args.input_filename
    if file_input is None:
        parser.error('Please specify the filename of the PDF file to process.')
    file_output = args.output_filename
    if file_output is None:
        parser.error('Please specify the name of the image to generate.')

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
    print(stat)

    # 绘制热力图
    cmd = 'tapmap ' + file_text + ' ' + file_output + ' -c Blues'
    res = os.popen(cmd).readlines()
    print(res)

    # 显示图片
    lena = mpimg.imread(file_output)
    plt.imshow(lena)
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    main()
