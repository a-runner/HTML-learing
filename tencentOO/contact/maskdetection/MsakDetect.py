#!/usr/bin/env python
# coding: utf-8

# # PaddleHub 口罩检测示例
# 
# 如果您想运行本项目，请先右上角fork本项目。
# 
# ![](https://ai-studio-static-online.cdn.bcebos.com/c93b5df8cefd4c7d97848d3bafb952f7082f89b74fca44eca7ef6778f6a127a4)
# 
# 
# 
# 防控疫情，众志成城。人工智能技术正被应用到疫情防控中来。
# 
# “控制传染源、切断传播途径和排查易感人群”是打赢抗疫的三种手段。
#  
# 其中切断传播途径中，佩戴口罩已经几乎成为了最重要的举措之一。但是在实际场景中，仍然有不重视、不注意、侥幸心理的人员不戴口罩，尤其在公众场合，给个人和公众造成极大的风险隐患。
# 
# 目前，仅有少数厂商能够提供口罩佩戴人脸检测AI模型的相关商业化方案，且在密集人流下的识别效果参差不齐。而由于缺乏数据集和模型开发经验，更多中小开放商在面临园区、关口等细分场景时，更是无从下手。
# 
#  百度积极响应号召，为了助推全社会的力量将AI技术应用于防疫工作，决定免费开源自研的“口罩人脸识别”预训练模型，该模型基于2018年百度在国际顶级计算机视觉会议ECCV 2018的论文PyramidBox而研发，可以在公共场景检测大量的人脸同时，将佩戴口罩和未佩戴口罩的人脸快速识别标注。基于此预训练模型，开发者仅需使用少量自有数据，便可快速完成自有场景模型开发。
#  
#  飞桨预训练模型管理与迁移学习工具PadddleHub已提供PyramidBox预训练模型(pyramidbox_lite_mobile_mask/pyramidbox_lite_server_mask)用于一键检测人们是否佩戴口罩。同时PaddleHub还提供了飞桨生态下的高质量预训练模型，涵盖了图像分类、目标检测、词法分析、语义模型、情感分析、视频分类、图像生成、图像分割、文本审核、关键点检测等主流模型。更多模型详情请查看官网：https://www.paddlepaddle.org.cn/hub 和 PaddleHub repo：https://github.com/PaddlePaddle/PaddleHub 同时，PaddleHub已和Paddle Lite，Paddle Serving串通，可以将预训练模型直接用于移动端和服务端部署。
#  
# 通过开源AI模型，百度希望激发广大的开发者和企业厂商（尤其是视频监控），发挥各自的聪明才智，把口罩人脸识别在实际场景中应用起来，更好的做好疫情的防控工作。
# 
# 
# 本示例利用目标检测轻量化模型pyramidbox_lite_mobile_mask和pyramidbox_lite_server_mask完成佩戴口罩检测。
# 
# **NOTE：** 如果您在本地运行该项目示例，需要首先安装PaddleHub。如果您在线运行，需要首先fork该项目示例。之后按照该示例操作即可。

# In[1]:


# get_ipython().system('pip install paddlehub==1.7.1 -i https://pypi.tuna.tsinghua.edu.cn/simple')


# ## 一、定义待预测数据
# 
# 
# 以本示例中文件夹下test_mask_detection.png为待预测图片

# In[2]:


# 待预测图片
test_img_path = ["./test_mask_detection.jpg"]


# import matplotlib.pyplot as plt
import matplotlib.image as mpimg 

img = mpimg.imread(test_img_path[0]) 

# 展示待预测图片
# plt.figure(figsize=(10,10))
# plt.imshow(img)
# plt.axis('off')
# plt.show()


# 若是待预测图片存放在一个文件中，如左侧文件夹所示的test.txt。每一行是待预测图片的存放路径。

# In[3]:


# get_ipython().system('cat test.txt')


# 用户想要利用完成对该文件的口罩检测，只需读入该文件，将文件内容存成list，list中每个元素是待预测图片的存放路径。

# In[4]:


