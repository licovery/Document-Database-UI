from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem, QPushButton, \
                            QMessageBox, QInputDialog, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot
from dialog import SearchDialog, InsertDialog
from doclistwidget import DocListWidget
from docdb import DocDb, Document


class MainWindow(QWidget):
    def __init__(self, path, parent=None):
        super().__init__(parent)

        #界面初始化
        self.resize(700, 400)
        self.setWindowTitle('文档数据库')
        self.setWindowIcon(QIcon('resource/doc_icon1'))

        #数据
        self.db = DocDb(path)
        self.current_col = self.db.collection('default')

        #初始化集合表
        self.collections = QListWidget(self)
        self.collections.setStyleSheet("QListWidget::item:selected{background:skyblue; color:black}");
        self.collections.setFont(QFont("consolas", 12))
        for col_name in self.db.getCollections():
            self.collections.addItem(QListWidgetItem(col_name))
            self.collections.sortItems()
        #默认选第一行
        self.collections.setCurrentRow(0)
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
        self.content.setStyleSheet("QListWidget::item:selected{background:skyblue; color:black}");
        self.content.setFont(QFont("consolas", 12))
        self.content.set_docs(self.current_col.all())
        self.content.signal_update_doc.connect(self.slot_update_doc)
        self.content.signal_remove_doc.connect(self.slot_remove_doc)

        hbox = QHBoxLayout()
        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()
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


    #关闭程序时关闭数据库
    def closeEvent(self, QCloseEvent):
        # print('close')
        self.db.close()


    #如果同时双击和切换行，会同时出发两个槽函数（优化）
    @pyqtSlot(QListWidgetItem)
    def slot_collection_doubleclick(self, item):
        col_name = item.text()
        self.current_col = self.db.collection(col_name)
        self.content.set_docs(self.current_col.all())
        # print('item double click')


    #集合切换，显示集合所有文档
    @pyqtSlot(int)
    def slot_collection_change(self, row):
        if row != -1:
            col_name = self.collections.item(row).text()
            self.current_col = self.db.collection(col_name)
            self.content.set_docs(self.current_col.all())
            # print('collection row change')


    #创建集合
    @pyqtSlot()
    def slot_cre_col(self):
        value, ok = QInputDialog.getText(self, '新建集合', '请输入集合名', QLineEdit.Normal)
        if ok and value:
            #判断集合是否已经存在
            if not value in self.db.getCollections():
                item = QListWidgetItem(value)
                self.collections.addItem(item)
                self.collections.setCurrentItem(item)
                self.current_col = self.db.collection(value)
                self.content.set_docs(self.current_col.all())
            else:
                QMessageBox.warning(self, '创建集合', '集合已经存在')


    #考虑删除集合移动到右键操作而不是单独按钮
    @pyqtSlot()
    def slot_del_col(self):
        row = self.collections.currentRow()
        if row != -1:
            col_name = self.collections.item(row).text()
            #弹出确认框
            ok = QMessageBox.question(self, '删除集合', '确认删除集合%s' % col_name, QMessageBox.Yes | QMessageBox.No)
            if ok == QMessageBox.Yes:
                self.collections.takeItem(row)
                self.db.dropCollection(col_name)
                self.content.set_docs([])

    #查询对话框
    @pyqtSlot()
    def slot_find_doc(self):
        if self.collections.currentRow() != -1:
            w = SearchDialog(self)
            if w.exec_():
                docs = self.current_col.find(w.res)
                self.content.set_docs(docs)

    #插入文档对话框
    @pyqtSlot()
    def slot_insert_doc(self):
        row = self.collections.currentRow()
        if row != -1:
            self.collections.item(row).text()
            w = InsertDialog(self)
            if w.exec_():
                self.current_col.insert(w.res)
            #调用槽函数重新显示插入文档后的集合
            self.slot_collection_change(row)


    #从数据库更新文档
    @pyqtSlot(Document)
    def slot_update_doc(self, doc):
        row = self.collections.currentRow()
        if row != -1:
            self.current_col.writeBack(doc)


    #从数据库删除文档
    @pyqtSlot(Document)
    def slot_remove_doc(self, doc):
        row = self.collections.currentRow()
        if row != -1:
            self.current_col.removeDoc(doc)