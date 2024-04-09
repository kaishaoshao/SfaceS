import requests
from PyQt5.QtCore import QThread,pyqtSignal
class detect_thread(QThread):
    transmit_data = pyqtSignal(dict) # 定义信号
    def __init__(self,access_token):
        super(detect_thread,self).__init__()
        self.ok = t=True # 循环控制变量
        self.condition = False # 人脸检查控制变量，是否进行人脸检测
        self.access_token = access_token # 主线程获取的access_token信息传递给子线程并设置为全局变量
    # run函数执行结束代表线程结束
    def run(self):
        while self.ok == True:
            if self.condition == True:
                self.detect_face(self.imge_data)

    # 接受主线程传递过来的图像
    def get_imge_data(self,data):
        # 当窗口调用这个槽函数，就把传递的数据放在线程的变量中
        self.imge_data = data # 将接收到的图像数据赋值给全局变量
        self.condition = True # 主线程有图像传递过来，改变condition的状态，run函数中运行人脸检测函数

    # 人脸检测
    def detect_face(self,base64_image):
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
        # 请求参数是一个字典，字典中存储了要识别的内容
        params = {
            "image":base64_image,    # 图片信息字符
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
            data = response.json()
            self.transmit_data.emit(dict(data))














