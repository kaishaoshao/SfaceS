# SfaceS

## 介绍

SfaceS是一个pc端的学生课堂签到系统，基于百度智能云人脸识别，采用python语言编写程序，使用pyqt搭建框架，并且借助fluent自定义控件设计界面。作为本科毕业设计，使用MIT授权

## 使用方法

### 下载

```
git clone https://github.com/kaishaoshao/SfaceS.git
```



### 下载依赖

```bash
#以下操作是ubuntu环境，windows环境可以使用wsl或者pycharm(除了换源，其他操作都可以使用)
#永久换源----清华源(看自己)
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

#豆瓣：http://pypi.douban.com/simple/
#阿里云：http://mirrors.aliyun.com/pypi/simple/
#华为云：https://repo.huaweicloud.com/repository/pypi/simple
#中科大：https://pypi.mirrors.ustc.edu.cn/simple/

#注：临时换源只需要在后面+上就可以了
pip install pyuic5 -i https://pypi.mirrors.ustc.edu.cn/simple/


#numpy：计算
#opencv-python：摄像头读取
#pyqt5：图形界面相关库使用
#pyqt5-tools：图形界面设计
#pyuic5：界面设计文件ui转python文件py工具
#requests：发出网络请求

#下载
pip install numpy
pip install opencv-python
pip install pyqt5
pip install pyqt5-tools
pip install pyuic5     -->安装可能有问题
pip install requests

```











