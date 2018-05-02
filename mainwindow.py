from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem, QPushButton, QMessageBox, QInputDialog, QLineEdit
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout


from dialog import *
from doclistwidget import DocListWidget
from docdb import *

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


        self.docdb = DocDb('test')
        self.current_col = self.docdb.collection('default')


        hbox = QHBoxLayout()
        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()

        self.collections = QListWidget(self)

        for col_name in self.docdb.getCollections():
            self.collections.addItem(QListWidgetItem(col_name))


        self.collections.currentRowChanged.connect(self.slot_collection_change)
        self.collections.itemDoubleClicked.connect(self.slot_collection_doubleclick)


        self.cre_collection = QPushButton('新建集合', self)
        self.cre_collection.clicked.connect(self.slot_cre_col)

        self.del_collection = QPushButton('删除集合', self)
        self.del_collection.clicked.connect(self.slot_del_col)

        self.find_doc = QPushButton('查询', self)
        self.find_doc.clicked.connect(self.slot_find_doc)

        self.insert_doc = QPushButton('插入文档', self)
        self.insert_doc.clicked.connect(self.slot_insert_doc)


        self.content = DocListWidget(self)
        self.content.set_docs(self.current_col.all())

        self.content.signal_update_doc.connect(self.slot_update_doc)
        self.content.signal_remove_doc.connect(self.slot_remove_doc)

        vbox1.addWidget(self.collections)
        vbox1.addWidget(self.cre_collection)
        vbox1.addWidget(self.del_collection)
        vbox1.addWidget(self.find_doc)
        vbox1.addWidget(self.insert_doc)
        vbox2.addWidget(self.content)
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)

        hbox.setStretchFactor(vbox1, 1)
        hbox.setStretchFactor(vbox2, 3)
        self.setLayout(hbox)

        print(self.size())

    #如果同时双击和切换行，会同时出发两个槽函数（优化）
    @pyqtSlot(QListWidgetItem)
    def slot_collection_doubleclick(self, item):
        col_name = item.text()
        self.current_col = self.docdb.collection(col_name)
        self.content.set_docs(self.current_col.all())
        print('item double click')


    @pyqtSlot(int)
    def slot_collection_change(self, row):
        if row != -1:
            col_name = self.collections.item(row).text()
            self.current_col = self.docdb.collection(col_name)
            self.content.set_docs(self.current_col.all())
            print('collection row change')


    @pyqtSlot()
    def slot_cre_col(self):
        value, ok = QInputDialog.getText(self, '新建集合', '请输入集合名', QLineEdit.Normal)
        if ok and value:
            if not value in self.docdb.getCollections():
                self.collections.addItem(QListWidgetItem(value))

            self.current_col = self.docdb.collection(value)
            self.content.set_docs(self.current_col.all())

            # 处理空串和同名集合


    #考虑删除集合移动到右键操作而不是单独按钮
    @pyqtSlot()
    def slot_del_col(self):
        row = self.collections.currentRow()
        if row != -1:
            col_name = self.collections.item(row).text()

            ok = QMessageBox.question(self, '删除集合', '确认删除集合%s' % col_name, QMessageBox.Yes | QMessageBox.No)
            if ok == QMessageBox.Yes:
                self.collections.takeItem(row)
                self.docdb.dropCollection(col_name)
                self.content.set_docs([])

    @pyqtSlot()
    def slot_find_doc(self):
        if self.collections.currentRow() != 1:
            w = SearchDialog(self)
            if w.exec_():
                docs = self.current_col.find(w.res)
                self.content.set_docs(docs)

    @pyqtSlot()
    def slot_insert_doc(self):
        row = self.collections.currentRow()
        if row != -1:
            self.collections.item(row).text()
            w = InsertDialog(self)
            if w.exec_():
                self.current_col.insert(w.res)
            self.slot_collection_change(row)


    @pyqtSlot(Document)
    def slot_update_doc(self, doc):
        row = self.collections.currentRow()
        if row != -1:
            self.current_col.writeBack(doc)


    @pyqtSlot(Document)
    def slot_remove_doc(self, doc):
        row = self.collections.currentRow()
        if row != -1:
            self.current_col.removeDoc(doc)