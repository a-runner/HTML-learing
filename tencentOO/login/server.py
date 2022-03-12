#!/root/Anaconda3/envs/py36/bin python
# -*- coding: utf-8 -*-
# @Time : 2021/5/6 15:28
# @Author : a-runner
# @Site : 
# @File : server.py
# @Software: PyCharm
import tornado.ioloop
import tornado.web
import pymysql
import json
import tornado.options
import requests
import base64
import matplotlib.pyplot as plt
import jieba
import wordcloud
import paddlehub as hub
import cv2
import json
import time

headers = {
    'Content - Type': 'application/json'
}
host = 'https://aip.baidubce.com/oauth/2.0/token?'

tokendata = {
        'grant_type': 'client_credentials',
        'client_id': 'aRBU2gfaqGtVCoFcFKTlcHyX',
        'client_secret': 'dqNz3WjKi36PyQ2bp3cbIZBTWlMN0UY8'
}

# 获取AccessToken
# host = host + urlencode(tokendata)
access_token = requests.post(host, data=tokendata).json()['access_token']
# 对图片颜值 beauty进行获取
url = 'https://aip.baidubce.com/rest/2.0/face/v3/detect?access_token={}'.format(access_token)
# 构造请求参数

data = {
    'image': '',
    'image_type': 'BASE64',
    'face_field': 'beauty'
}

# 建立一个数据库得类
# login register共用
class Mysql_write():
    def __init__(self,user,password,phone=None):
        try:
            self.con = pymysql.connect('localhost', 'root', 'root123', 'tencentoo', charset='utf8')
            self.user = user
            self.password = password
            self.phoneNum=phone
        except Exception as e:
            print(e)
            print('数据库连接失败！！')

    def insert_data(self):
        cursor = self.con.cursor()
        print('执行操作：{}'.format('insert into login values("{}", "{}");'.format(self.user, self.password)))
        cursor.execute('insert into login values("{}", "{}");'.format(self.user, self.password))
        self.con.commit()

    # 供register.html调用
    def insert_dataR(self):
        cursor = self.con.cursor()
        sql='select * from login where phoneNum="{}";'.format(self.phoneNum)
        cursor.execute(sql)
        result=cursor.fetchall()
        print(result)
        if not result:
            print('执行操作：{}'.format('insert into login values("{}","{}", "{}");'.format(self.user, self.password,self.phoneNum)))
            cursor.execute('insert into login values("{}","{}", "{}");'.format(self.user, self.password,self.phoneNum))
            self.con.commit()
            self.con.close()
            return 1
        else:
            print("该手机号已注册")
            return 0

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

# 建立一个 new database
class Mysql_write_contact():
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
        rrr = []

        for i in range(len(re)):
            sql = r'select * from {} where recver="{}";'.format(re[i][0],self.user)
            print(sql)
            cursor.execute(sql)
            rr=cursor.fetchall()
            rr=list(rr)
            rr.reverse()

            sql=r'select * from {} where recver="{}";'.format(self.user,re[i][0])
            print(sql)
            cursor.execute(sql)
            rre = cursor.fetchall()
            rre = list(rre)
            rre.reverse()

            # print(rr)
            rra=rr[0:[len(rr) if len(rr)<13 else 13][0]]
            rree=rre[0:[len(rre) if len(rre)<13 else 13][0]]

            # print("rra:   ",rra)
            for i in range(len(rra)):
                rree.append(rra[i])
            # print("result: ",result)

            print("result_all_people back:",rree)

            for i in rree:
                rrr.append(i)


        index=sorted(range(len(rrr)), key=lambda k: rrr[k][4], reverse=False)

        result=[]
        for i in index[0:[len(index) if len(index)<13 else 13][0]]:
            result.append(rrr[i])

        print("result_last:  ",result)
        return result


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
        cursor.execute(sql)
        self.con.commit()
        result=cursor.fetchall()
        res = []

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
        cursor.execute(sql)
        result = cursor.fetchall()
        print("lalal:",result)
        self.con.commit()
        if not result[0]:
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
            print()
            datatime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            sql='insert into {} values("{}", "{}","{}","{}","{}")'.format(self.user,self.user, sendName,message,0,datatime)
            cursor.execute(sql)
            self.con.commit()


    def check_name(self,recName):
        cursor = self.con.cursor()
        sql1 = 'SHOW TABLES LIKE "{}";'.format(recName)
        cursor.execute(sql1)
        re = cursor.fetchall()

        return re