with open('test.txt', 'r') as f:
    test_img_path=[]
    for line in f:
        test_img_path.append(line.strip())
print(test_img_path)


# ## 二、加载预训练模型
# 
# PaddleHub口罩检测提供了两种预训练模型，[pyramidbox_lite_mobile_mask](https://www.paddlepaddle.org.cn/hubdetail?name=pyramidbox_lite_mobile_mask&en_category=ObjectDetection)和[pyramidbox_lite_server_mask](https://www.paddlepaddle.org.cn/hubdetail?name=pyramidbox_lite_server_mask&en_category=ObjectDetection)。二者均是基于2018年百度发表于计算机视觉顶级会议ECCV 2018的论文PyramidBox而研发的轻量级模型，模型基于主干网络FaceBoxes，对于光照、口罩遮挡、表情变化、尺度变化等常见问题具有很强的鲁棒性。不同点在于，pyramidbox_lite_mobile_mask是针对于移动端优化过的模型，适合部署于移动端或者边缘检测等算力受限的设备上。

# In[4]:


import paddlehub as hub

module = hub.Module(name="pyramidbox_lite_mobile_mask")
# module = hub.Module(name="pyramidbox_lite_server_mask")


# ## 三、预测
# 
# 
# PaddleHub对于支持一键预测的module，可以调用module的相应预测API，完成预测功能。

# In[7]:


import os

import cv2

imgs = [cv2.imread(test_img_path[0])]

# 口罩检测预测
# visualization=True 将预测结果保存图片可视化
# output_dir='detection_result' 预测结果图片保存在当前运行路径下detection_result文件夹下
results = module.face_detection(images=imgs, use_multi_scale=True, shrink=0.6, visualization=True, output_dir='detection_result')
# for result in results:
#     print(result)

# 预测结果展示

path = os.path.join('detection_result', 'test_img.jpg')
img = mpimg.imread(path)
# plt.figure(figsize=(10,10))
# plt.imshow(img)
# plt.axis('off')
# plt.show()
cv2.imwrite('./result/maskdetection.jpg',img)



# 上一步骤的输出结果，有三条数据：
# ```
# {'data': {'label': 'MASK', 'left': 457.5789153575897, 'right': 654.8277450799942, 'top': 182.25817680358887, 'bottom': 440.94200134277344, 'confidence': 0.8900112}, 'id': 1}
# {'data': {'label': 'MASK', 'left': 945.8848892450333, 'right': 1125.7660418748856, 'top': 340.7917723059654, 'bottom': 578.5958737134933, 'confidence': 0.99627507}, 'id': 1}
# {'data': {'label': 'NO MASK', 'left': 1166.5987054109573, 'right': 1323.4498780965805, 'top': 292.07742512226105, 'bottom': 500.40101408958435, 'confidence': 0.9576567}, 'id': 1}
# ```
# 
# 其中，label有'MASK'和'NO MASK'两种选择：'MASK'表示戴了口罩，'NO MASK表示没有佩戴口罩。'left'/'rigth'/'top'/'bottom'表示口罩在图片当中的位置。'confidence'表示预测为佩戴口罩'MASK'或者不佩戴口罩'NO MASK'的概率大小。
# 

