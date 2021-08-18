#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import os
import re
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from io import StringIO
from io import open
from xpinyin import Pinyin
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, process_pdf

parser = argparse.ArgumentParser(description='Generate a keyboard heatmap from a PDF file.')
parser.add_argument('input_filename', metavar='input_file', type=str,
                    help='the name of the file to process')
parser.add_argument('output_filename', metavar='output_file', type=str,
                    help='the name of the image file to output')
args = parser.parse_args()

# 声母替换数据字典
initials_dict = {
    "b": "B",
    "c": "C",
    "d": "D",
    "f": "F",
    "g": "G",
    "h": "H",
    "j": "J",
    "k": "K",
    "l": "L",
    "m": "M",
    "n": "N",
    "p": "P",
    "q": "Q",
    "r": "R",
    "s": "S",
    "t": "T",
    "w": "W",
    "x": "X",
    "y": "Y",
    "z": "Z",
    "ch": "I",
    "sh": "U",
    "zh": "V"
}

# 介母韵母替换数据字典
finals_dict = {
    "a": "A",
    "ai": "L",
    "an": "J",
    "ang": "H",
    "ao": "K",
    "e": "E",
    "ei": "Z",
    "en": "F",
    "eng": "G",
    "i": "I",
    "ia": "W",
    "ian": "M",
    "iang": "D",
    "iao": "C",
    "ie": "X",
    "ong": "S",
    "in": "N",
    "ing": "Y",
    "iu": "Q",
    "o": "O",
    "ou": "B",
    "u": "U",
    "uan": "R",
    "ue": "T",
    "un": "P",
    "v": "V",
}

# 零声母替换数据字典
others_dict = {
    "a": "AA",
    "ai": "AI",
    "an": "AN",
    "ang": "AH",
    "ao": "AO",
    "e": "EE",
    "ei": "EI",
    "en": "EN",
    "eng": "EG",
    "er": "ER",
    "o": "OO",
    "ou": "OU"
}

# 可重用的声母，替换为较短者
reuse_dict = {
    "uang": "iang",
    "iong": "ong",
    "uai": "ing",
    "ua": "ia",
    "ve": "ue",
    "uo": "o",
    "ui": "v"
}

# 文本暂存位置
# 空格分隔的原始拼音
file_text_separated = './data/text_separated.txt'
# 空格分隔的重编码拼音
file_text_encode = './data/text_encode.txt'
# 无间隔重编码拼音
file_text = './data/text.txt'
# 原始全拼热力图路径
file_img_org = './data/img_org.png'

# 存放声母、介母韵母统计数据
phrase_in = {}
phrase_fi = {}


# 从 PDF 读取中文字符文本数据
def read_pdf(pdf):
    # 资源管理器配置
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()

    # 文本转换工具
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    process_pdf(rsrcmgr, device, pdf)
    device.close()
    content = retstr.getvalue()
    retstr.close()

    # 获取内容并提取汉字
    lines = str(content)
    chinese = ''.join(re.findall('[\u4e00-\u9fef]', lines))

    return chinese


# 计算并打印输入效率
def cal_efficiency(len_ch, len_ty):
    eta = len_ch / len_ty
    print('Lenth of Chinese characters: %d' % len_ch)
    print('Lenth of type coding: %d' % len_ty)
    print('Input efficiency: %.4f' % eta)


# 计算并打印均衡度
def cal_balance(stat):
    stat_sum = 0
    stat_word = []
    stat_list = []

    # 分离字母与频次
    for i in range(0, 26):
        stat_word.append(stat[i][0])
        stat_list.append(stat[i][1])
        stat_sum += stat[i][1]
    for i in range(0, 26):
        stat_list[i] /= stat_sum

    # 计算均衡度
    stat_std = np.std(stat_list, ddof=1)
    print('Balance: %.4f' % stat_std)

    # 计算重配列均衡度
    stat_H = stat_list[:7]
    stat_L = stat_list[7:]
    stat_H_std = np.std(stat_H, ddof=1)
    stat_L_std = np.std(stat_L, ddof=1)
    stat_R_std = np.sqrt(stat_H_std * stat_H_std + stat_L_std * stat_L_std)
    print('Balance_r: %.4f' % stat_R_std)


# 根据文本文件绘制热力图
def draw_heatmap(file_output):
    cmd = 'tapmap ' + file_text + ' ' + file_output + ' -c Blues'
    res = os.popen(cmd).readlines()
    print(res)


# 统计声母、介母韵母出现频次
def re_count(org):
    tmp = org

    # 替换重用介母韵母
    for key, value in reuse_dict.items():
        tmp = tmp.replace(key + ' ', value + ' ')

    # 替换零声母
    for key, value in others_dict.items():
        tmp = tmp.replace(' ' + key + ' ', ' ' + value + ' ')

    # 统计声母频次，从长到短，统计后替换以免多次计算
    for key, value in initials_dict.items():
        if len(key) == 2:
            phrase_in[key] = tmp.count(key)
            tmp = tmp.replace(' ' + key, ' ' + value)
    for key, value in initials_dict.items():
        if len(key) == 1:
            phrase_in[key] = tmp.count(key)
            tmp = tmp.replace(' ' + key, ' ' + value)

    # 统计介母韵母频次，从长到短，统计后替换以免多次计算
    for key, value in finals_dict.items():
        if len(key) == 4:
            phrase_fi[key] = tmp.count(key)
            tmp = tmp.replace(key + ' ', value + ' ')
    for key, value in finals_dict.items():
        if len(key) == 3:
            phrase_fi[key] = tmp.count(key)
            tmp = tmp.replace(key + ' ', value + ' ')
    for key, value in finals_dict.items():
        if len(key) == 2:
            phrase_fi[key] = tmp.count(key)
            tmp = tmp.replace(key + ' ', value + ' ')
    for key, value in finals_dict.items():
        if len(key) == 1:
            phrase_fi[key] = tmp.count(key)


