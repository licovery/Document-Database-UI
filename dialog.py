from PyQt5.QtWidgets import QTextBrowser, QLabel, QTextEdit, QPushButton, QGridLayout, QDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot

import json

from docdb.query import Query
from docdb.database import Document

#查看窗口
class ReadDialog(QDialog):
    def __init__(self, doc, parent=None):


        super().__init__(parent)
        self.resize(500, 400)

        self.gbox = QGridLayout()
        self.label = QLabel('详细内容', self)

        self.textbrowser = QTextBrowser(self)


        self.textbrowser.setPlainText(json.dumps(doc.element))

        self.gbox.addWidget(self.label)
        self.gbox.addWidget(self.textbrowser)
        self.setLayout(self.gbox)



#db.find(cond)
#查询窗口
class SearchDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(500, 400)

        self.gbox = QGridLayout()
        self.label1 = QLabel('查询条件(字符串使用双引号 例 {"name": "neo"})', self)
        self.textedit =  QTextEdit(self)
        self.label2 = QLabel('空条件', self)
        self.label2.setStyleSheet('color:red')
        self.button = QPushButton('确定查询')



        self.textedit.textChanged.connect(self.slot_check_json)
        self.button.clicked.connect(self.slot_search)

        self.gbox.addWidget(self.label1)
        self.gbox.addWidget(self.textedit)
        self.gbox.addWidget(self.label2)
        self.gbox.addWidget(self.button)
        self.setLayout(self.gbox)



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
                if not cond:
                    cond = (Query(field) == value)
                else:
                    cond = cond & (Query(field) == value)

            self.res = cond
            self.done(1)

        else:
            self.label2.setText('格式错误，填入正确的内容再进行下一步')
            self.label2.setStyleSheet('color: red')



#插入窗口
#db.insert(elment)
class InsertDialog(QDialog):



    def __init__(self, parent=None):
        super().__init__(parent)


        self.resize(500, 400)
        self.gbox = QGridLayout()
        self.label1 = QLabel('插入文档(字符串使用双引号 例 {"name": "neo"} )', self)
        self.textedit = QTextEdit(self)
        self.label2 = QLabel('空文档', self)
        self.label2.setStyleSheet('color:red')
        self.button = QPushButton('插入')

        self.textedit.textChanged.connect(self.slot_check_json)
        self.button.clicked.connect(self.slot_insert_doc)

        self.gbox.addWidget(self.label1)
        self.gbox.addWidget(self.textedit)
        self.gbox.addWidget(self.label2)
        self.gbox.addWidget(self.button)
        self.setLayout(self.gbox)



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


    #返回的结果不是Document
    @pyqtSlot()
    def slot_insert_doc(self):
        if self.slot_check_json():
            element = json.loads(self.textedit.toPlainText())
            self.res = element
            self.done(1)
        else:
            self.label2.setText('格式错误，填入正确的内容再进行下一步')
            self.label2.setStyleSheet('color: red')





#更新窗口
#db.writeBack(Document)
class UpdateDialog(QDialog):


    def __init__(self, doc, parent=None):
        super().__init__(parent)

        self.doc = doc

        self.resize(500, 400)

        self.gbox = QGridLayout()
        self.label1 = QLabel('更新文档(字符串使用双引号 例 {"name": "neo"} )', self)
        self.textedit = QTextEdit(self)
        self.textedit.setPlainText(json.dumps(doc.element))
        self.label2 = QLabel('格式正确', self)
        self.label2.setStyleSheet('color: green')
        self.button = QPushButton('更新')

        self.textedit.textChanged.connect(self.slot_check_json)
        self.button.clicked.connect(self.slot_update_doc)

        self.gbox.addWidget(self.label1)
        self.gbox.addWidget(self.textedit)
        self.gbox.addWidget(self.label2)
        self.gbox.addWidget(self.button)
        self.setLayout(self.gbox)


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
            self.doc.element = json.loads(self.textedit.toPlainText())
            # self.res = self.doc
            self.done(1)
        else:
            self.label2.setText('格式错误，填入正确的内容再进行下一步')
            self.label2.setStyleSheet('color: red')

