# coding:utf-8

import requests

from src.detect import detect_thread
from view.message import Ui_FocusInterface
from PyQt5.QtWidgets import QWidget, QMessageBox, QInputDialog
from src.function_window import function_window

class message_window(QWidget, Ui_FocusInterface):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.access_token = self.get_accessToken1()          # 获取Access_token访问令牌，并复制为全局变量
        self.btn_addclass.clicked.connect(self.add_class)


    def get_accessToken1(self):
        #client_id为官网获取的AK,client为SK
        host = "https://aip.baidubce.com/oauth/2.0/token?client_id=epOt70CmIb4G5peBkwoWGfHB&client_secret=Gb4UcedWUGwepjbYGyc9NAA1gGPYBwc7&grant_type=client_credentials"
        #进行网络请求，使用getg函数
        response = requests.get(host)
        if response:
            data = response.json()
            self.access_token = data['access_token']
            return self.access_token
        else:
            QMessageBox(self,"提示，请检查网络链接")

    # 添加班级
    def add_class(self):
        # 打开输入框，进行输入用户组
        group, ret = QInputDialog.getText(self, "添加班级", "请输入班级名称(由数字、字母、下划线组成)")
        if group == "":
            print("取消添加班级")
        else:
            request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/add"

            params = {
                "group_id": group
            }
            access_token = self.access_token
            request_url = request_url + "?access_token=" + access_token
            headers = {'content-type': 'application/json'}
            response = requests.post(request_url, data=params, headers=headers)
            if response:
                print(response.json())
                message = response.json()
                if message['error_code'] == 0:  # 根据规则，返回0则为班级添加成功
                    QMessageBox.about(self, "班级创建结果", "班级创建成功")
                else:
                    QMessageBox.about(self, "班级创建结果", "班级创建失败")

 #班级查询
    def get_class(self):
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/getlist"
        params = {
            "start":0,
            "length":100
        }
        access_token = self.access_token
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            return response.json()
    #将查询到的结果显示在MessageBOX框上面
    def display_class(self):
        list=self.get_class()
        str=''
        for i in list['result']['group_id_list']:
            str=str+'\n'+i
        QMessageBox.about(self,"班级列表",str)

    #班级删除
    def delete_calss(self):
        #打开输入框，进行输入用户组
        list = self.get_class()#首先获取用户组信息
        group,ret=QInputDialog.getText(self, "存在的用户组", "用户组信息"+str(list['result']['group_id_list']))
        if group == "":
            print("取消删除用户组")
        else:
            request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/delete"

            params = {
                "group_id": group#要删除用户组的id
            }
            access_token = self.access_token
            request_url = request_url + "?access_token=" + access_token
            headers = {'content-type': 'application/json'}
            response = requests.post(request_url, data=params, headers=headers)
            if response:
                print(response.json())
                message = response.json()
                if message['error_code'] == 0:
                    QMessageBox.about(self, "用户删除结果", "用户删除成功")
                else:
                    QMessageBox.about(self, "用户删除结果", "用户删除失败")
