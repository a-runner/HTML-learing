import tornado.ioloop
import tornado.web
import json
import pymysql

# 建立一个数据库得类
class Mysql_write():
    def __init__(self,user,password):
        try:
            self.con = pymysql.connect('localhost', 'root', 'root123', 'tencentoo', charset='utf8')
            self.user = user
            self.password = password
        except Exception as e:
            print(e)
            print('数据库连接失败！！')

    def insert_data(self):
        cursor = self.con.cursor()
        print('执行操作：{}'.format('insert into login values("{}", "{}");'.format(self.user, self.password)))
        cursor.execute('insert into login values("{}", "{}");'.format(self.user, self.password))
        self.con.commit()


    def check_phone(self):
        cursor = self.con.cursor()
        search_counts =cursor.execute('select * from login where phoneNum="{}";'.format(self.user))
        # 获得该用户的密码
        result=cursor.fetchall()
        print(result)
        self.real_pwd=result[0][1]
        # 获得该用户的用户名
        self.username=result[0][0]

        if self.password==self.real_pwd:
            return [1,self.username]
        else:
            return [0,0]

headers = {
    'Content - Type': 'application/json'
}

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("login_in.html")

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header(
            "Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE"
        )

    def post(self, *args, **kwargs):
        self.user=self.get_argument("user")
        self.pwd=self.get_argument('pwd')
        print(self.user,self.pwd)
        con = Mysql_write(self.get_argument("user"), self.get_argument('pwd'))
        # 检查数据库中是否存在该用户名
        try:
            result = con.check_phone()
            print(result)
            if result[0]:
            # con.insert_data()
                self.write(json.dumps([1,result[1]]))
            else:
                self.write(json.dumps([0,"用户名或密码错误！！！"]))

        except Exception as e:
            print(e)
            self.write(json.dumps([0,'信息不存在！！！']))

if __name__ == "__main__":

    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(8800)
    tornado.ioloop.IOLoop.current().start()