class LoginIner(tornado.web.RequestHandler):

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


class Register(tornado.web.RequestHandler):

    def get(self):
        self.render("register.html")

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header(
            "Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE"
        )

    def post(self, *args, **kwargs):
        self.user=self.get_argument("user")
        self.pwd=self.get_argument("pwd")
        self.phone = self.get_argument("phone")

        con = Mysql_write(self.get_argument("user"), self.get_argument('pwd'),self.phone)
        rr=con.insert_dataR()
        if rr:
            self.write(json.dumps({"0":1,"1":"提交成功"}))
        else:
            self.write(json.dumps({"0":0,"1":"该手机号已经注册！"}))


class Beautyer(tornado.web.RequestHandler):
    def get(self):
        self.render("../beautyLevel/beauty.html")

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
            file_name="../image/颜值排行/"+file_name
            with open(file_name, 'wb') as up:
                up.write(meta['body'])
            up.close()
            f=open(file_name,'rb')
            data['image'] = base64.b64encode(f.read())
            # data['image'] = f.read()
            response = requests.post(url, headers=headers, data=data)
            beauty = response.json()['result']['face_list'][0]['beauty']
            # beauty :38
            f.close()
            # returnData={"beauty":beauty}
            print(beauty)
            # self.write(json.dumps(returnData))
            self.write(str(beauty))
            # self.write("hello")
            # self.write(str.encode(str(beauty)))


# contact  Mysql_write_contact
class Contacter(tornado.web.RequestHandler):

    def get(self):
        self.render("../contact/interaction.html")


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


        self.ty=self.get_argument("ty")

        con = Mysql_write_contact(self.get_argument("user"))
        # 检查数据库中是否存在该用户名
        try:
            if self.ty==1 or self.ty=='1':

                result = con.check_name(self.recver)
                print("查找：",result)
                if result[0]:
                    if self.message:
                        print("进入：")
                        con.insert_data(self.recver,self.message)
                        print("rec——data")
                        # self.write([1,"操作成功"])
                        rres=con.rec_data(self.recver)
                        print("rres:"+ str(rres))
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


# 实时翻译
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
    w = wordcloud.WordCloud(width=490,
                            height=600,
                            background_color='black',
                            font_path='SIMKAI.TTF')

    # 调用jieba的lcut()方法对原始文本进行中文分词，得到string
    # txt = '同济大学（Tongji University），简称“同济”，是中华人民共和国教育部直属，由教育部、国家海洋局和上海市共建的全国重点大学，历史悠久、声誉卓著，是国家“双一流”、“211工程”、“985工程”重点建设高校，也是收生标准最严格的中国大学之一'
    print("词云图内容：",txt)
    # txtlist = jieba.lcut(txt)
    # string = " ".join(txtlist)

    # print("string:",string)
    # 将string变量传入w的generate()方法，给词云输入文字
    w.generate(txt)

    # 将词云图片导出到当前文件夹
    print("../translate/cloud/"+user+".png")

    w.to_file("../translate/cloud/"+user+".png")



