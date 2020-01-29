import tornado.ioloop
import tornado.web

# class MainHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.render("AJAX.html")
#
#     def post(self, *args, **kwargs):
#         print(self.get_argument("user"))
#         print(self.get_argument("pwd"))
#         self.write('登陆成功')
#
# if __name__ == "__main__":
#
#     application = tornado.web.Application([
#         (r"/", MainHandler),
#     ])
#     application.listen(8888)
#     tornado.ioloop.IOLoop.current().start()
#



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("AJAX.html")

    def post(self, *args, **kwargs):
        print(self.get_argument("name"))
        # print(self.get_argument("pwd"))
        self.write('提交成功')

if __name__ == "__main__":

    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(8800)
    tornado.ioloop.IOLoop.current().start()