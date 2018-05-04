from PyQt5.QtWidgets import QTextBrowser, QLabel, QTextEdit, QPushButton, QGridLayout, QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
import json
from docdb.query import Query



#查看窗口
class ReadDialog(QDialog):

    def __init__(self, doc, parent=None):
        super().__init__(parent)

        #界面初始化
        self.resize(400, 275)
        self.setWindowTitle('查看')

        #部件
        self.label = QLabel('详细内容', self)
        self.textbrowser = QTextBrowser(self)
        self.textbrowser.setFont(QFont("consolas", 12))
        self.textbrowser.setPlainText(json.dumps(doc.element, sort_keys=True, indent=4))

        #控件布局
        self.gbox = QGridLayout()
        self.gbox.addWidget(self.label)
        self.gbox.addWidget(self.textbrowser)
        self.setLayout(self.gbox)



#查询窗口
class SearchDialog(QDialog):


    def __init__(self, parent=None):
        super().__init__(parent)

        #界面初始化
        self.resize(400, 275)
        self.setWindowTitle('查询')

        #部件
        self.label1 = QLabel('查询条件(字符串使用双引号 例 {"name": "neo"})', self)
        self.textedit =  QTextEdit(self)
        self.textedit.setFont((QFont("consolas", 12)))
        self.label2 = QLabel('空条件', self)
        self.label2.setStyleSheet('color:red')
        self.button = QPushButton('确定查询')

        #布局
        self.gbox = QGridLayout()
        self.gbox.addWidget(self.label1)
        self.gbox.addWidget(self.textedit)
        self.gbox.addWidget(self.label2)
        self.gbox.addWidget(self.button)
        self.setLayout(self.gbox)

        #信号与槽
        self.textedit.textChanged.connect(self.slot_check_json)
        self.button.clicked.connect(self.slot_search)


    @pyqtSlot()
    def slot_check_json(self):
        try:
            if json.loads(self.textedit.toPlainText()) == {}:
                raise ValueError
            self.label2.setText('格式正确')
            self.label2.setStyleSheet('color: green')
            return True
        except:
            self.label2.setText('格式错误')
            self.label2.setStyleSheet('color: red')
            return False


    @pyqtSlot()
    def slot_search(self):
        if self.slot_check_json():
            d = json.loads(self.textedit.toPlainText())
            cond = None
            for field, value in d.items():
                if cond is None:
                    cond = (Query(field) == value)
                else:
                    cond = cond & (Query(field) == value)
            #从用户输入中获取查询的条件
            self.res = cond
            #结束对话框，参数是exec_()的返回值，用于判断用户是否点击按钮返回，或是关闭窗口（取消操作）
            self.done(1)
        else:
            self.label2.setText('格式错误，填入正确的内容再进行下一步')
            self.label2.setStyleSheet('color: red')



#插入窗口
class InsertDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        #界面初始化
        self.resize(400, 275)
        self.setWindowTitle('插入')

        #部件
        self.label1 = QLabel('插入文档(字符串使用双引号 例 {"name": "neo"} )', self)
        self.textedit = QTextEdit(self)
        self.textedit.setFont((QFont("consolas", 12)))
        self.label2 = QLabel('空文档', self)
        self.label2.setStyleSheet('color:red')
        self.button = QPushButton('插入')

        #布局
        self.gbox = QGridLayout()
        self.gbox.addWidget(self.label1)
        self.gbox.addWidget(self.textedit)
        self.gbox.addWidget(self.label2)
        self.gbox.addWidget(self.button)
        self.setLayout(self.gbox)

        #信号与槽
        self.textedit.textChanged.connect(self.slot_check_json)
        self.button.clicked.connect(self.slot_insert_doc)


    @pyqtSlot()
    def slot_check_json(self):
        try:
            if json.loads(self.textedit.toPlainText()) == {}:
                raise ValueError
            self.label2.setText('格式正确')
            self.label2.setStyleSheet('color: green')
            return True
        except:
            self.label2.setText('格式错误')
            self.label2.setStyleSheet('color: red')
            return False



    @pyqtSlot()
    def slot_insert_doc(self):
        if self.slot_check_json():
            element = json.loads(self.textedit.toPlainText())
            #用户修改过后的文档
            self.res = element
            #exce_返回值
            self.done(1)
        else:
            self.label2.setText('格式错误，填入正确的内容再进行下一步')
            self.label2.setStyleSheet('color: red')



#更新窗口
class UpdateDialog(QDialog):

    def __init__(self, doc, parent=None):
        super().__init__(parent)

        #界面初始化
        self.setWindowTitle('修改')
        self.resize(400, 275)

        #部件
        self.label1 = QLabel('更新文档(字符串使用双引号 例 {"name": "neo"} )', self)
        self.textedit = QTextEdit(self)
        self.textedit.setFont((QFont("consolas", 12)))
        self.textedit.setPlainText(json.dumps(doc.element, sort_keys=True, indent=4))
        self.label2 = QLabel('格式正确', self)
        self.label2.setStyleSheet('color: green')
        self.button = QPushButton('更新')

        #布局
        self.gbox = QGridLayout()
        self.gbox.addWidget(self.label1)
        self.gbox.addWidget(self.textedit)
        self.gbox.addWidget(self.label2)
        self.gbox.addWidget(self.button)
        self.setLayout(self.gbox)

        #信号与槽
        self.textedit.textChanged.connect(self.slot_check_json)
        self.button.clicked.connect(self.slot_update_doc)

        #数据
        self.doc = doc


    @pyqtSlot()
    def slot_check_json(self):
        try:
            if json.loads(self.textedit.toPlainText()) == {}:
                raise ValueError
            self.label2.setText('格式正确')
            self.label2.setStyleSheet('color: green')
            return True
        except:
            self.label2.setText('格式错误')
            self.label2.setStyleSheet('color: red')
            return False


    @pyqtSlot()
    def slot_update_doc(self):
        if self.slot_check_json():
            #更新文档
            self.doc.element = json.loads(self.textedit.toPlainText())
            self.done(1)
        else:
            self.label2.setText('格式错误，填入正确的内容再进行下一步')
            self.label2.setStyleSheet('color: red')