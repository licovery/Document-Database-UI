from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from dialog import *
import json


class DocListWidget(QListWidget):

    signal_update_doc = pyqtSignal(Document)
    signal_remove_doc  = pyqtSignal(Document)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.menu = QMenu(self)



        self.read_doc = QAction('查看文档')
        self.update_doc = QAction('修改文档')
        self.remove_doc = QAction('删除文档')

        self.menu.addAction(self.read_doc)
        self.menu.addAction(self.update_doc)
        self.menu.addAction(self.remove_doc)

        self.currentRowChanged.connect(self.slot_doc_change)
        self.read_doc.triggered.connect(self.slot_read_doc)
        self.update_doc.triggered.connect(self.slot_update_doc)
        self.remove_doc.triggered.connect(self.slot_remove_doc)


    def set_docs(self, docs):
        self.docs = docs
        self.flush()


    def flush(self):
        self.clear()
        for doc in self.docs:
            self.addItem(QListWidgetItem(json.dumps(doc.element)))
        self.setCurrentRow(0)



    #右键菜单的执行对象是currentRow()
    def contextMenuEvent(self, *args, **kwargs):
        if self.currentRow() != -1:
            self.menu.exec_(QCursor.pos())



    @pyqtSlot(int)
    def slot_doc_change(self, row):
        if row != -1:
            print('slot_doc_change   ' + 'current index: ' + str(row))
            print(self.docs[row])


    @pyqtSlot()
    def slot_read_doc(self):
        w = ReadDialog(self.docs[self.currentRow()], self)
        w.exec_()


    @pyqtSlot()
    def slot_update_doc(self):
        doc = self.docs[self.currentRow()]

        w = UpdateDialog(doc, self)
        if w.exec_():
            self.item(self.currentRow()).setText(json.dumps(doc.element))
            print('update ', doc)
            #write_back()

            self.signal_update_doc.emit(doc)


    @pyqtSlot()
    def slot_remove_doc(self):
        ok = QMessageBox.question(self, '删除文档', '确认删除文档', QMessageBox.Yes | QMessageBox.No)
        if ok == QMessageBox.Yes:
            self.takeItem(self.currentRow())
            doc = self.docs.pop(self.currentRow())

            #发射信号通知db删除doc

            self.signal_remove_doc.emit(doc)
            #从数据库删除