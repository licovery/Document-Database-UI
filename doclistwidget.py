from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from dialog import ReadDialog, UpdateDialog

import json
from docdb import Document

class DocListWidget(QListWidget):


    signal_update_doc = pyqtSignal(Document)
    signal_remove_doc  = pyqtSignal(Document)


    def __init__(self, parent=None):
        super().__init__(parent)

        #右键菜单
        self.menu = QMenu(self)
        self.read_doc = QAction('查看文档')
        self.update_doc = QAction('修改文档')
        self.remove_doc = QAction('删除文档')

        self.menu.addAction(self.read_doc)
        self.menu.addAction(self.update_doc)
        self.menu.addAction(self.remove_doc)

        #信号与槽
        # self.currentRowChanged.connect(self.slot_doc_change)
        self.read_doc.triggered.connect(self.slot_read_doc)
        self.update_doc.triggered.connect(self.slot_update_doc)
        self.remove_doc.triggered.connect(self.slot_remove_doc)

        self.set_docs([])


    #获取到新的文档，刷新显示
    def set_docs(self, docs):
        #按list的顺序显示
        #数据保存在对象中
        self.docs = docs
        self.flush()

    #把docs内容显示到listwidget
    def flush(self):
        self.clear()
        for doc in self.docs:
            self.addItem(QListWidgetItem(json.dumps(doc.element, sort_keys=True)))
        #默认选择第一行，当docs == [],默认是-1行
        self.setCurrentRow(0)


    #右键菜单
    def contextMenuEvent(self, *args, **kwargs):
        #listwidget不为空时，右键菜单操作一定要有对象
        if self.currentRow() != -1:
            #从鼠标点击位置出现菜单
            self.menu.exec_(QCursor.pos())


    # @pyqtSlot(int)
    # def slot_doc_change(self, row):
    #     if row != -1:
    #         print('doc change  index: %d content: %s' % (row, self.docs[row]))


    #查询对话框
    @pyqtSlot()
    def slot_read_doc(self):
        w = ReadDialog(self.docs[self.currentRow()], self)
        w.exec_()


    #修改对话框
    @pyqtSlot()
    def slot_update_doc(self):
        doc = self.docs[self.currentRow()]
        w = UpdateDialog(doc, self)
        if w.exec_():
            self.item(self.currentRow()).setText(json.dumps(doc.element))
            #发射信号，参数是被修改后的文档，调用writeBack(doc)方法
            self.signal_update_doc.emit(doc)


    @pyqtSlot()
    def slot_remove_doc(self):
        ok = QMessageBox.question(self, '删除文档', '确认删除文档', QMessageBox.Yes | QMessageBox.No)
        if ok == QMessageBox.Yes:
            self.takeItem(self.currentRow())
            doc = self.docs.pop(self.currentRow())
            #发射信号通知db删除doc,调用removeDoc(doc)
            self.signal_remove_doc.emit(doc)