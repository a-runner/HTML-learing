#!/root/Anaconda3/envs/py36/bin python
# -*- coding: utf-8 -*-
# @Time : 2021/6/1 15:39
# @Author : a-runner
# @Site : 
# @File : translate.py
# @Software: PyCharm
import tornado.ioloop
import tornado.web
import json
import pymysql
# 导入需要的包
import pandas as pd
import numpy as np
import requests
import jieba
import wordcloud
import json



def translate(word):
    # 有道词典 api
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    # 传输的参数，其中 i 为需要翻译的内容
    key = {
        'type': "AUTO",
        'i': word,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true"
    }
    # key 这个字典为发送给有道词典服务器的内容
    response = requests.post(url, data=key)
    # 判断服务器是否相应成功
    if response.status_code == 200:
        # 然后相应的结果
        return response.text
    else:
        print("有道词典调用失败")
        # 相应失败就返回空
        return None


def get_main(word):
    list_trans = translate(word)
    result = json.loads(list_trans)
    result = result['translateResult'][0][0]['tgt']
    print(word,'----',result)
    return result


def word_cloud(txt,user):
    # 构建并配置词云对象w
    w = wordcloud.WordCloud(width=1000,
                            height=700,
                            background_color='white',
                            font_path='msyh.ttc')

    # 调用jieba的lcut()方法对原始文本进行中文分词，得到string
    # txt = '同济大学（Tongji University），简称“同济”，是中华人民共和国教育部直属，由教育部、国家海洋局和上海市共建的全国重点大学，历史悠久、声誉卓著，是国家“双一流”、“211工程”、“985工程”重点建设高校，也是收生标准最严格的中国大学之一'
    txtlist = jieba.lcut(txt)
    string = " ".join(txtlist)

    # 将string变量传入w的generate()方法，给词云输入文字
    w.generate(string)

    # 将词云图片导出到当前文件夹
    w.to_file("./cloud/"+user+'.png')


# 建立一个 new database
class Mysql_write():
    def __init__(self,user):
        try:
            self.con = pymysql.connect('localhost', 'root', 'root123', 'wordcloud', charset='utf8')
            self.user = user
            # self.password = password
        except Exception as e:
            print(e)
            print('数据库连接失败！！')

    def get_text(self):
        # 查看表，如果没有这个表就新创建

        cursor = self.con.cursor()
        sql1 = 'SHOW TABLES LIKE "{}";'.format(self.user)
        cursor.execute(sql1)
        re = cursor.fetchall()

        if re[0]:
            # 查找表中所有的字段
            sql="select * from {}".format(self.user)
            cursor.execute(sql)
            self.con.commit()
            result = cursor.fetchall()
            txt=''
            for a in result:
                txt=txt+a["filed"]+r' '

            return txt
        else:
            # 创建名为self.user 的表
            sql = r'CREATE TABLE {} ( ' \
                  r'filed varchar(20) NOT NULL;'.format({self.user})
            # ENGINE = InnoDB
            # AUTO_INCREMENT = 1
            cursor.execute(sql)
            self.con.commit()

            return None

    def addWord(self,text):
        cursor = self.con.cursor()
        sql1 = 'SHOW TABLES LIKE "{}";'.format(self.user)
        cursor.execute(sql1)
        re = cursor.fetchall()
        if re[0]:
            # 首先查找表中是否有这个字段
            sql='select * from {} where filed="{}";'.format(self.user,text)
            result=cursor.fetchall()
            if result[0]:
                # 执行添加
                sql='INSERT INTO {} VALUES("{}")'.format(self.user,text)
                cursor.execute(sql.encode('utf8'))
                cursor.execute()
                self.con.commit()

                return self.get_text()

        else:
            return None

    def delWord(self,text):
        cursor = self.con.cursor()
        sql1 = 'SHOW TABLES LIKE "{}";'.format(self.user)
        cursor.execute(sql1)
        re = cursor.fetchall()
        if re[0]:
            # 首先查找表中是否有这个字段
            sql = 'select * from {} where filed="{}";'.format(self.user,text)
            result = cursor.fetchall()
            if result[0]:
                # 执行添加
                sql = 'DELETE FROM {} WHERE filed="{}"'.format(self.user, text)
                cursor.execute()
                self.con.commit()

                return self.get_text()
        else:
            return None


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
        self.mess=self.get_argument('message')
        self.ty=self.get_argument('ty')
        self.text=self.get_argument('info')
        con = Mysql_write(self.get_argument("user"))

        if self.ty==0 or self.ty=="0":
            result=get_main(self.mess)
            return self.write(json.dumps({"0": 0, "1": result}))
        elif self.ty==1 or self.ty=='1':
            # con = Mysql_write(self.get_argument("user"))
            txt=con.get_text()
            if txt:
                # 根据text生成词云图
                word_cloud(txt,self.user)
                return self.write(json.dumps({"0": 1, "1": "./cloud/"+self.user+".png"}))
            else:
                return self.write(json.dumps({"0": 0, "1": "未输入过数据"}))
        elif self.ty==2 or self.ty=='2':
            txt=con.addWord(self.text)
            return self.write(json.dumps({"0": 1, "1": txt}))
        elif self.ty==3 or self.ty=='3':
            txt=con.delWord(self.text)
            return self.write(json.dumps({"0": 1, "1": txt}))
        else:
            return self.write(json.dumps({"0":0,"1":"ty类型错误"}))



if __name__ == "__main__":

    application = tornado.web.Application([
        (r"/translate", MainHandler),
    ])
    application.listen(8800)
    tornado.ioloop.IOLoop.current().start()