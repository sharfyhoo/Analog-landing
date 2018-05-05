#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from PIL import Image
from ordered_set import OrderedSet
import pytesseract


def graying(img):
    u"""对图片进行灰度化"""
    img = img.convert("L")
    return img


def binarization(img):
    u"""二值化,白底黑字"""
    w, h = img.size
    for y in range(h):
        for x in range(w):
            color = img.getpixel((x, y))
            print color
            if color < 254:
                img.putpixel((x, y), 0)
            else:
                img.putpixel((x,y), 255)
    return img


def filter_pixel_not_in_L(img):
    u"""去掉不在L图形中的像素."""
    width, height = img.size
    black_pixel = OrderedSet()

    for y in range(height):
        for x in range(width):
            color = img.getpixel((x, y))
            assert color in (0, 255)
            if color == 0:
                black_pixel.add((x, y))

    valid_pixel = set()
    for pixel in black_pixel:
        if not pixel_in_L(black_pixel, pixel, valid_pixel):
            img.putpixel(pixel, 255)
    return img

def pixel_in_L(black_pixel, pixel, valid_pixel):
    u"""判断像素点在不在L内"""
    x, y = pixel
    pixels = []

    for m in (-1, 0, 1):
        for n in (-1, 0, 1):
            pixels.append((x + n, y + m))   # 存储的是9个点的坐标

    com = (
        (0, 1), (0, 3), (1, 2), (1, 3), (1, 5), (2, 5),
        (3, 6), (3, 7), (5, 8), (5, 7), (6, 7), (7, 8)
    )
    for c in com:
        if pixels[c[0]] in black_pixel and pixels[c[1]] in black_pixel:
            valid_pixel.add(pixels[c[0]])
            valid_pixel.add(pixels[c[1]])
            return True
    return False

def get_char_img(img, idx):
    width, height = img.size
    w = width / 4  # 将宽平均分为四等分
    img = img.crop(w * idx, 0, w * (idx + 1), height)  # crop 后面跟(左，上，右，下，)对图片进行切割
    return img

def covert_char_to_matrix(img):
    u"""把字符图像转为统一大小的矩阵"""
    pix = np.array(img)
    center = self.find_center(pix)
    x, y = center
    pix[y, x] = 9


def make_matrices(self):
    u"""获取整个图片转成的四个 矩阵"""
    char_imgs = self.split_chars()
    tmp = []
    for idx, img in enumerate(char_imgs):
        tmp.append(self.covert_char_to_matrix(img))

def decode_captcha(img_name):
    u"""测试入口"""
    img = Image.open("img/{}".format(img_name))
    img = graying(img)
    img = binarization(img)
    img = filter_pixel_not_in_L(img)
    # chars = [get_char_img(img, i) for i in range(4)]
    char = pytesseract.image_to_string(img, lang='eng')
    print u"识别的验证码为:{}".format(char)
    return char




if __name__ == '__main__':

    #img.save('imgs/huidu1.png')

    test()




