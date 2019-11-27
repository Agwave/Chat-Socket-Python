# 一、界面展示
 
## 主界面：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191127130811604.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQxODA1NTEx,size_16,color_FFFFFF,t_70)

## 注册界面：
![在这里插入图片描述](https://img-blog.csdnimg.cn/2019112713095498.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQxODA1NTEx,size_16,color_FFFFFF,t_70)

## 登录界面：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191127131027466.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQxODA1NTEx,size_16,color_FFFFFF,t_70)

# 二、使用方法
1. 导入需要的库，如PyQt5，pymysql等
2. 建立数据库 QcChat
3. 在QcChat内建立 users 表，表结构如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191127131403245.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQxODA1NTEx,size_16,color_FFFFFF,t_70)

4. 设置好connectMysql中参数
![在这里插入图片描述](https://img-blog.csdnimg.cn/20191127133847776.png)
6. 运行 object 里的 server.py
7. 运行 main.py 。注册、登录。
8. 运行 debug 里的 main1.py。注册、登录。
9. 两个用户便可以通信了。

附：如果想要在不同主机中通信，需要在同一个局域网或者连同一个路由（热点相连或连同一个wifi），并修改好server.py、client.py和connectMySQL.py中host地址。 