# 重编码
def re_encode(org, list_in, list_fi):
    res = org
    tmp = {}

    # 替换重用介母韵母
    for key, value in reuse_dict.items():
        res = res.replace(key + ' ', value + ' ')
        print('Notice: "' + value + '" same with "' + key + '"')

    # 替换零声母拼音
    for key, value in others_dict.items():
        res = res.replace(' ' + key + ' ', ' ' + value + ' ')
        print('Replace with ' + value + ' : ' + key)

    # 固定替换声母
    for key, value in list_in:
        if len(key) == 2:
            res = res.replace(' ' + key, ' ' + initials_dict[key])
            print('Replace with ' + initials_dict[key] + ' : ' + key)
    for key, value in list_in:
        if len(key) == 1:
            res = res.replace(' ' + key, ' ' + initials_dict[key])
            print('Replace with ' + initials_dict[key] + ' : ' + key)

    # 倒序创建介母韵母替代方案数列
    for i in range(len(list_in)):
        tmp[i] = initials_dict[list_in[i][0]]
    tmp[23] = 'A'
    tmp[24] = 'E'
    tmp[25] = 'O'

    # 依次替换介母韵母
    for i in range(len(list_fi)):
        if len(list_fi[i][0]) == 4:
            res = res.replace(list_fi[i][0] + ' ', tmp[i] + ' ')
            print('Replace with ' + tmp[i] + ' : ' + list_fi[i][0])
    for i in range(len(list_fi)):
        if len(list_fi[i][0]) == 3:
            res = res.replace(list_fi[i][0] + ' ', tmp[i] + ' ')
            print('Replace with ' + tmp[i] + ' : ' + list_fi[i][0])
    for i in range(len(list_fi)):
        if len(list_fi[i][0]) == 2:
            res = res.replace(list_fi[i][0] + ' ', tmp[i] + ' ')
            print('Replace with ' + tmp[i] + ' : ' + list_fi[i][0])
    for i in range(len(list_fi)):
        if len(list_fi[i][0]) == 1:
            res = res.replace(list_fi[i][0] + ' ', tmp[i] + ' ')
            print('Replace with ' + tmp[i] + ' : ' + list_fi[i][0])

    # 替换后均为大写字母，转为小写
    res = res.lower()

    return res


def main():
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
    result_separated = ' ' + Pinyin().get_pinyin(text, ' ') + ' '
    with open(file_text_separated, 'w') as f:
        f.write(result_separated)

    print('\n\n====== Original ======\n')

    # 直接使用原始数据
    result_org = result_separated
    with open(file_text_encode, 'w') as f:
        f.write(result_org)
    result = ''.join(re.findall('[a-z]', result_org))
    with open(file_text, 'w') as f:
        f.write(result)

    # 统计字母出现频次
    for i in range(ord('a'), ord('z') + 1):
        stat[chr(i)] = result.count(chr(i))
    stat = sorted(stat.items(), key=lambda x: x[1], reverse=True)
    print(stat)

    # 计算输入效率
    cal_efficiency(len(text), len(result))

    # 计算均衡性
    cal_balance(stat)

    # 生成热力图文件
    draw_heatmap(file_img_org)

    print('\n\n====== Re-encode ======\n')

    # 统计声母、介母韵母各自频次，两个排序相反
    re_count(result_org)
    list_in = sorted(phrase_in.items(), key=lambda x: x[1], reverse=True)
    list_fi = sorted(phrase_fi.items(), key=lambda x: x[1], reverse=False)

    # 重新编码
    result_re = re_encode(result_separated, list_in, list_fi)
    with open(file_text_encode, 'w') as f:
        f.write(result_re)
    result = ''.join(re.findall('[a-z]', result_re))
    with open(file_text, 'w') as f:
        f.write(result)

    # 统计字母出现频次
    stat_re = {}
    for i in range(ord('a'), ord('z') + 1):
        stat_re[chr(i)] = result.count(chr(i))
    stat_re = sorted(stat_re.items(), key=lambda x: x[1], reverse=True)
    print(stat_re)

    # 计算输入效率
    cal_efficiency(len(text), len(result))

    # 计算均衡性
    cal_balance(stat_re)

    # 生成热力图文件
    draw_heatmap(file_output)

    # 对比显示两张热力图图片文件
    img1 = mpimg.imread(file_img_org)
    img2 = mpimg.imread(file_output)
    plt.subplot(2, 1, 1)
    plt.imshow(img1)
    plt.title('Original')
    plt.axis('off')
    plt.subplot(2, 1, 2)
    plt.imshow(img2)
    plt.title('Improved')
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    main()
