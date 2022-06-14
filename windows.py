from Ui_face_detect import Ui_MainWindow as face
from Ui_Main import Ui_MainWindow
from Ui_wait import Ui_Wait
from Ui_GKLink import Ui_GKlink
from Ui_Light import Ui_MainWindow as Light
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from detect import Detect_CKH
import cv2
import os

app=QApplication(sys.argv)

class GKLink(QMainWindow,Ui_GKlink):
    def __init__(self):
        super(GKLink, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.close)
        self.pushButton_2.clicked.connect(self.close)

Link=GKLink()

class WaitWin(QMainWindow,Ui_Wait):
    def __init__(self):
        super(WaitWin, self).__init__()
        self.setupUi(self)

class TempWin(QMainWindow,face,Ui_Wait):
    deal_ok=pyqtSignal()
    def __init__(self):
        super(TempWin,self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.openMsg_WJ)
        self.action_4.triggered.connect(self.openMsg_QZ)
        self.pushButton_4.clicked.connect(self.butoon_clicked)
        self.file_img='0'
        self.file_model='0'
        self.pushButton_3.clicked.connect(self.videocap_init)
        self.timer_camera=QTimer()
        self.timer_camera.timeout.connect(self.openvideo)
        self.de_flag=0
        self.pushButton_2.clicked.connect(self.videofile_init)
        self.timer_video=QTimer()
        self.timer_video.timeout.connect(self.openvideo)
        self.v_flag=0
        self.count=0
        self.font=QFont()
        self.font.setPointSize(10)
        self.action_2.triggered.connect(self.messagebox_author)
        self.action_3.triggered.connect(self.messagebox_version)
        self.action_5.triggered.connect(self.messagebox_info)
        self.pushButton_5.clicked.connect(self.GKlink)
    def GKlink(self):
        Link.show()
    def messagebox_info(self):
        QMessageBox.information(self,"权重文件信息","各类物体识别-YoloV5x网络")
    def messagebox_version(self):
        QMessageBox.information(self,"版本信息","V1.0")
    def messagebox_author(self):
        QMessageBox.information(self,"作者信息","主持人：崔锴华\n指导老师：靳红梅 王少博")
    def videofile_init(self):
        file,ok=QFileDialog.getOpenFileName(self,"输入要识别的视频文件（目录请不要带中文）","C:/","视频文件 (*.mp4 *.avi)")
        self.statusbar.showMessage("已打开文件："+file)
        print(file)
        self.file_img=file
        self.cap=cv2.VideoCapture(self.file_img)
        flag=self.cap.isOpened()
        if flag==False:
            reply = QMessageBox.warning(self, "警告！", "无法读取视频文件！")
        else:
            self.timer_video.start(30)
            self.v_flag=1

    def videocap_init(self):
        self.cap=cv2.VideoCapture(0+cv2.CAP_DSHOW)
        flag=self.cap.isOpened()
        if flag==False:
            reply=QMessageBox.warning(self,"警告！","无法打开摄像头！")
        else:
            self.timer_camera.start(10)
            self.v_flag=1

    def openvideo(self):
        flag,self.video_temp=self.cap.read()
        if self.de_flag==1:
            dir_path = os.getcwd()
            try:
                self.dection()
            except BaseException:
                image_out = cv2.cvtColor(self.video_temp, cv2.COLOR_RGB2BGR)
                height, width, bytesPerComponent = image_out.shape
                bytesPerLine = bytesPerComponent * width
                Qimg = QImage(image_out.data, width, height, bytesPerLine, QImage.Format_RGB888)
                self.label.setScaledContents(False)
                scaerdpath = QPixmap.fromImage(Qimg)
                scaerdpath_out = scaerdpath.scaled(761, 481, Qt.AspectRatioMode.KeepAspectRatio)
                self.label.setPixmap(scaerdpath_out)
                pass
            camera_source = dir_path + "\\video.jpg"
            cv2.imwrite(camera_source, self.video_temp)
            self.file_img = camera_source
        else:
            try:
                image_out = cv2.cvtColor(self.video_temp, cv2.COLOR_RGB2BGR)
            except BaseException:
                return 0
            height, width, bytesPerComponent = image_out.shape
            bytesPerLine = bytesPerComponent * width
            Qimg = QImage(image_out.data, width, height, bytesPerLine, QImage.Format_RGB888)
            self.label.setScaledContents(False)
            scaerdpath = QPixmap.fromImage(Qimg)
            scaerdpath_out = scaerdpath.scaled(761, 481, Qt.AspectRatioMode.KeepAspectRatio)
            self.label.setPixmap(scaerdpath_out)

    def openMsg_QZ(self):
        file,ok=QFileDialog.getOpenFileName(self,"输入权重文件：（目录请不要带中文）","C:/","神经网络权重 (*.pt)")
        self.statusbar.showMessage("已打开文件："+file)
        print(file)
        self.file_model=file

    def openMsg_WJ(self):
        file,ok=QFileDialog.getOpenFileName(self,"输入要识别的图像文件（目录请不要带中文）","C:/","图片文件 (*.jpeg *.jpg)")
        self.statusbar.showMessage("已打开文件："+file)
        path=QPixmap(file)
        print(file)
        scaerdpath=path.scaled(761,481,Qt.AspectRatioMode.KeepAspectRatio)
        self.label.setScaledContents(False)
        self.label.setPixmap(scaerdpath)
        self.file_img=file

    def dection(self):
        # try:
        #     img,save_dir,self.count=Detect_CKH(self.file_img)
        # except BaseException:
        #     self.count="正在初始化系统..."
        #     self.label_2.setText(str(self.count))
        #     QApplication.processEvents()
        # else:
        #     image_out=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        #     height,width,bytesPerComponent=image_out.shape
        #     bytesPerLine=bytesPerComponent*width
        #     Qimg=QImage(image_out.data,width,height,bytesPerLine,QImage.Format_RGB888)
        #     self.label.setScaledContents(False)
        #     scaerdpath=QPixmap.fromImage(Qimg)
        #     scaerdpath_out = scaerdpath.scaled(761, 481, Qt.AspectRatioMode.KeepAspectRatio)
        #     self.label.setPixmap(scaerdpath_out)
        #     self.label_2.setText(str(self.count))
        #     QApplication.processEvents()


        img, save_dir, self.count = Detect_CKH(self.file_img)
        image_out = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        height, width, bytesPerComponent = image_out.shape
        bytesPerLine = bytesPerComponent * width
        Qimg = QImage(image_out.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.label.setScaledContents(False)
        scaerdpath = QPixmap.fromImage(Qimg)
        scaerdpath_out = scaerdpath.scaled(761, 481, Qt.AspectRatioMode.KeepAspectRatio)
        self.label.setPixmap(scaerdpath_out)
        self.label_2.setText(str(self.count))
        QApplication.processEvents()


    def butoon_clicked(self):
        self.pushButton_4.setText("正在识别")
        self.count="没有检测到"
        QApplication.processEvents()
        try:
            img,save_dir,self.count=Detect_CKH(self.file_img)
        except UnboundLocalError:
            self.count="没有检测到目标！"
            self.label_2.setText(self.count)
            if self.v_flag == 1:
                if self.de_flag == 1:
                    self.de_flag = 0
                else:
                    self.de_flag = 1
            else:
                self.pushButton_4.setText("开始识别")
                QApplication.processEvents()
            return 0
        image_out=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        height,width,bytesPerComponent=image_out.shape
        bytesPerLine=bytesPerComponent*width
        Qimg=QImage(image_out.data,width,height,bytesPerLine,QImage.Format_RGB888)
        self.label.setScaledContents(False)
        scaerdpath=QPixmap.fromImage(Qimg)
        scaerdpath_out = scaerdpath.scaled(761, 481, Qt.AspectRatioMode.KeepAspectRatio)
        self.label.setPixmap(scaerdpath_out)
        if self.v_flag==1:
            if self.de_flag==1:
                self.de_flag=0
            else:
                self.de_flag=1
                self.pushButton_4.setText("开始识别")
                QApplication.processEvents()
        else:
            self.pushButton_4.setText("开始识别")
            QApplication.processEvents()
        self.label_2.setText(self.count)
        self.label_2.setAlignment(Qt.AlignHCenter)
        self.label_2.setFont(self.font)
        QApplication.processEvents()
        print(self.count)

class Singal(QObject):
    sendmsg=pyqtSignal(object)
    def __init__(self):
        super(Singal,self).__init__()

    def run(self):
        self.sendmsg.emit("Hello")

class Slot(QObject):
    def __init__(self):
        super(Slot,self).__init__()

    def get(self,msg):
        print("QSlot get msg-->"+msg)

class Light_Window(QMainWindow, Light):
    def __init__(self):
        super(Light_Window, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.messagebox_OK)
        self.pushButton_2.clicked.connect(self.messagebox_OK)
        self.pushButton_3.clicked.connect(self.messagebox_OK)
        self.pushButton_4.clicked.connect(self.messagebox_OK)
        self.pushButton_5.clicked.connect(self.messagebox_OK)
        self.pushButton_6.clicked.connect(self.messagebox_OK)
        self.pushButton_7.clicked.connect(self.messagebox_OK)
        self.pushButton_8.clicked.connect(self.messagebox_OK)

    def messagebox_OK(self):
        QMessageBox.information(self, "消息提示", "切换成功！")

light=Light_Window()
send=Singal()
slot=Slot()
send.sendmsg.connect(slot.get)
send.run()
ui = TempWin()

class StartWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(StartWindow,self).__init__()
        self.setupUi(self)
        timer1=QTimer(self)
        timer2=QTimer(self)
        timer1.timeout.connect(self.close)
        timer2.timeout.connect(ui.show)
        # timer1.start(3000)
        # timer2.start(3000)
        self.pushButton_17.clicked.connect(ui.show)
        self.pushButton_7.clicked.connect(Link.show)
        self.pushButton_15.clicked.connect(self.messagebox_opendoorOK)
        self.pushButton_16.clicked.connect(self.messagebox_closedoorOK)
        self.pushButton_7.clicked.connect(self.GKlink)
        self.pushButton_21.clicked.connect(light.show)
    def messagebox_opendoorOK(self):
        QMessageBox.information(self,"消息提示","开门成功！")
    def messagebox_closedoorOK(self):
        QMessageBox.information(self,"消息提示","锁门成功！")
    def GKlink(self):
        Link.show()




st=StartWindow()
st.show()

sys.exit(app.exec_())