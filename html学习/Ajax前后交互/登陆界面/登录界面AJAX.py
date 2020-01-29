import tornado.ioloop
import tornado.web




class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("登陆界面.html")

    def post(self, *args, **kwargs):
        print(self.get_argument('user'))
        print(self.get_argument('pwd'))
        print(self.get_argument('sex'))
        print(self.get_arguments('hobby'))
        print(self.get_argument('file'))
        print(self.get_argument('address'))
        print(self.get_argument('introduction'))

if __name__ == "__main__":

    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(8800)
    tornado.ioloop.IOLoop.current().start()