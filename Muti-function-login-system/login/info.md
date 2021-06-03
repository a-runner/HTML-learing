# 展示login的作用

**本文件负责登录，注册及主菜单的显示**

## login_in.html
 * 注册的电话号
 * 注册时的密码
 * **忘记密码** 目前未设置跳转页面
![image](https://user-images.githubusercontent.com/49384694/120595137-84e85080-c474-11eb-9d99-ab68fe7c4b90.png)


## register.html
  注册时的信息包括：
  * 用户名
  * 密码
  * 手机号（个人课设的原因无法获取短信验证码服务），验证码采用本地生成
![image](https://user-images.githubusercontent.com/49384694/120595347-caa51900-c474-11eb-9daf-5c1dc66b58da.png)

## mean.html
  输入正确的电话号于密码，会跳转到mean.html
  ![image](https://user-images.githubusercontent.com/49384694/120595617-43a47080-c475-11eb-8cdb-715524e7581c.png)

 mean菜单目前大致包括以下功能：
 * 口罩检测（百度飞桨接口）
 * 颜值评分（百度AI的API）
 * 在线实时聊天系统（目前只完成了文字的发送）
 * 新年祝福（单纯的html+JS编写）
 * 字典及词云图的生成（调用有道词典的API完成翻译功能）

**缺点**：
* 只能承受小部分流量（单纯的采用后端处理数据并读取存放进入数据库），并不能适合大规模使用（纯属完成课设要求）
 ![image](https://user-images.githubusercontent.com/49384694/120595711-6898e380-c475-11eb-8897-3bee30e9aeff.png)
