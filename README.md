Ada
===

Ada运维管理平台

- 写在前言：
  - 本人某电商一名小小的运维开发工程师，喜欢交友，热爱技术 :)
  - 分享，学习，总结；
  - 代码很菜，分享出来，希望得到学习，只要你提我就肯花时间写。希望得到反馈，谢谢 ^_^
  - 算是对自动化运维一个小小总结，里面肯定有不完善的地方，希望可以得到交流，毕竟每人角度不一，观点也不一样。
  - 为什么是Ada呢? 因为女票的英文名^_^

- 平台部分截图
![主页](http://ou529e3sj.bkt.clouddn.com/ada-index.jpg)
![主页](http://ou529e3sj.bkt.clouddn.com/ada-resources.pic.jpg)
![主页](http://ou529e3sj.bkt.clouddn.com/ada-code_update.jpg)
![主页](http://ou529e3sj.bkt.clouddn.com/ada-product.pic.jpg)

- 部署
组件查看requirements.txt

- 我的开发环境: 172.16.18.88    

1. 启动服务是/opt/python2713:
```
(py2713) [root@zyl-node1 conf.d]# ps -ef|grep python|grep -v grep
root      29492  29491  0 Sep22 ?        00:00:00 /bin/bash -c /opt/py2713/bin/python /data/AMC/AMC.py >> /data/AMC/AMC_send.log
root      29493  29492  0 Sep22 ?        00:00:00 /opt/py2713/bin/python /data/AMC/AMC.py
root      39951      1  0 12:23 ?        00:00:00 /opt/py2713/bin/python /opt/py2713/bin/supervisord -c /etc/supervisor/supervisord.conf
root      39953  39951  3 12:23 ?        00:00:02 /opt/py3/bin/python manage.py celery worker --loglevel=info
root      39955  39951  1 12:23 ?        00:00:01 /opt/py3/bin/python manage.py runserver 0.0.0.0:8080
root      39969  39955  4 12:23 ?        00:00:03 /opt/py3/bin/python manage.py runserver 0.0.0.0:8080
root      39970  39953  0 12:23 ?        00:00:00 /opt/py3/bin/python manage.py celery worker --loglevel=info
```

2. 开发环境:  
```
[root@zyl-node1 conf.d]# cd /opt/py3
[root@zyl-node1 py3]# . ./bin/activate
(py3) [root@zyl-node1 py3]# which  python
/opt/py3/bin/python
(py3) [root@zyl-node1 py3]# python --version
Python 3.6.1
```
