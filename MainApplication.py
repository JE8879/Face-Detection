import sys
import cv2
import numpy as np
from PyQt6 import uic, QtCore
from PyQt6.QtGui import QImage, QPixmap, QGuiApplication
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, Qt, QTimer
from PyQt6.QtWidgets import QPushButton, QLabel, QLineEdit, QWidget, QApplication


class MainApplication(QWidget):
    # Constructor
    def __init__(self):
        super(MainApplication, self).__init__()

        # Load Template
        uic.loadUi('Templates/FaceDetectionTemplate.ui', self)

        # Open default camera
        self.VideoCapture = cv2.VideoCapture(0) 
        # Set Width and Height
        # self.VideoCapture.set(cv2.CAP_PROP_FRAME_WIDTH, 812)
        # self.VideoCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        # self.VideoCapture.set(cv2.CAP_PROP_FPS, 30)

        self.LblCapture = self.findChild(QLabel, 'LblCapture')
        self.face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.UpdateImage)
        self.timer.start(100) # Update every 100 milliseconds

        self.SetCenterWidget()

    def SetCenterWidget(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def UpdateImage(self):      
        ret, cap = self.VideoCapture.read()
        if ret:
        # Convert OpenCV image to QImage
            rgbImage = cv2.cvtColor(cap, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytes_per_line = 3 * w
            qImage = QImage(rgbImage.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

            faceImage = rgbImage.copy()
            faces = self.face_cascade.detectMultiScale(faceImage, scaleFactor=1.3, minNeighbors=5)

            # Draw rectangles around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(rgbImage, (x,y), (x+w, y+h), (255, 255, 255), 5)

            pixmap = QPixmap.fromImage(qImage)
            self.LblCapture.setPixmap(pixmap)

if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = MainApplication()
    
    window.show()
    
    app.exec()
