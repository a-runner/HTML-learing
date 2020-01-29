import tornado.ioloop
import tornado.web




class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("小案例.html")

    def post(self, *args, **kwargs):
        a = int(self.get_argument("aa"))
        b = int(self.get_argument("bb"))
        c = a + b
        print(c)
        re_data = {
            'result':c
        }
        self.write(re_data)
        # self.write('提交成功')

if __name__ == "__main__":

    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(8800)
    tornado.ioloop.IOLoop.current().start()