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


#增加学生信息
    def add_student(self):
        '''
        人脸注册
        '''
        list=self.get_class()#获取班级，将班级信息传递到我们新建的界面之中
        # 创建一个窗口，进行用户信息录入
        window = add_student_window(list['result']['group_id_list'],self)#将获取到的班级传递到新的界面，后续有用
        #新创建窗口，通过exec()函数一直在执行，窗口不进行关闭
        window_status=window.exec_()
        #判断
        if window_status !=1:
            return
        base64_image = window.base64_image
        # 参数请求中，需要获取人脸编码，添加的组的id,添加的用户，新用户id信息
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add"

        params = {
            "image": base64_image,  # 人脸图片
            "image_type": "BASE64",  # 图片编码格式
            "group_id": window.class_id,  # 班级名称
            "user_id": window.student_id,  # 学生学号
            "user_info": window.student_name# 学生姓名
        }
        access_token = self.access_token
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            data = response.json()
            if data['error_code'] == 0:
                QMessageBox.about(self, "增加结果", "学生增加成功！")
            else:
                QMessageBox.about(self, "增加结果", "学生增加失败！")


    def show_camera(self):
        # 获取摄像头数据
        pic = self.cameravideo.camera_to_pic()#获取一帧图像
        # 显示数据、显示画面
        self.label.setPixmap(pic)

    def get_cameradata(self):
        camera_data1 = self.cameravideo.read_camera()
        # 把摄像头画面转化为一张图片，然后设置编码为base64编码
        _, enc = cv2.imencode('.jpg', camera_data1)
        base64_image = base64.b64encode(enc.tobytes())
        self.base64_image=base64_image#全局变量，用于保存画面base64格式画面
        self.time.stop()#计时器停止
        self.cameravideo.colse_camera()#摄像机关闭

    def show_class(self):
        self.comboBox.clear()
        for i in self.list:
            self.comboBox.addItem(i)#将获取到的班级列表显示在下拉框中

    
       #获取学生基本信息
    def get_student_data(self):
        self.class_id=self.comboBox.currentText()#获取班级
        self.student_id=self.lineEdit.text()#获取学号
        self.student_name=self.lineEdit_2.text()#获取姓名
        self.accept()#点击确认后关闭对话框
    #关闭窗口
    def close_window(self):
        #关闭对话框
        self.close()



