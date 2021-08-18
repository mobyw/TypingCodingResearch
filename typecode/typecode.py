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

initials = ['b', 'p', 'm', 'f', 'd', 't', 'n', 'l',
            'g', 'k', 'h', 'j', 'q', 'x',
            'zz', 'cc', 'ss', 'r', 'z', 'c', 's',
            'y', 'w']

initials_single = [
    [' ba ', ' bei ', ' bu '],
    [' pa ', ' pi ', ' po '],
    [' me ', ' mei ', ' men ', ' mian ', ' ming '],
    [' fa ', ' fang ', ' fen '],
    [' da ', ' dan ', ' dang ', ' dao ', ' de ', ' di ', ' dong ', ' du ', ' dui ', ' duo '],
    [' ta ', ' tian ', ' tong ', ' tou '],
    [' na ', ' neng ', ' ni ', ' nian ', ' nv '],
    [' lai ', ' lao ', ' le ', ' li ', ' liang '],
    [' gan ', ' gao ', ' ge ', ' gei ', ' guo '],
    [' kai ', ' kan ', ' ke '],
    [' hao ', ' he ', ' hen ', ' hou ', ' hua ', ' huan ', ' hui ', ' huo '],
    [' ji ', ' jia ', ' jian ', ' jin ', ' jing ', ' jiu '],
    [' qi ', ' qian ', ' qin ', ' qing ', ' qu '],
    [' xia ', ' xian ', ' xiang ', ' xiao ', ' xie ', ' xin ', ' xing ', ' xue '],
    [' zhao ', ' zhe ', ' zheng ', ' zhi ', ' zhong '],
    [' chang ', ' cheng ', ' chu '],
    [' shang ', ' shen ', ' sheng ', ' shi ', ' shou ', ' shuo '],
    [' ran ', ' ren ', ' ri ', ' ru '],
    [' zai ', ' zi ', ' zong ', ' zui ', ' zuo '],
    [' ci ', ' cong '],
    [' si ', ' suo '],
    [' yang ', ' yao ', ' ye ', ' yi ', ' yin ', ' yong ', ' you ', ' yu '],
    [' wei ', ' wo ', ' wu ']
]

initials_values = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0],
    [0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0]
]

initials_dict = {' zh': ' zz', ' ch': ' cc', ' sh': ' ss'}

finals_dict = {'ng ': 'm ', 'uan ': 'on ', 'iao ': 'eo '}

sel_array = ['vp', 'vk', 'vr', 'vf', 'vq', 'vw', 'vt', 'vb', 'vh', 'vx']

# 文本暂存位置
file_text_separated = './data/text_separated.txt'
file_text_encode = './data/text_encode.txt'
file_text = './data/text.txt'
file_img_org = './data/img_org.png'


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


def cal_efficiency(len_ch, len_ty):
    eta = len_ch / len_ty
    print('Lenth of Chinese characters: %d' % len_ch)
    print('Lenth of type coding: %d' % len_ty)
    print('Input efficiency: %.4f' % eta)


def cal_balance(stat):
    stat_sum = 0
    stat_word = []
    stat_list = []

    for i in range(0, 26):
        stat_word.append(stat[i][0])
        stat_list.append(stat[i][1])
        stat_sum += stat[i][1]
    for i in range(0, 26):
        stat_list[i] /= stat_sum

    stat_std = np.std(stat_list, ddof=1)
    print('Balance: %.4f' % stat_std)

    # 计算重配列均衡性
    stat_H = stat_list[:7]
    stat_L = stat_list[7:]
    stat_H_std = np.std(stat_H, ddof=1)
    stat_L_std = np.std(stat_L, ddof=1)
    stat_R_std = np.sqrt(stat_H_std * stat_H_std + stat_L_std * stat_L_std)
    print('Balance_r: %.4f' % stat_R_std)


def draw_heatmap(file_output):
    cmd = 'tapmap ' + file_text + ' ' + file_output + ' -c Blues'
    res = os.popen(cmd).readlines()
    # print(res)


def re_encode(org):
    res = org

    for i in range(len(initials_single)):
        for j in range(len(initials_single[i])):
            initials_values[i][j] = res.count(initials_single[i][j])
        res = res.replace(
            initials_single[i][initials_values[i].index(max(initials_values[i]))],
            ' ' + initials[i] + ' ')
        print('Replace with ' + initials[i] + ' :' +
              initials_single[i][initials_values[i].index(max(initials_values[i]))])

    for key, value in initials_dict.items():
        res = res.replace(key, value)
        print('Replace with' + value + ' :' + key)
    for key, value in finals_dict.items():
        res = res.replace(key, value)
        print('Replace with ' + value + ': ' + key)

    return res


def re_replace(org):
    words = org.split()
    counts = {}

    for word in words:
        if len(word) >= 3:
            counts[word] = counts.get(word, 0) + 1

    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)

    res = org

    for i in range(10):
        word, count = items[i]
        # print("{0:<10}{1:>5}".format(word, count))
        res = res.replace(' ' + word + ' ', ' ' + sel_array[i] + ' ')
        print('Replace with ' + sel_array[i] + ' : ' + word)

    return res


def main():
    # 字母使用统计结果
    stat = {}
    stat_re = {}

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

    # 绘制热力图
    draw_heatmap(file_img_org)

    print('\n\n====== Re-encode ======\n')

    # 重新编码
    result_re = re_encode(result_separated)
    result_re = re_replace(result_re)
    with open(file_text_encode, 'w') as f:
        f.write(result_re)
    result = ''.join(re.findall('[a-z]', result_re))
    with open(file_text, 'w') as f:
        f.write(result)

    # 统计字母出现频次
    for i in range(ord('a'), ord('z') + 1):
        stat_re[chr(i)] = result.count(chr(i))
    stat_re = sorted(stat_re.items(), key=lambda x: x[1], reverse=True)
    print(stat_re)

    # 计算输入效率
    cal_efficiency(len(text), len(result))

    # 计算均衡性
    cal_balance(stat_re)

    # 绘制热力图
    draw_heatmap(file_output)

    # 显示图片
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