# 建立一个 new database
class Mysql_write_trans():
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

        if re:
            # 查找表中所有的字段
            sql="select * from {}".format(self.user)
            cursor.execute(sql)
            self.con.commit()
            result = cursor.fetchall()
            txt=''
            for a in result:
                txt=txt+a[0]+r' '

            return txt
        else:
            # 创建名为self.user 的表
            sql = r'CREATE TABLE {} ( ' \
                  r'filed varchar(20) NOT NULL);'.format({self.user})
            # ENGINE = InnoDB
            # AUTO_INCREMENT = 1
            cursor.execute(sql)
            self.con.commit()

            return ''

    def addWord(self,text):
        cursor = self.con.cursor()
        sql1 = 'SHOW TABLES LIKE "{}";'.format(self.user)
        cursor.execute(sql1)
        self.con.commit()
        re = cursor.fetchall()
        # print(re)
        if not re:
            # 创建名为self.user 的表
            sql = r'CREATE TABLE {} ( ' \
                  r'filed varchar(20) NOT NULL);'.format(self.user)
            # ENGINE = InnoDB
            # AUTO_INCREMENT = 1
            cursor.execute(sql)
            self.con.commit()

        # 首先查找表中是否有这个字段
        sql='select * from {} where filed="{}";'.format(self.user,text)
        cursor.execute(sql)
        result=cursor.fetchall()
        if not result:
            # 执行添加
            sql='INSERT INTO {} VALUES("{}")'.format(self.user,text)
            cursor.execute(sql.encode('utf8'))
            # cursor.execute(sql)
            self.con.commit()
            print(self.user, "---tranlate：添加", text)
            return self.get_text()
        else:
            return self.get_text()

    def delWord(self,text):
        cursor = self.con.cursor()
        sql1 = 'SHOW TABLES LIKE "{}";'.format(self.user)
        cursor.execute(sql1)
        re = cursor.fetchall()
        if not re:
            # 创建名为self.user 的表
            sql = r'CREATE TABLE {} ( ' \
                  r'filed varchar(20) NOT NULL);'.format(self.user)
            # ENGINE = InnoDB
            # AUTO_INCREMENT = 1
            cursor.execute(sql)
            self.con.commit()

        # 首先查找表中是否有这个字段
        sql = 'select * from {} where filed="{}";'.format(self.user,text)
        cursor.execute(sql)
        self.con.commit()
        result = cursor.fetchall()
        if result:
            # 执行添加
            sql = 'DELETE FROM {} WHERE filed="{}";'.format(self.user, text)
            cursor.execute(sql)
            self.con.commit()
            print(self.user,"---tranlate：删除",text)

            return self.get_text()
        else:
            return self.get_text()

class Translationer(tornado.web.RequestHandler):

    def get(self):
        self.render("../translate/trans.html")

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
        con = Mysql_write_trans(self.get_argument("user"))

        try:
            if self.ty==0 or self.ty=="0":
                result=get_main(self.mess)
                self.write(json.dumps({"0": 1, "1": result}))
            elif self.ty==1 or self.ty=='1':
                # con = Mysql_write(self.get_argument("user"))
                txt=con.get_text()
                if txt:
                    # 根据text生成词云图
                    word_cloud(txt,self.user)
                    self.write(json.dumps({"0": 1, "1": "../translate/cloud/"+self.user+".png"}))
                else:
                    self.write(json.dumps({"0": 0, "1": "未输入过数据"}))
            elif self.ty==2 or self.ty=='2':
                txt=con.addWord(self.text)
                self.write(json.dumps({"0": 1, "1": txt}))
            elif self.ty==3 or self.ty=='3':
                txt=con.delWord(self.text)
                self.write(json.dumps({"0": 1, "1": txt}))
            elif self.ty==4 or self.ty=='4':
                self.write(json.dumps({"0": 1, "1": con.get_text()}))
            else:
                self.write(json.dumps({"0":0,"1":"ty类型错误"}))
        except Exception as e:
            print(e)
            self.write(json.dumps({"0": 0, "1": "try错误"}))


class AnimalDetect(tornado.web.RequestHandler):
    def get(self):
        self.render("../animalDetect/animal.html")

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
            (key, value), = results[0].items()
            print("category:",key)
            print("score:",value)
            if results:
                self.write(json.dumps({'0':key,'1':round(value*100,2)}))
            else:
                self.write(json.dumps({'0':'','1':''}))


# 建立一个数据库得类
class Mysql_Question():
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
        search_counts =cursor.execute('select * from question where user="{}";'.format(self.user))
        # 获得该用户的密码
        result=cursor.fetchall()
        print(result)
        if result:
            return [1,self.user]
        else:
            return [0,0]


# 问卷调查
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
        con = Mysql_Question(self.user,self.age,self.tele,self.ocup,self.education,self.use,self.how,self.app)
        # 检查数据库中是否存在该用户名
        try:
            result = con.check_phone()
            print(result)
            if not result[0]:
                print("准备插入数据")
                con.insert_data()
                self.write(json.dumps(['%s %s' % (self.user,'提交成功')]))
            else:
                self.write(json.dumps([result[1],"不能重复提交！！！"]))

        except Exception as e:
            print(e)
            self.write(json.dumps([0,'出现错误！！！']))


if __name__ == "__main__":

    application = tornado.web.Application([
        (r"/login", LoginIner),
        (r'/register',Register),
        (r'/beautyLevel',Beautyer),
        (r'/interaction',Contacter),
        (r'/translate',Translationer),
        (r'/animalDetect',AnimalDetect),
        (r'/questionnaire',QuestionHandler),

    ])
    application.listen(8800)
    tornado.ioloop.IOLoop.current().start()