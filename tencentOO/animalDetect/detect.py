#!/root/Anaconda3/envs/py36/bin python
# -*- coding: utf-8 -*-
# @Time : 2021/6/3 19:52
# @Author : a-runner
# @Site : 
# @File : detect.py
# @Software: PyCharm
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
import requests
import base64
import json
import paddlehub as hub
import cv2



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("beauty.html")

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header(
            "Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE"
        )
        self.set_header("Access-Control-Allow-Headers", "*")
    def post(self, *args, **kwargs):
        file_metas = self.request.files["fileDemo"]
        # print(file_metas)
        # import pdb
        # pdb.set_trace()
        for meta in file_metas:
            file_name = meta['filename']
            file_name="../image/动物检测/"+file_name
            with open(file_name, 'wb') as up:
                up.write(meta['body'])
            up.close()
            f=open(file_name,'rb')
            module = hub.Module(name="resnet50_vd_animals")
            # module = hub.Module(name="mobilenet_v2_animals")
            np_images = [cv2.imread(file_name)]

            results = module.classification(images=np_images)

            # for result in results:
            #     print(result)
            self.write(str(results))


if __name__ == "__main__":
    # tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/animalDetect", MainHandler),
    ])
    # http_server = tornado.httpserver.HTTPServer(application)  # 创建httpserver实例
    # http_server.listen(8080)
    application.listen(8800)
    tornado.ioloop.IOLoop.current().start()