import sys
from PyQt5.QtWidgets import QApplication, QInputDialog, QLineEdit
from PyQt5.QtGui import QFont
from mainwindow import MainWindow


#了解import机制，会出现类似C++的头文件重复包含问题吗？

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # letterfont = QFont("consolas", 12)
    # wordfont = QFont("Microsoft YaHei", 10)

    #统一设置字体
    app.setFont(QFont("Microsoft YaHei", 10))

    path, ok = QInputDialog.getText(None, '创建数据库', '请输入数据库路径', QLineEdit.Normal)
    if ok and path:
        w = MainWindow(path)
        w.show()
        sys.exit(app.exec_())