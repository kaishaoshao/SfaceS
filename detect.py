import requests
from PyQt5.QtCore import QThread,pyqtSignal,QDateTime

class detect_thread(QThread):
    transmit_data = pyqtSignal(dict) # 定义信号,用于子线程与主线程的人脸检测数据交互
    transmit_data1 = pyqtSignal(str) # 定义信号，用于子线程与主线程中的人脸识别数据交互
    def __init__(self,access_token):
        super(detect_thread,self).__init__()
        self.ok = True # 循环控制变量
        self.condition = False # 人脸检查控制变量，是否进行人脸检测
        self.access_token = access_token # 主线程获取的access_token信息传递给子线程并设置为全局变量
        # self.run()
    # run函数执行结束代表线程结束
    def run(self):
        while self.ok == True:
            if self.condition == True:
                print("imag_data")
                self.detect_face(self.imge_data)
                self.condition = False
            else:
                continue

    # 接受主线程传递过来的图像
    def get_imge_data(self,data):
        # 当窗口调用这个槽函数，就把传递的数据放在线程的变量中
        if data:
            self.imge_data = data # 将接收到的图像数据赋值给全局变量
            self.condition = True # 主线程有图像传递过来，改变condition的状态，run函数中运行人脸检测函数
        else:
            self.condition = False
            print("BULL")
    # 人脸检测
    def detect_face(self,base64_image):
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
        # 请求参数是一个字典，字典中存储了要识别的内容
        params = {
            "image": base64_image,    # 图片信息字符
            "image_type": "BASE64",  # 图片信息格式
            "face_field": "gender,age,beauty,mask,emotion,expression,glasses,face_shape",
            "max_face_num": 10
        }

        # 访问令牌
        access_token = self.access_token
        request_url = request_url + "?access_token=" + access_token
        # 设置请求的格式体
        headers = {'content-type': 'application/json'}
        #发送post网络请求，请求百度AI进行人脸检测
        response = requests.post(request_url,data=params,headers=headers)
        if response:
            print(response.json())
            data = response.json()
            self.face_search()
            if data['error_code'] == 0:
                self.transmit_data.emit(dict(data))
            else:
                return
        else:
            return

    # 人脸识别搜索算法，识别一个人
    def face_search(self):
        requests_url = "https://aip.baidubce.com/rest/2.0/face/v3/search"
        params = {
            "image": self.imge_data,
            "image_type": "BASE64",
            "group_id_list": "class1",
        }
        access_token = self.access_token
        request_url = requests_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            data = response.json()
            print(data)
            if data['error_msg'] == 'SUCCESS':
                del [data['result']['user_list'][0]['score']]
                datetime = QDateTime.currentDateTime() # 获取人脸打开时间
                datetime = datetime.toString() # 转换为字符串
                data['result']['user_list'][0]['datetime'] = datetime  # 将获取到的时间添加到返回的数据中
                list1 = [data['result']['user_list'][0]['user_id'],data['result']['user_list'][0]['group_id']]  # 去除名字和班级
                stu_str = "学生签到成功\n学生信息如下:\n"
                print(list1[0])

                self.transmit_data1.emit(stu_str + "姓名:" + list1[0] + "\n" + "班级:" + list1[1])  # 将信号发送给主线程











