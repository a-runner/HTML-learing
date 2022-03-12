#!/root/Anaconda3/envs/py36/bin python
# -*- coding: utf-8 -*-
# @Time : 2021/4/30 14:53
# @Author : a-runner
# @Site : 
# @File : detect.py
# @Software: PyCharm
import tornado.ioloop
import tornado.web
import paddlehub as hub
import os

import cv2

module = hub.Module(name="pyramidbox_lite_mobile_mask")



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("mask.html")

    def post(self, *args, **kwargs):
        file_metas = self.request.files["fileDemo"]
        print(file_metas)
        # import pdb
        # pdb.set_trace()
        for meta in file_metas:
            file_name = meta['filename']
            file_name="../image/口罩检测/"+file_name
            with open(file_name, 'wb') as up:
                up.write(meta['body'])
            self.write("成功")
            imgs = [cv2.imread(file_name)]
            results = module.face_detection(images=imgs, use_multi_scale=True, shrink=0.6, visualization=True,
                                            output_dir='detection_result')
            file_name2="../image/口罩检测/"+"detection_result/"

            # with open(file_name, 'wb') as up:
            #     up.write(meta['body'])
            # self.write(1)


if __name__ == "__main__":

    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(8800)
    tornado.ioloop.IOLoop.current().start()