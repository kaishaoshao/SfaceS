# coding:utf-8
'''
人脸显示设置
'''
import base64

import cv2
import requests
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget,QMessageBox
from cameraVideo import camera
from PyQt5.QtGui import QIcon,QPixmap
from view.mainWindow import Ui_mainwindow
from qfluentwidgets import SplitFluentWindow,FluentIcon,NavigationItemPosition,NavigationAvatarWidget
from detect import detect_thread

class Main(SplitFluentWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SfaceS")
        self.setWindowIcon(QIcon('./resource/images/logo.png'))
        self.setMinimumSize(700,600)
        #添加子界面
        self.mainWindow = function_window()
        #添加侧边栏Icon
        self.addSubInterface(self.mainWindow,FluentIcon.RINGER,"签到界面")


        #添加其他导航项
        self.navigationInterface.addWidget(
            routeKey = 'avatar',
            widget = NavigationAvatarWidget('用户','./resource/images/logo.png'),
            position=NavigationItemPosition.BOTTOM
        )

        self.navigationInterface.addItem(
            routeKey = 'setting',
            icon = FluentIcon.SETTING,
            text = '设置',
            position=NavigationItemPosition.BOTTOM
        )



class function_window(QWidget,Ui_mainwindow):
    
    #初始化
    def __init__(self):
        super(function_window,self).__init__()
        self.setupUi(self)

        self.sign_pressed = False

        self.lab_cap.setScaledContents(True)                #设置图片自适应大小
        self.btn_sign.clicked.connect(self.open_sign_in)
        self.btn_close.clicked.connect(self.close_sign_in)
        self.access_token = self.get_accessToken()

        self.start_state = True
    #打开签到
    def open_sign_in(self):
        if self.start_state == True:

            #启动摄像头
            self.cameraVideo = camera()
            #启动定时器，获取摄像头刷新
            self.timeshow = QTimer(self)
            self.timeshow.start(10)
            #每隔10ms刷新一次
            print("1\n")
            self.timeshow.timeout.connect(self.show_cameradata)
            print("2\n")
            self.detect = detect_thread(self.access_token) # 创建线程
            print("3\n")
            self.detect.start() # 启动线程
            #签到500ms获取一次，用来获取检测画面
            self.faceshow = QTimer(self)
            self.faceshow.start(500)
            print("4\n")
            self.faceshow.timeout.connect(self.get_camera_data)
            print("5\n")
            self.detect.transmit_data.connect(self.get_data)
            print("6\n")
            self.start_state = False
            self.sign_pressed = True
        else:
            QMessageBox.about(self,"提示","正在检测，请关闭")


    # 获取图像，并转换为base64格式
    def get_camera_data(self):
        camera_data1 = self.cameraVideo.read_cameraData()
        # 把摄像头画面转化为一张图片，然后设置编码为base64编码
        _,encode = cv2.imencode('.jpg',camera_data1)
        base64_image = base64.b64encode(encode.tobytes())
        # print("get_camera_data\n")
        self.detect.get_imge_data(base64_image)


    # 获取人脸检测数据并显示到文本框中
    def get_data(self, data):
        if data['error_code'] != 0:
            self.tex_check_message.setPlainText(data['error_msg'])
            return
        elif data['error_msg'] == 'SUCCESS':
            self.tex_check_message.clear()
            # 在data字典中键为result对应的值才是返回的检测结果
            face_num = data['result']['face_num']
            # print(face_num)
            if face_num == 0:
                self.tex_check_message.setPlainText("当前没有人或人脸出现！")
                return
            else:
                self.tex_check_message.clear()
                self.tex_check_message.appendPlainText("检测到人脸！")
                self.tex_check_message.appendPlainText("——————————————")
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
                self.tex_check_message.appendPlainText("第" + str(i + 1) + "个学生人脸信息:")
                self.tex_check_message.appendPlainText("——————————————")
                self.tex_check_message.appendPlainText("年龄:" + str(age))
                if gender == 'male':
                    gender = "男"
                else:
                    gender = "女"
                self.tex_check_message.appendPlainText("性别:" + str(gender))
                self.tex_check_message.appendPlainText("表情:" + str(expression))
                self.tex_check_message.appendPlainText("颜值分数:" + str(beauty))
                self.tex_check_message.appendPlainText("脸型:" + str(face_shape))
                self.tex_check_message.appendPlainText("情绪:" + str(emotion))
                if glasses == "none":
                    glasses = "否"
                elif glasses == "common":
                    glasses = "是:普通眼镜"
                else:
                    glasses = "是:太阳镜"
                self.tex_check_message.appendPlainText("是否佩戴眼镜:" + str(glasses))
                if mask == 0:
                    mask = "否"
                else:
                    mask = "是"
                self.tex_check_message.appendPlainText("是否佩戴口罩:" + str(mask))
                self.tex_check_message.appendPlainText("——————————————")
        else:
            print("人脸获取失败！")

    # #摄像头数据显示
    def show_cameradata(self):
        #获取摄像头数据
        pic = self.cameraVideo.camera_to_pic()
        #在Bodylabel中显示画面
        self.lab_cap.setPixmap(pic)


    # #关闭签到
    def close_sign_in(self):
        if self.sign_pressed == False :
            QMessageBox.warning(self,"警告","没有签到")
            return self.sign_pressed
        else:
            self.start_state = True     # 签到关闭
            self.faceshow.stop()        # 计时器停止
            self.detect.ok = False      # 停止run
            self.detect.quit()          # 关闭线程
            #关闭定时器
            self.timeshow.stop()
            self.timeshow.timeout.disconnect(self.show_cameradata)
            #关闭摄像头
            self.cameraVideo.colse_camera()
            #判断定时器是否关闭，则显示为自己设定的图像
            if self.timeshow.isActive() == False:
                self.lab_cap.setPixmap(QPixmap("./resource/images/logo.png"))
                self.tex_check_message.clear()
            else:
                QMessageBox.warning(self, "提示", "关闭失败")

            if self.faceshow.isActive() == True:
                QMessageBox.warning(self, "警告", "关闭run失败")
            else:
                print("yy")
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

