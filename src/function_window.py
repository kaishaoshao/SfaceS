# coding:utf-8
'''
人脸显示设置
'''
import base64

import cv2
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from src.cameraVideo import camera
from src.detect import detect_thread
from view.mainWindow import Ui_mainwindow
from PyQt5.QtWidgets import QWidget,QMessageBox,QInputDialog

from qfluentwidgets import StateToolTip
class function_window(QWidget,Ui_mainwindow):
    #初始化
    def __init__(self):
        super(function_window,self).__init__()
        self.setupUi(self)
        self.sign_pressed = False
        self.lab_cap.setScaledContents(True)                # 设置图片自适应大小
        self.btn_sign.clicked.connect(self.open_sign_in)    # 打开签到
        self.btn_sign.clicked.connect(self.onButtonClicked)
        self.btn_close.clicked.connect(self.close_sign_in)  # 关闭签到
        self.btn_close.clicked.connect(self.onButtonClicked)
        self.access_token = self.get_accessToken()          # 调用api
        self.start_state = True
        self.stateTooltip = None
    #打开签到
    def open_sign_in(self):
        if self.start_state == True:
            #启动摄像头
            self.cameraVideo = camera()
            #启动定时器，获取摄像头刷新
            self.timeshow = QTimer(self)
            self.timeshow.start(10)
            #每隔10ms刷新一次
            self.timeshow.timeout.connect(self.show_cameradata)

            self.detect = detect_thread(self.access_token) # 创建线程
            self.detect.start() # 启动线程

            #签到500ms获取一次，用来获取检测画面
            self.faceshow = QTimer(self)
            self.faceshow.start(500)
            self.faceshow.timeout.connect(self.get_camera_data)
            self.detect.transmit_data.connect(self.get_data)
            self.detect.transmit_data1.connect(self.get_search_data)
            self.start_state = False
        else:
            QMessageBox.about(self,"提示","正在检测，请关闭")


    # #关闭签到
    def close_sign_in(self):
        if  self.start_state == False:
            self.start_state = True  # 签到关闭
            self.faceshow.stop()  # 计时器停止
            self.detect.ok = False  # 停止run
            self.detect.quit()  # 关闭线程
            # 关闭定时器
            self.timeshow.stop()
            self.timeshow.timeout.disconnect(self.show_cameradata)
            # 关闭摄像头
            self.cameraVideo.colse_camera()
            # 判断定时器是否关闭，则显示为自己设定的图像
            if self.timeshow.isActive() == False:
                self.lab_cap.setPixmap(QPixmap("../resource/images/logo.png"))
                self.tex_check_message.clear()
            else:
                QMessageBox.warning(self, "提示", "关闭失败")

            if self.faceshow.isActive() == True:
                QMessageBox.warning(self, "警告", "关闭run失败")
            else:
               pass
        else:
            QMessageBox.warning(self, "警告", "没有签到")
            # return self.sign_pressed


    # 摄像头数据显示
    def show_cameradata(self):
        # 获取摄像头数据
        pic = self.cameraVideo.camera_to_pic()
        # 在Bodylabel中显示画面
        self.lab_cap.setPixmap(pic)

    # 获取图像，并转换为base64格式
    def get_camera_data(self):
        camera_data1 = self.cameraVideo.read_cameraData()
        # 把摄像头画面转化为一张图片，然后设置编码为base64编码
        _,encode = cv2.imencode('.jpg',camera_data1)
        base64_image = base64.b64encode(encode.tobytes())
        # print("get_camera_data\n")
        self.detect.get_imge_data(base64_image)


    # 获取人脸检测数据并显示到文本框中
    def get_data(self,data):
        if data['error_code'] != 0:
            self.tex_check_message.setPlainText(data['error_msg'])
            print("test")
            return
        elif data['error_msg'] == 'SUCCESS':
            # self.tex_check_message.clear()
            # 在data字典中键为result对应的值才是返回的检测结果
            face_num = data['result']['face_num']
            print(face_num)
            if face_num == 0:
                self.tex_check_message.setPlainText("当前没有人或人脸出现！\n")
                return
            else:
                self.tex_check_message.clear()
                self.tex_check_message.insertPlainText("检测到人脸！\n")
                self.tex_check_message.insertPlainText("——————————————\n")
            # 人脸信息获取['result']['face_list']是列表，每个数据就是一个人脸信息，需要取出每个列表信息（0-i）
            for i in range(face_num):
                age = data['result']['face_list'][i]['age']  # 年龄
                # print(age)
                beauty = data['result']['face_list'][i]['beauty']  # 美观度
                gender = data['result']['face_list'][i]['gender']['type']  # 性别
                expression = data['result']['face_list'][i]['expression']['type']
                face_shape = data['result']['face_list'][i]['face_shape']['type']  # 脸型
                glasses = data['result']['face_list'][i]['glasses']['type']  # 是否戴眼镜
                emotion = data['result']['face_list'][i]['emotion']['type']  # 情绪
                mask = data['result']['face_list'][i]['mask']['type']  # 是否戴口罩
                # 往窗口中添加文本，参数就是需要的文本信息
                # print(age,gender,expression,beauty,face_shape,emotion,glasses,mask)
                self.tex_check_message.insertPlainText("第" + str(i + 1) + "个学生人脸信息:\n")
                self.tex_check_message.insertPlainText("——————————————\n")
                self.tex_check_message.insertPlainText("年龄:" + str(age) + "\n")
                if gender == 'male':
                    gender = "男"
                else:
                    gender = "女"
                self.tex_check_message.insertPlainText("性别:" + str(gender) + "\n")
                self.tex_check_message.insertPlainText("表情:" + str(expression) + "\n")
                self.tex_check_message.insertPlainText("颜值分数:" + str(beauty) + "\n")
                self.tex_check_message.insertPlainText("脸型:" + str(face_shape) + "\n")
                self.tex_check_message.insertPlainText("情绪:" + str(emotion) + "\n")
                if glasses == "none":
                    glasses = "否"
                elif glasses == "common":
                    glasses = "是:普通眼镜"
                else:
                    glasses = "是:太阳镜"
                self.tex_check_message.insertPlainText("是否佩戴眼镜:" + str(glasses) + "\n")
                if mask == 0:
                    mask = "否"
                else:
                    mask = "是"
                self.tex_check_message.insertPlainText("是否佩戴口罩:" + str(mask) + "\n")
                self.tex_check_message.insertPlainText("——————————————\n")
        else:
            print("人脸获取失败\n")


    def get_accessToken(self):
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

    # 查找人脸数据
    def get_search_data(self,data):
        self.tex_sign_message.setPlainText(data)

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

    # 班级查询
    def get_class(self):
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/getlist"
        params = {
            "start": 0,
            "length": 100
        }
        access_token = self.access_token
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            return response.json()

    # 将查询结果显示在MessageBox中
    def display_class(self):
        list = self.get_class()
        str = ''
        for i in list['result']['group_id_list']:
            str = str + '\n' + i
        QMessageBox.about(self, "班级列表", str)

    # 班级删除
    def delete_class(self):
        # 打开输入框，进行输入用户组
        list = self.get_class()  # 首先获取用户组信息
        group, ret = QInputDialog.getText(self, "存在的班级", "班级信息" + str(list['result']['group_id_list']))
        if group == "":
            print("取消删除班级")
        else:
            request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/delete"

            params = {
                "group_id": group  # 要删除用户组的id
            }
            access_token = self.access_token
            request_url = request_url + "?access_token=" + access_token
            headers = {'content-type': 'application/json'}
            response = requests.post(request_url, data=params, headers=headers)
            if response:
                print(response.json())
                message = response.json()
                if message['error_code'] == 0:
                    QMessageBox.about(self, "班级删除结果", "班级删除成功")
                else:
                    QMessageBox.about(self, "班级删除结果", "班级删除失败")


    def onButtonClicked(self):
        if self.stateTooltip:
            self.stateTooltip.setContent('签到关闭啦 😆')
            self.stateTooltip.setState(True)
            self.stateTooltip = None
        else:
            self.stateTooltip = StateToolTip('正在签到', '同学请耐心等待哦~~', self)
            self.stateTooltip.move(510, 30)
            self.stateTooltip.show()
