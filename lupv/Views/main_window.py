# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/azzamsya/code-coba-home/skripsi/Lupv/lupv/Resources/ui/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1092, 875)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.page)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.tableWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.gridLayout = QtWidgets.QGridLayout(self.page_2)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.to_mainview_btn = QtWidgets.QPushButton(self.page_2)
        self.to_mainview_btn.setMinimumSize(QtCore.QSize(100, 0))
        self.to_mainview_btn.setObjectName("to_mainview_btn")
        self.horizontalLayout_2.addWidget(self.to_mainview_btn)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.log_splitter = QtWidgets.QSplitter(self.page_2)
        self.log_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.log_splitter.setObjectName("log_splitter")
        self.activity_splitter = QtWidgets.QSplitter(self.log_splitter)
        self.activity_splitter.setOrientation(QtCore.Qt.Vertical)
        self.activity_splitter.setObjectName("activity_splitter")
        self.groupBox = QtWidgets.QGroupBox(self.activity_splitter)
        self.groupBox.setMinimumSize(QtCore.QSize(200, 100))
        self.groupBox.setObjectName("groupBox")
        self.machine_const_lbl = QtWidgets.QLabel(self.groupBox)
        self.machine_const_lbl.setGeometry(QtCore.QRect(10, 60, 71, 16))
        self.machine_const_lbl.setObjectName("machine_const_lbl")
        self.name_lbl = QtWidgets.QLabel(self.groupBox)
        self.name_lbl.setGeometry(QtCore.QRect(80, 30, 101, 16))
        self.name_lbl.setText("")
        self.name_lbl.setObjectName("name_lbl")
        self.machine_lbl = QtWidgets.QLabel(self.groupBox)
        self.machine_lbl.setGeometry(QtCore.QRect(80, 60, 101, 16))
        self.machine_lbl.setText("")
        self.machine_lbl.setObjectName("machine_lbl")
        self.ip_const_lbl = QtWidgets.QLabel(self.groupBox)
        self.ip_const_lbl.setGeometry(QtCore.QRect(190, 30, 91, 16))
        self.ip_const_lbl.setObjectName("ip_const_lbl")
        self.ip_lbl = QtWidgets.QLabel(self.groupBox)
        self.ip_lbl.setGeometry(QtCore.QRect(290, 30, 101, 16))
        self.ip_lbl.setText("")
        self.ip_lbl.setObjectName("ip_lbl")
        self.name_const_lbl = QtWidgets.QLabel(self.groupBox)
        self.name_const_lbl.setGeometry(QtCore.QRect(10, 30, 59, 14))
        self.name_const_lbl.setObjectName("name_const_lbl")
        self.all_windows_tw = QtWidgets.QTreeWidget(self.activity_splitter)
        self.all_windows_tw.setObjectName("all_windows_tw")
        self.all_windows_tw.headerItem().setText(0, "Windows")
        self.file_tw = QtWidgets.QTreeWidget(self.activity_splitter)
        self.file_tw.setObjectName("file_tw")
        self.file_tw.headerItem().setText(0, "Files")
        self.diff_pte = QtWidgets.QPlainTextEdit(self.activity_splitter)
        self.diff_pte.setMinimumSize(QtCore.QSize(0, 400))
        self.diff_pte.setObjectName("diff_pte")
        self.log_tw = QtWidgets.QTreeWidget(self.log_splitter)
        self.log_tw.setObjectName("log_tw")
        self.log_tw.headerItem().setText(0, "Relative Time")
        self.gridLayout.addWidget(self.log_splitter, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_2)
        self.horizontalLayout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1092, 19))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuDateTime_Format = QtWidgets.QMenu(self.menuSettings)
        self.menuDateTime_Format.setObjectName("menuDateTime_Format")
        self.menuThemes = QtWidgets.QMenu(self.menuSettings)
        self.menuThemes.setObjectName("menuThemes")
        self.menuAnalyze = QtWidgets.QMenu(self.menubar)
        self.menuAnalyze.setObjectName("menuAnalyze")
        self.menuStatistic = QtWidgets.QMenu(self.menuAnalyze)
        self.menuStatistic.setObjectName("menuStatistic")
        self.menuSHA = QtWidgets.QMenu(self.menuAnalyze)
        self.menuSHA.setObjectName("menuSHA")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_Records = QtWidgets.QAction(MainWindow)
        self.actionOpen_Records.setObjectName("actionOpen_Records")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionToggleLight = QtWidgets.QAction(MainWindow)
        self.actionToggleLight.setObjectName("actionToggleLight")
        self.actionToggleDark = QtWidgets.QAction(MainWindow)
        self.actionToggleDark.setObjectName("actionToggleDark")
        self.actionRelativeDate = QtWidgets.QAction(MainWindow)
        self.actionRelativeDate.setObjectName("actionRelativeDate")
        self.actionRealDate = QtWidgets.QAction(MainWindow)
        self.actionRealDate.setObjectName("actionRealDate")
        self.actionShow_Editdistance = QtWidgets.QAction(MainWindow)
        self.actionShow_Editdistance.setObjectName("actionShow_Editdistance")
        self.actionShow_SHA = QtWidgets.QAction(MainWindow)
        self.actionShow_SHA.setObjectName("actionShow_SHA")
        self.actionHide_SHA = QtWidgets.QAction(MainWindow)
        self.actionHide_SHA.setObjectName("actionHide_SHA")
        self.actionShow_stats = QtWidgets.QAction(MainWindow)
        self.actionShow_stats.setObjectName("actionShow_stats")
        self.actionHide_stats = QtWidgets.QAction(MainWindow)
        self.actionHide_stats.setObjectName("actionHide_stats")
        self.menuFile.addAction(self.actionOpen_Records)
        self.menuFile.addAction(self.actionQuit)
        self.menuDateTime_Format.addAction(self.actionRelativeDate)
        self.menuDateTime_Format.addAction(self.actionRealDate)
        self.menuThemes.addSeparator()
        self.menuThemes.addSeparator()
        self.menuThemes.addAction(self.actionToggleLight)
        self.menuThemes.addAction(self.actionToggleDark)
        self.menuSettings.addAction(self.menuThemes.menuAction())
        self.menuSettings.addAction(self.menuDateTime_Format.menuAction())
        self.menuStatistic.addSeparator()
        self.menuStatistic.addSeparator()
        self.menuStatistic.addAction(self.actionShow_stats)
        self.menuStatistic.addAction(self.actionHide_stats)
        self.menuSHA.addAction(self.actionShow_SHA)
        self.menuSHA.addAction(self.actionHide_SHA)
        self.menuAnalyze.addSeparator()
        self.menuAnalyze.addAction(self.actionShow_Editdistance)
        self.menuAnalyze.addAction(self.menuSHA.menuAction())
        self.menuAnalyze.addAction(self.menuStatistic.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuAnalyze.menuAction())

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Lupv"))
        self.tableWidget.setSortingEnabled(True)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "NIM"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Total Records"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Work Duration"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "First Record"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Last Record"))
        self.to_mainview_btn.setText(_translate("MainWindow", "OK"))
        self.groupBox.setTitle(_translate("MainWindow", "Activity Info"))
        self.machine_const_lbl.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Machine:</span></p></body></html>"))
        self.ip_const_lbl.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">IP Address:</span></p></body></html>"))
        self.name_const_lbl.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Name:</span></p></body></html>"))
        self.log_tw.setSortingEnabled(True)
        self.log_tw.headerItem().setText(1, _translate("MainWindow", "Date Time"))
        self.log_tw.headerItem().setText(2, _translate("MainWindow", "SHA"))
        self.log_tw.headerItem().setText(3, _translate("MainWindow", "Line Insertions"))
        self.log_tw.headerItem().setText(4, _translate("MainWindow", "Line Deletions"))
        self.menuFile.setTitle(_translate("MainWindow", "Fi&le"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settin&gs"))
        self.menuDateTime_Format.setTitle(_translate("MainWindow", "&DateTime Format"))
        self.menuThemes.setTitle(_translate("MainWindow", "&Themes"))
        self.menuAnalyze.setTitle(_translate("MainWindow", "Analy&ze"))
        self.menuStatistic.setTitle(_translate("MainWindow", "Stat&istic"))
        self.menuSHA.setTitle(_translate("MainWindow", "S&HA"))
        self.actionOpen_Records.setText(_translate("MainWindow", "&Open Records"))
        self.actionQuit.setText(_translate("MainWindow", "&Quit"))
        self.actionToggleLight.setText(_translate("MainWindow", "&Light"))
        self.actionToggleDark.setText(_translate("MainWindow", "&Dark"))
        self.actionRelativeDate.setText(_translate("MainWindow", "&Relative"))
        self.actionRealDate.setText(_translate("MainWindow", "R&eal"))
        self.actionShow_Editdistance.setText(_translate("MainWindow", "&Show Editdistance"))
        self.actionShow_SHA.setText(_translate("MainWindow", "&Show SHA"))
        self.actionHide_SHA.setText(_translate("MainWindow", "&Hide SHA"))
        self.actionShow_stats.setText(_translate("MainWindow", "&Show stats"))
        self.actionHide_stats.setText(_translate("MainWindow", "&Hide stats"))

