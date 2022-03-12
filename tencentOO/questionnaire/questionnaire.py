#!/root/Anaconda3/envs/py36/bin python
# -*- coding: utf-8 -*-
# @Time : 2021/9/21 8:44
# @Author : a-runner
# @Site : 
# @File : questionnaire.py
# @Software: PyCharm
import tornado.ioloop
import tornado.web
import json
import pymysql

# 建立一个数据库得类
class Mysql_write():
    def __init__(self,user,age,tele,ocup,education,use,how,app):
        try:
            self.con = pymysql.connect('localhost', 'root', 'root123', 'tencentoo', charset='utf8')
            self.user = user
            self.ocup = ocup
            self.tele = tele
            self.education = education
            self.age = age
            self.use = use
            self.how = how
            self.app = app

        except Exception as e:
            print(e)
            print('数据库连接失败！！')

    # 问卷调查表的 表
    def insert_data(self):
        cursor = self.con.cursor()
        print('执行操作：{}'.format('insert into question values("{}", "{}","{}", "{}","{}", "{}","{}", "{}");'.format(self.user,self.age,self.tele,self.ocup,self.education,self.use,self.how,self.app)))
        cursor.execute('insert into question values("{}", "{}","{}", "{}","{}", "{}","{}", "{}");'.format(self.user,self.age,self.tele,self.ocup,self.education,self.use,self.how,self.app))
        self.con.commit()


    def check_phone(self):
        cursor = self.con.cursor()
        search_counts =cursor.execute('select * from question where name="{}";'.format(self.user))
        # 获得该用户的密码
        result=cursor.fetchall()
        print(result)

        if result[0]:
            return [1,self.username]
        else:
            return [0,0]

headers = {
    'Content - Type': 'application/json'
}

class QuestionHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("../questionnaire/questionnaiire.html")

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header(
            "Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE"
        )

    def post(self, *args, **kwargs):
        self.user=self.get_argument("username")
        self.ocup=self.get_argument('occupation')
        self.tele=self.get_argument('tele')
        self.education=self.get_argument('education')
        self.age=self.get_argument('age')
        self.use=self.get_argument('use')
        self.how=self.get_argument('how')
        self.app=self.get_argument('app')
        print('捕获到： ',self.user,'提交的表单')
        con = Mysql_write(self.user,self.age,self.tele,self.ocup,self.education,self.use,self.how,self.app)
        # 检查数据库中是否存在该用户名
        try:
            result = con.check_phone()
            print(result)
            if result[0]:
            # con.insert_data()
                self.write(json.dumps([1,result[1]]))
            else:
                self.write(json.dumps([0,"能重复提交！！！"]))

        except Exception as e:
            print(e)
            self.write(json.dumps([0,'出现错误！！！']))

if __name__ == "__main__":

    application = tornado.web.Application([
        (r"/", QuestionHandler),
    ])
    application.listen(8800)
    tornado.ioloop.IOLoop.current().start()