# 同时，作为一项完善的开源工作，除了本地推断以外，PaddleHub还支持将该预训练模型部署到服务器或移动设备中。
# 
# **由于AIStudio不支持ip访问，以下代码仅做示例，如有需要，请在本地机器运行。**
# 
# ## 四、部署服务器
# 
# 借助 PaddleHub，服务器端的部署也非常简单，直接用一条命令行在服务器启动口罩人脸检测与分类模型就行了：
# 
# ```shell
# $ hub serving start -m pyramidbox_lite_server_mask -p 8866
# ```
# 
# 是的，在服务器端这就完全没问题了。相比手动配置各种参数或者调用各种框架，PaddleHub 部署服务器实在是太好用了。
# 
# 只要在服务器端完成部署，剩下在客户端调用就不会有多大问题了。如下百度展示了调用服务器做推断的示例：制定要预测的图像列表、发出推断请求、返回并保存推断结果。
# 
# 
# ```python
# # coding: utf8
# import requests
# import json
# import base64
# import os
# 
# # 指定要检测的图片并生成列表[("image", img_1), ("image", img_2), ... ]
# file_list = ["test.jpg"]
# files = [("image", (open(item, "rb"))) for item in file_list]
# 
# # 指定检测方法为pyramidbox_lite_server_mask并发送post请求
# url = "http://127.0.0.1:8866/predict/image/pyramidbox_lite_server_mask"
# r = requests.post(url=url, files=files, data={"visual_result": "True"})
# 
# results = eval(r.json()["results"])
# 
# # 保存检测生成的图片到output文件夹，打印模型输出结果
# if not os.path.exists("output"):
#     os.mkdir("output")
# for item in results:
#     with open(os.path.join("output", item["path"]), "wb") as fp:
#         fp.write(base64.b64decode(item["base64"].split(',')[-1]))
#         item.pop("base64")
# print(json.dumps(results, indent=4, ensure_ascii=False))
# ```
# 
# 相信只要有一些 Python 基础，在本地预测、以及部署到服务器端都是没问题的，飞桨的 PaddleHub 已经帮我们做好了各种处理过程。
# 

# ## 五、移动端部署
# 
# Paddle Lite 是飞桨的端侧推理引擎，专门面向移动端的模型推理部署。如果我们需要把口罩人脸检测及分类模型嵌入到手机等移动设备，那么 Paddle Lite 这样的端侧推理引擎能帮我们节省很多工作。
# 
# 在移动端部署口罩人脸检测及分类模型，也只需要三步：①下载预测库，Paddle Lite 会提供编译好的预测库；②优化模型，使用 model_optimize_tool 工具实现模型优化；③通过预测 API 实现调用。
# 
# **Paddle Lite 介绍：https://github.com/PaddlePaddle/Paddle-Lite/**
# 
# 开发者可以通过PaddleHub下载人脸口罩识别模型。
# 在正常安装PaddleHub以后，可以通过python执行以下代码下载并保存模型
# 以下载保存移动端人脸口罩识别模型为例：
# 
# ```python
# # coding: utf8
# import paddlehub as hub
# module = hub.Module(name="pyramidbox_lite_mobile_mask")
# # 将模型保存在test_program文件夹之中
# module.processor.save_inference_model(dirname="test_program") 
# ```
# 
# 通过以上代码，可以获得人脸检测和口罩佩戴判断模型，分别存储在test_program 目录下的pyramidbox_lite和mask_detector子文件夹之中。文件夹中的__model__是模型结构文件，__param__文件是权重文件。

# 
# 其中比较重要的是移动端 API 调用方法，具体实现请参考下文给出的 Paddle Lite 的示例地址。
# 
# ```c++
# // 读取图片
# cv::Mat img = imread(img_path, cv::IMREAD_COLOR); 
# // 加载人脸检测或者口罩佩戴判别模型
# MobileConfig config;
# config.set_model_dir(model_dir);
# PaddlePredictor* predictor =
#       CreatePaddlePredictor<MobileConfig>(config); 
# // 设置输入
# Tensor* input_tensor = predictor->GetInput(0);
# input_tensor->Resize({1, 3, img.rows，img.cols});
# set_input(img, input_tensor); //调用自定义函数
# // 执行
# predictor->Run();  
# // 输出结果
# Tensor* output_tensor = predictor->GetOutput(0);
# show_output(img, output_tensor); //调用自定义函数
# ```
# 
# 人脸识别和佩戴口罩判断在移动端部署的示例地址为：
# https://github.com/PaddlePaddle/Paddle-Lite/tree/develop/lite/demo/cxx

# 如您在运行本教程有任何疑问，可以通过以下两种方式提问：
# * 进入 飞桨官方技术交流QQ群：79677175 提问
# * 通过PaddleHub repo提issue https://github.com/PaddlePaddle/PaddleHub/issues
