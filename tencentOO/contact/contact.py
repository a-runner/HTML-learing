#!/root/Anaconda3/envs/py36/bin python
# -*- coding: utf-8 -*-
# @Time : 2021/5/4 22:53
# @Author : a-runner
# @Site : 
# @File : contact.py
# @Software: PyCharm
import tornado.ioloop
import tornado.web
import pymysql
import tornado.options
import requests
import json
import time

# 建立一个 new database
class Mysql_write():
    def __init__(self,user):
        try:
            self.con = pymysql.connect('localhost', 'root', 'root123', 'customer', charset='utf8')
            self.user = user
            # self.password = password
        except Exception as e:
            print(e)
            print('数据库连接失败！！')

    def rec_from_all_people(self):
        cursor = self.con.cursor()
        sql1='show tables;'
        cursor.execute(sql1)
        re=cursor.fetchall()
        result=[]
        for i in range(len(re)):
            sql = r'select * from {} where recver="{}";'.format(re[i][0],self.user)
            print(sql)
            cursor.execute(sql)
            rr=cursor.fetchall()
            rr=list(rr)
            rr.reverse()
            # print(rr)
            rra=rr[0:[len(rr) if len(rr)<13 else 13][0]]
            # print("rra:   ",rra)
            for i in range(len(rra)):
                result.append(rra[i])
            # print("result: ",result)

        # sql=r''
        index=sorted(range(len(result)), key=lambda k: result[k][4], reverse=False)
        rrr=[]
        for i in index:
            rrr.append(result[i])

        # print("rrr: ",rrr)
        return rrr

    def rec_all_username(self):
        cursor = self.con.cursor()
        sql1 = 'show tables;'
        cursor.execute(sql1)
        re = cursor.fetchall()
        result=[r[0]+'\n' for r in re]

        return result


    def rec_data(self,recName):
        recName=recName.strip()
        cursor = self.con.cursor()
        sql='SHOW TABLES LIKE "{}";'.format(recName)
        self.con.commit()
        cursor.execute(sql)
        result=cursor.fetchall()
        res = []
        ty = []
        if not result[0]:
            # 创建该表
            sql=r'CREATE TABLE {} ( ' \
                r'sender varchar(20) NOT NULL,' \
                r'recver varchar(20) DEFAULT NULL,' \
                r'message varchar(100) DEFAULT NULL,' \
                r'type varchar(5) DEFAULT NULL' \
                r'time varchar(30) DEFAULT NULL) DEFAULT CHARSET=utf8'.format(recName)
            # ENGINE = InnoDB
            # AUTO_INCREMENT = 1
            cursor.execute(sql)
            self.con.commit()
            return res
        else:
            # 查找是否有需要的信息
            sql1=r'select * from {} where recver="{}";'.format(recName,self.user)
            sql2 = r'select * from {} where recver="{}";'.format(self.user,recName)
            cursor.execute(sql1)
            result1=cursor.fetchall()
            result1 = list(result1)
            result1.reverse()
            result11 = result1[0:[len(result1) if len(result1)<13 else 13][0]]
            cursor.execute(sql2)
            result2=cursor.fetchall()
            result2 = list(result2)
            result2.reverse()
            result22 = result2[0:[len(result2) if len(result2)<13 else 13][0]]

            for i in result22:
                result11.append(i)

            print("result11 back:",result11)

            index=sorted(range(len(result11)), key=lambda k: result11[k][4], reverse=False)

            rrr = []
            for i in index:
                rrr.append(result11[i])

            print("errrr:  ",rrr)
        return rrr

    def insert_data(self,sendName,message):
        cursor = self.con.cursor()
        sql = 'SHOW TABLES LIKE "{}";'.format(self.user)
        self.con.commit()
        cursor.execute(sql)
        result = cursor.fetchall()
        if not result:
            # 创建该表
            sql = r'CREATE TABLE {} ( ' \
                  r'"sender" varchar(20) NOT NULL,' \
                  r'"recver" varchar(20) DEFAULT NULL,' \
                  r'"message" varchar(100) DEFAULT NULL,' \
                  r'"type" varchar(5) DEFAULT NULL' \
                  r'"time" varchar(30) DEFAULT NULL) DEFAULT CHARSET=utf8'.format(
                sendName)
            cursor.execute(sql)
            self.con.commit()
        else:
            datatime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            sql='insert into {} values("{}", "{}","{}","{}","{}")'.format(self.user, sendName,message,0,datatime)
            cursor.execute(sql)
            self.con.commit()


    def check_name(self,recName):
        cursor = self.con.cursor()
        sql1 = 'SHOW TABLES LIKE "{}";'.format(recName)
        cursor.execute(sql1)
        re = cursor.fetchall()

        return re


headers = {
    'Content - Type': 'application/json'
}

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("interaction.html")


    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header(
            "Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE"
        )


    def post(self, *args, **kwargs):
        # 过去当前的用户名
        self.result={}
        self.user=self.get_argument("user").strip('\\')
        self.recver=self.get_argument("recver").strip('\\')
        self.message=self.get_argument("message").strip('\\')
        # type代表接受还是发送
        # print(self.user)
        self.ty=self.get_argument("ty")

        con = Mysql_write(self.get_argument("user"))
        # 检查数据库中是否存在该用户名
        try:
            if self.ty==1 or self.ty=='1':

                result = con.check_name()
                if result[0]:
                    if self.message:
                        con.insert_data(self.recver,self.message)

                        # self.write([1,"操作成功"])
                        rres=con.rec_data(self.recver)
                        # rres=rres[-13:-1:1]
                        rrres=rres[0:[len(rres) if len(rres)<13 else 13][0]]
                        self.write(json.dumps({"0":1,"1":rrres,"len":len(rrres)}))
                    else:
                        self.write(json.dumps({"0":0, "1":"不能发送空消息！！！"}))
                else:
                    self.write(json.dumps({"0":0,"1":"错误！！！"}))
            elif self.ty==0 or self.ty=='0':
                if self.recver:
                    result = con.check_name(self.recver)
                    if result[0]:
                        res = con.rec_data(self.recver)
                        # if len(res)>12:
                        #     res=res[-13:-1:1]
                        # 不为空
                        if res:
                            self.result={}
                            self.result["recv"] = res[0:[len(res) if len(res)<13 else 13][0]]

                            self.write(json.dumps({"0":1,"1":self.result,"len":len(self.result["recv"])}))
                        else:
                            self.write(json.dumps({"0":0, "1":"此人未注册！！！"}))
                else:
                    self.write(json.dumps({"0":0,"1":"发送用户名不得为空！！！"}))

            # 获取全部信息
            elif self.ty==2 or self.ty=='2':

                res=con.rec_from_all_people()

                result={}
                result["recv"]=res[0:[len(res) if len(res)<13 else 13][0]]
                result["recv"]=[list(r) for r in result["recv"]]
                # print("recv:  ",result["recv"])
                self.write(json.dumps({"0":1,"1":result,"len":len(result["recv"])}))

            # 获取全部的用户名
            elif self.ty==3 or self.ty=='3':
                res=con.rec_all_username()

                self.write(json.dumps({"0":1,"1":res,"len":len(res)}))

            else:
                self.write(json.dumps({"0":0,"1":"发生错误！！！"}))

        except Exception as e:
            print(e)
            self.write('提交失败')

if __name__ == "__main__":

    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(8000)
    tornado.ioloop.IOLoop.current().start()