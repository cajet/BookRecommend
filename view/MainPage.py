# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainPage.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import pymysql
import sys
from recommend import recommend as rc
from recommend import performance as pf

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(752, 641)

        self.label_borrowed = QtWidgets.QLabel(Dialog)
        self.label_borrowed.setGeometry(QtCore.QRect(10, 60, 131, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.label_borrowed.setFont(font)
        self.label_borrowed.setObjectName("label_borrowed")

        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 10, 711, 41))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.HlLayout_top = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.HlLayout_top.setContentsMargins(0, 0, 0, 0)
        self.HlLayout_top.setObjectName("HlLayout_top")
        self.HLayout_cardid = QtWidgets.QHBoxLayout()
        self.HLayout_cardid.setObjectName("HLayout_cardid")
        self.label_cardid = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.label_cardid.setFont(font)
        self.label_cardid.setObjectName("label_cardid")
        self.HLayout_cardid.addWidget(self.label_cardid)
        self.Edit_cardid = QtWidgets.QTextEdit(self.horizontalLayoutWidget_3)
        self.Edit_cardid.setMinimumSize(QtCore.QSize(120, 0))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.Edit_cardid.setFont(font)
        self.Edit_cardid.setObjectName("Edit_cardid")
        self.HLayout_cardid.addWidget(self.Edit_cardid)
        self.HLayout_k = QtWidgets.QHBoxLayout()
        self.HLayout_k.setObjectName("HLayout_k")
        self.label_k = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.label_k.setFont(font)
        self.label_k.setObjectName("label_k")
        self.HLayout_k.addWidget(self.label_k)
        self.Edit_k = QtWidgets.QTextEdit(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.Edit_k.setFont(font)
        self.Edit_k.setObjectName("Edit_k")
        self.HLayout_k.addWidget(self.Edit_k)
        self.HLayout_rec_nums = QtWidgets.QHBoxLayout()
        self.HLayout_rec_nums.setObjectName("HLayout_rec_nums")
        self.label_rec_num = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.label_rec_num.setFont(font)
        self.label_rec_num.setObjectName("label_rec_num")
        self.HLayout_rec_nums.addWidget(self.label_rec_num)
        self.Edit_rec_nums = QtWidgets.QTextEdit(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.Edit_rec_nums.setFont(font)
        self.Edit_rec_nums.setObjectName("Edit_rec_nums")
        self.HLayout_rec_nums.addWidget(self.Edit_rec_nums)
        self.HLayout_k.addLayout(self.HLayout_rec_nums)
        self.HLayout_cardid.addLayout(self.HLayout_k)
        self.HlLayout_top.addLayout(self.HLayout_cardid)

        self.Btn_query_borrowed = QtWidgets.QPushButton(Dialog)
        self.Btn_query_borrowed.setGeometry(QtCore.QRect(600, 60, 121, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.Btn_query_borrowed.setFont(font)
        self.Btn_query_borrowed.setObjectName("Btn_query_borrowed")

        self.listview_borrowed = QtWidgets.QListWidget(Dialog)
        self.listview_borrowed.setGeometry(QtCore.QRect(10, 90, 711, 161))
        self.listview_borrowed.setObjectName("listview_borrowed")

        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 260, 281, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.label_alrogithm = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.label_alrogithm.setFont(font)
        self.label_alrogithm.setObjectName("label_alrogithm")
        self.horizontalLayout.addWidget(self.label_alrogithm)

        self.comboBox = QtWidgets.QComboBox(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)

        self.label_recommendresult = QtWidgets.QLabel(Dialog)
        self.label_recommendresult.setGeometry(QtCore.QRect(10, 310, 131, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.label_recommendresult.setFont(font)
        self.label_recommendresult.setObjectName("label_recommendresult")

        self.listview_recommendresult = QtWidgets.QListWidget(Dialog)
        self.listview_recommendresult.setGeometry(QtCore.QRect(10, 350, 711, 171))
        self.listview_recommendresult.setObjectName("listview_recommendresult")

        self.Btn_recommend = QtWidgets.QPushButton(Dialog)
        self.Btn_recommend.setGeometry(QtCore.QRect(600, 320, 121, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.Btn_recommend.setFont(font)
        self.Btn_recommend.setObjectName("Btn_recommend")

        self.label_performance = QtWidgets.QLabel(Dialog)
        self.label_performance.setGeometry(QtCore.QRect(20, 570, 800, 51))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.label_performance.setFont(font)
        self.label_performance.setObjectName("label_performance")

        self.Btn_query_performance = QtWidgets.QPushButton(Dialog)
        self.Btn_query_performance.setGeometry(QtCore.QRect(10, 530, 111, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.Btn_query_performance.setFont(font)
        self.Btn_query_performance.setObjectName("Btn_query_performance")
        self.label_borrowed.raise_()
        self.horizontalLayoutWidget_3.raise_()
        self.Btn_query_borrowed.raise_()
        self.listview_borrowed.raise_()
        self.horizontalLayoutWidget_2.raise_()
        self.label_recommendresult.raise_()
        self.listview_recommendresult.raise_()
        self.Btn_recommend.raise_()
        self.label_performance.raise_()
        self.Btn_query_performance.raise_()

        self.retranslateUi(Dialog)
        self.Btn_query_borrowed.clicked.connect(self.query_bor_button_click)
        self.Btn_recommend.clicked.connect(self.recommend_button_click)
        self.Btn_query_performance.clicked.connect(self.query_performance_click)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

        self.Edit_k.setText(_translate("Dialog", "20"))
        self.Edit_rec_nums.setText(_translate("Dialog", "10"))
        self.label_borrowed.setText(_translate("Dialog", "借阅记录："))
        self.label_cardid.setText(_translate("Dialog", "校园卡号："))
        self.label_k.setText(_translate("Dialog", "推荐邻居数："))
        self.label_rec_num.setText(_translate("Dialog", "推荐数目："))
        self.Btn_query_borrowed.setText(_translate("Dialog", "查询借阅记录"))

        self.label_alrogithm.setText(_translate("Dialog", "推荐算法选择："))

        self.comboBox.setItemText(0, _translate("Dialog", "itemcf"))
        self.comboBox.setItemText(1, _translate("Dialog", "usercf"))
        self.comboBox.setCurrentIndex(0)

        self.label_recommendresult.setText(_translate("Dialog", "推荐结果："))

        self.Btn_recommend.setText(_translate("Dialog", "开始推荐书籍"))
        self.label_performance.setText(_translate("Dialog", "算法性能："))
        self.Btn_query_performance.setText(_translate("Dialog", "查看算法性能"))

    def query_bor_button_click(self):
        #QtWidgets.QMessageBox.information(self.Btn_query_borrowed, "标题", "这是第一个PyQt5 GUI程序")
        cardid= self.Edit_cardid.toPlainText()
        self.listview_borrowed.clear()

        db = pymysql.connect("localhost", "CAJET", "12226655", "book_recommend")
        cursor = db.cursor()
        sql_query_sim = "SELECT book_name FROM BorrowTable WHERE card_id= '%s' AND testdata='%d';"
        data = (cardid, 0)
        try:
            cursor.execute(sql_query_sim % data)
            if cursor.rowcount == 0:
                item = QtWidgets.QListWidgetItem()
                item.setText('未找到相关借阅记录')
                self.listview_borrowed.addItem(item)
            for row in cursor.fetchall():
                item = QtWidgets.QListWidgetItem()
                item.setText(row[0])
                self.listview_borrowed.addItem(item)
        except:
            print('Error!')

    def recommend_button_click(self):
        db = pymysql.connect("localhost", "CAJET", "12226655", "book_recommend")
        cursor = db.cursor()
        sql_query_bookname = "SELECT book_name FROM BookTable WHERE id= '%d';"

        self.listview_recommendresult.clear()
        cardid = self.Edit_cardid.toPlainText()
        K= int(self.Edit_k.toPlainText())
        N= int(self.Edit_rec_nums.toPlainText())
        algorithm_type= self.comboBox.currentIndex()

        if (int(cardid)< 14331000 or int(cardid) > 14332000) :
            item = QtWidgets.QListWidgetItem()
            item.setText("无法对该card_id进行书籍推荐")
            self.listview_recommendresult.addItem(item)
        else:
            rec_books = rc.Recommend(cardid, K, N, algorithm_type).start_recommend()
            for book, _ in rec_books:
                data= (int(book))
                cursor.execute(sql_query_bookname % data)
                for row in cursor.fetchall():
                    item = QtWidgets.QListWidgetItem()
                    item.setText(row[0])
                    #self.listview_recommendresult.itemDoubleClicked().connect(lv_recommend_reason)
                    self.listview_recommendresult.addItem(item)

    def query_performance_click(self):
        self.label_performance.clear()
        K= int(self.Edit_k.toPlainText())
        N= int(self.Edit_rec_nums.toPlainText())
        algorithm_type= self.comboBox.currentIndex()

        db = pymysql.connect("localhost", "CAJET", "12226655", "book_recommend")
        cursor = db.cursor()
        sql_query_performance = "SELECT precision_, recall, coverage, popularity FROM Performance WHERE algorithm_type= '%d' and k= '%d';"
        data= (algorithm_type, K)
        cursor.execute(sql_query_performance % data)

        if cursor.rowcount == 0:  #无法从数据库中找到
            per= pf.Performance(N, K, algorithm_type)
            per.evaluate()
            self.label_performance.setText('算法性能：\nprecision:%.6f\trecall:%.6f\tcoverage:%.6f\tpopularity:%.6f' %
                  (per.precision, per.recall, per.coverage, per.popularity))

        else:
            for row in cursor.fetchall():
                self.label_performance.setText('算法性能：\nprecision:%.6f\trecall:%.6f\tcoverage:%.6f\tpopularity:%.6f' %
                                               (row[0], row[1], row[2], row[3]))


