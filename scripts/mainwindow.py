from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5 import QtCore
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QCheckBox, QLineEdit, QGridLayout, QWidget, QLabel, QPushButton, QTextEdit

import threading

import scripts.threadqueue as tq

import os

import time

import scripts.server as serv
import scripts.client as clnt

import scripts.encrypted as ect


class ChatroomWindow(QWidget):

    def displayText(self):
        if self.textTQ.size > 0:
            giventext = self.textDisplay.toPlainText()
            giventext += f"\n{self.textTQ.pop()}"
            self.textDisplay.setText(giventext)

    def timerDisp(self):
        self.timer = QTimer()
        self.timer.setInterval(300)
        self.timer.timeout.connect(self.displayText)
        self.timer.start()

    def sendText(self):
        text = self.enterText.text()
        self.sendTQ.push(text)
        self.enterText.setText("")

    def __init__(self, data,parent=None):
        super().__init__(parent)
        self.sendTQ = tq.ThreadQueue()
        self.textTQ = tq.ThreadQueue()
        self.signalSend = tq.ThreadQueue()

        self.textDisplay = QTextEdit()
        self.textDisplay.setReadOnly(True)

        self.ip = data[0]
        self.port = int(data[1])
        self.mode = data[2]
        self.type = data[3]
        self.nickname = data[4]

        layout = QGridLayout()
        
        self.enterText = QLineEdit()
        self.enterText.setPlaceholderText("Enter text here...")

        self.enterText.returnPressed.connect(self.sendText)

        layout.addWidget(self.textDisplay)
        layout.addWidget(self.enterText)

        self.setLayout(layout)

        if self.type is True:
            if self.mode is True:
                self.chatthread = threading.Thread(target=serv.main, args=(self.port, self.textTQ, self.signalSend))
            else:
                self.chatthread = threading.Thread(target=clnt.main, args=(self.ip, self.port, self.nickname, self.textTQ, self.sendTQ))
        else:
            self.chatthread = threading.Thread(target=ect.mainscript, args=(self.ip, self.port, self.mode, self.textTQ, self.sendTQ))

        self.timerDisp()
        self.chatthread.start()

    def closeEvent(self, event):
        self.signalSend.push("End")
        self.timer.stop()
        time.sleep(1)
        

class MenuWindow(QMainWindow):

    def ChatroomToggle(self):
        if not self.chatroom:
            self.chatroom = True

    def EncryptedToggle(self):
        if self.chatroom:
            self.chatroom = False

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chatroom Service")

        self.welcomeText = QLabel("Welcome to the Chatroom Service!")
        self.ipEnter = QLineEdit()
        self.portEnter = QLineEdit()
        self.nicknameEnter = QLineEdit()
        self.hostCheckBox = QCheckBox("Host mode")
        self.chatRoom = QPushButton("Chatroom")
        self.encrypted = QPushButton("1-to-1")

        self.chatroom = False

        self.chatRoom.clicked.connect(self.ChatroomToggle)
        self.encrypted.clicked.connect(self.EncryptedToggle)

        self.hostCheckBox.toggled.connect(lambda:self.hostCheckState(self.hostCheckBox))

        self.setFixedSize(400, 200)

        self.ipEnter.setPlaceholderText("Enter IP Address here...")
        self.portEnter.setPlaceholderText("Enter port number here...")
        self.nicknameEnter.setPlaceholderText("Enter nickname (only for chatroom option)...")

        layout = QGridLayout()
        layout.addWidget(self.welcomeText, 0, 0)
        layout.addWidget(self.ipEnter, 1, 0)
        layout.addWidget(self.portEnter, 2, 0)
        layout.addWidget(self.nicknameEnter, 3, 0)
        layout.addWidget(self.hostCheckBox, 4, 0)
        layout.addWidget(self.chatRoom, 4, 1)
        layout.addWidget(self.encrypted, 4, 2)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def hostCheckState(self, checkBox):
        if checkBox.isChecked() == True:
            self.ipEnter.setVisible(False)
        else:
            self.ipEnter.setVisible(True)

    def showChatWindow(self):
        self.chatroomWindow = ChatroomWindow((self.ipEnter.text(), self.portEnter.text(), self.hostCheckBox.isChecked(), self.chatroom, self.nicknameEnter.text()))
        self.chatroomWindow.show()

    def EncryptedToggle(self):
        if self.chatroom == True:
            self.chatroom = False
        self.showChatWindow()

    def ChatroomToggle(self):
        if self.chatroom == False:
            self.chatroom = True
        self.showChatWindow()

    def closeEvent(self, event):
        os._exit(0)