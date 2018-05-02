import sys
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow
from PyQt5.QtWidgets import *
from dialog import *
from docdb import *


#了解import机制，会出现类似C++的头文件重复包含问题吗？

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()


    # c = Document('1', {'name': 1})
    # a = UpdateDialog(c)
    # if a.exec_():#点击按钮返回1
    #     print(a.res)
    #     print(c)

    # w = QListWidget()
    # w.addItem(QListWidgetItem('111'))
    # w.item(0).setText('s789797')
    # w.takeItem(0)
    # w.show()

    sys.exit(app.exec_())