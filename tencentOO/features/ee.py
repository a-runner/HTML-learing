#!/root/Anaconda3/envs/py36/bin python
# -*- coding: utf-8 -*-
# @Time : 2021/5/1 11:15
# @Author : a-runner
# @Site : 
# @File : ee.py
# @Software: PyCharm
from os import listdir
from PIL import Image


ims1=Image.open('../image/祝福11.jpg')
ims2=Image.open('../image/祝福22.jpg')

width, height = ims1.size
result = Image.new(ims1.mode, (width*2, height))

imgs=[]
imgs.append(ims1)
imgs.append(ims2)
# 拼接图片
for i, im in enumerate(imgs):
    result.paste(im, box=(i * width,0))

# 保存图片
    result.save('../image/res.jpg')