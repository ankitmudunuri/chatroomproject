import scripts.mainwindow as mw
from PyQt5.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)

    window = mw.MenuWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()

