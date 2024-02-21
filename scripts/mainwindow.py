from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QCheckBox, QLineEdit, QGridLayout, QWidget, QLabel, QPushButton, QTextEdit

import threadqueue as tq

import server as serv
import client as clnt

import encrypted as ect


class ChatroomWindow(QWidget):

    def __init__(self, data,parent=None):
        super().__init__(parent)
        self.sendTQ = tq.ThreadQueue()
        self.textTQ = tq.ThreadQueue()

        self.textDisplay = QTextEdit()
        self.textDisplay.setReadOnly(True)

        self.ip = data[0]
        self.port = data[1]
        self.mode = data[2]
        self.type = data[3]

        layout = QGridLayout()
        
        self.enterText = QLineEdit()
        self.enterText.setPlaceholderText("Enter text here...")

    def displayText(self):
        pass


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

        self.chatRoom.setCheckable(True)
        self.chatRoom.clicked.connect(self.ChatroomToggle)
        self.encrypted.setCheckable(True)
        self.chatRoom.clicked.connect(self.EncryptedToggle)

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
        self.chatroomWindow = ChatroomWindow((self.ipEnter.text(), self.portEnter.text(), self.hostCheckBox.isChecked(), self.chatroom))

        

    def clicked(self):
        print("Yes")