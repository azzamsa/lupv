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
        self.main_table = QtWidgets.QTableWidget(self.page)
        self.main_table.setObjectName("main_table")
        self.main_table.setColumnCount(6)
        self.main_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setHorizontalHeaderItem(5, item)
        self.main_table.horizontalHeader().setStretchLastSection(True)
        self.main_table.verticalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.main_table)
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
        self.windows_tree = QtWidgets.QTreeWidget(self.activity_splitter)
        self.windows_tree.setObjectName("windows_tree")
        self.windows_tree.headerItem().setText(0, "Windows")
        self.file_tree = QtWidgets.QTreeWidget(self.activity_splitter)
        self.file_tree.setObjectName("file_tree")
        self.file_tree.headerItem().setText(0, "Files")
        self.file_content_widget = QtWidgets.QPlainTextEdit(self.activity_splitter)
        self.file_content_widget.setMinimumSize(QtCore.QSize(0, 400))
        self.file_content_widget.setObjectName("file_content_widget")
        self.log_tree = QtWidgets.QTreeWidget(self.log_splitter)
        self.log_tree.setObjectName("log_tree")
        self.log_tree.headerItem().setText(0, "Relative Time")
        self.gridLayout.addWidget(self.log_splitter, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.page_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.suspect_table = QtWidgets.QTableWidget(self.page_3)
        self.suspect_table.setObjectName("suspect_table")
        self.suspect_table.setColumnCount(5)
        self.suspect_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.suspect_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.suspect_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.suspect_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.suspect_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.suspect_table.setHorizontalHeaderItem(4, item)
        self.suspect_table.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_3.addWidget(self.suspect_table)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.to_mainview_btn2 = QtWidgets.QPushButton(self.page_3)
        self.to_mainview_btn2.setObjectName("to_mainview_btn2")
        self.horizontalLayout_3.addWidget(self.to_mainview_btn2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.stackedWidget.addWidget(self.page_3)
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
        self.open_records_action = QtWidgets.QAction(MainWindow)
        self.open_records_action.setObjectName("open_records_action")
        self.quit_action = QtWidgets.QAction(MainWindow)
        self.quit_action.setObjectName("quit_action")
        self.toogle_light_action = QtWidgets.QAction(MainWindow)
        self.toogle_light_action.setObjectName("toogle_light_action")
        self.toogle_dark_action = QtWidgets.QAction(MainWindow)
        self.toogle_dark_action.setObjectName("toogle_dark_action")
        self.toggle_relativedate_action = QtWidgets.QAction(MainWindow)
        self.toggle_relativedate_action.setObjectName("toggle_relativedate_action")
        self.toggle_realdate_action = QtWidgets.QAction(MainWindow)
        self.toggle_realdate_action.setObjectName("toggle_realdate_action")
        self.show_editdistance_action = QtWidgets.QAction(MainWindow)
        self.show_editdistance_action.setObjectName("show_editdistance_action")
        self.show_sha_action = QtWidgets.QAction(MainWindow)
        self.show_sha_action.setObjectName("show_sha_action")
        self.hide_sha_action = QtWidgets.QAction(MainWindow)
        self.hide_sha_action.setObjectName("hide_sha_action")
        self.show_stats_action = QtWidgets.QAction(MainWindow)
        self.show_stats_action.setObjectName("show_stats_action")
        self.hide_stats_action = QtWidgets.QAction(MainWindow)
        self.hide_stats_action.setObjectName("hide_stats_action")
        self.analyze_suspect_action = QtWidgets.QAction(MainWindow)
        self.analyze_suspect_action.setObjectName("analyze_suspect_action")
        self.menuFile.addAction(self.open_records_action)
        self.menuFile.addAction(self.quit_action)
        self.menuDateTime_Format.addAction(self.toggle_relativedate_action)
        self.menuDateTime_Format.addAction(self.toggle_realdate_action)
        self.menuThemes.addSeparator()
        self.menuThemes.addSeparator()
        self.menuThemes.addAction(self.toogle_light_action)
        self.menuThemes.addAction(self.toogle_dark_action)
        self.menuSettings.addAction(self.menuThemes.menuAction())
        self.menuSettings.addAction(self.menuDateTime_Format.menuAction())
        self.menuStatistic.addSeparator()
        self.menuStatistic.addSeparator()
        self.menuStatistic.addAction(self.show_stats_action)
        self.menuStatistic.addAction(self.hide_stats_action)
        self.menuSHA.addAction(self.show_sha_action)
        self.menuSHA.addAction(self.hide_sha_action)
        self.menuAnalyze.addSeparator()
        self.menuAnalyze.addAction(self.analyze_suspect_action)
        self.menuAnalyze.addAction(self.show_editdistance_action)
        self.menuAnalyze.addAction(self.menuSHA.menuAction())
        self.menuAnalyze.addAction(self.menuStatistic.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuAnalyze.menuAction())

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Lupv"))
        self.main_table.setSortingEnabled(True)
        item = self.main_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.main_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "NIM"))
        item = self.main_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Total Records"))
        item = self.main_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Work Duration"))
        item = self.main_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "First Record"))
        item = self.main_table.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Last Record"))
        self.to_mainview_btn.setText(_translate("MainWindow", "OK"))
        self.groupBox.setTitle(_translate("MainWindow", "Activity Info"))
        self.machine_const_lbl.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Machine:</span></p></body></html>"))
        self.ip_const_lbl.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">IP Address:</span></p></body></html>"))
        self.name_const_lbl.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Name:</span></p></body></html>"))
        self.log_tree.setSortingEnabled(True)
        self.log_tree.headerItem().setText(1, _translate("MainWindow", "Date Time"))
        self.log_tree.headerItem().setText(2, _translate("MainWindow", "SHA"))
        self.log_tree.headerItem().setText(3, _translate("MainWindow", "Line Insertions"))
        self.log_tree.headerItem().setText(4, _translate("MainWindow", "Line Deletions"))
        item = self.suspect_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.suspect_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Nim"))
        item = self.suspect_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Filename"))
        item = self.suspect_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Insertion"))
        item = self.suspect_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Date"))
        self.to_mainview_btn2.setText(_translate("MainWindow", "Ok"))
        self.menuFile.setTitle(_translate("MainWindow", "Fi&le"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settin&gs"))
        self.menuDateTime_Format.setTitle(_translate("MainWindow", "&DateTime Format"))
        self.menuThemes.setTitle(_translate("MainWindow", "&Themes"))
        self.menuAnalyze.setTitle(_translate("MainWindow", "Analy&ze"))
        self.menuStatistic.setTitle(_translate("MainWindow", "Stat&istic"))
        self.menuSHA.setTitle(_translate("MainWindow", "S&HA"))
        self.open_records_action.setText(_translate("MainWindow", "&Open Records"))
        self.quit_action.setText(_translate("MainWindow", "&Quit"))
        self.toogle_light_action.setText(_translate("MainWindow", "&Light"))
        self.toogle_dark_action.setText(_translate("MainWindow", "&Dark"))
        self.toggle_relativedate_action.setText(_translate("MainWindow", "&Relative"))
        self.toggle_realdate_action.setText(_translate("MainWindow", "R&eal"))
        self.show_editdistance_action.setText(_translate("MainWindow", "&Show Editdistance"))
        self.show_sha_action.setText(_translate("MainWindow", "&Show SHA"))
        self.hide_sha_action.setText(_translate("MainWindow", "&Hide SHA"))
        self.show_stats_action.setText(_translate("MainWindow", "&Show stats"))
        self.hide_stats_action.setText(_translate("MainWindow", "&Hide stats"))
        self.analyze_suspect_action.setText(_translate("MainWindow", "&Analyze suspect"))

