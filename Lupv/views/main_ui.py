# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1324, 927)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.page1_btn = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.page1_btn.sizePolicy().hasHeightForWidth())
        self.page1_btn.setSizePolicy(sizePolicy)
        self.page1_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.page1_btn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../img/lup.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.page1_btn.setIcon(icon)
        self.page1_btn.setIconSize(QtCore.QSize(64, 64))
        self.page1_btn.setObjectName("page1_btn")
        self.verticalLayout.addWidget(self.page1_btn)
        self.page2_btn = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.page2_btn.sizePolicy().hasHeightForWidth())
        self.page2_btn.setSizePolicy(sizePolicy)
        self.page2_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.page2_btn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../img/history.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.page2_btn.setIcon(icon1)
        self.page2_btn.setIconSize(QtCore.QSize(64, 64))
        self.page2_btn.setObjectName("page2_btn")
        self.verticalLayout.addWidget(self.page2_btn)
        self.page3_btn = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.page3_btn.sizePolicy().hasHeightForWidth())
        self.page3_btn.setSizePolicy(sizePolicy)
        self.page3_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.page3_btn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../img/search.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.page3_btn.setIcon(icon2)
        self.page3_btn.setIconSize(QtCore.QSize(64, 56))
        self.page3_btn.setObjectName("page3_btn")
        self.verticalLayout.addWidget(self.page3_btn)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2.addWidget(self.widget)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_2 = QtWidgets.QGroupBox(self.page)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 50))
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.main_reldate_rbtn = QtWidgets.QRadioButton(self.groupBox_2)
        self.main_reldate_rbtn.setObjectName("main_reldate_rbtn")
        self.horizontalLayout_8.addWidget(self.main_reldate_rbtn)
        self.main_realdate_rbtn = QtWidgets.QRadioButton(self.groupBox_2)
        self.main_realdate_rbtn.setObjectName("main_realdate_rbtn")
        self.horizontalLayout_8.addWidget(self.main_realdate_rbtn)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_8)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.main_table = QtWidgets.QTableWidget(self.page)
        self.main_table.setObjectName("main_table")
        self.main_table.setColumnCount(9)
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
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setHorizontalHeaderItem(8, item)
        self.verticalLayout_3.addWidget(self.main_table)
        self.stackedWidget.addWidget(self.page)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.gridLayout = QtWidgets.QGridLayout(self.page_3)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_3 = QtWidgets.QGroupBox(self.page_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.show_mode_rbtn = QtWidgets.QRadioButton(self.groupBox_5)
        self.show_mode_rbtn.setObjectName("show_mode_rbtn")
        self.horizontalLayout_3.addWidget(self.show_mode_rbtn)
        self.diff_mode_rbtn = QtWidgets.QRadioButton(self.groupBox_5)
        self.diff_mode_rbtn.setObjectName("diff_mode_rbtn")
        self.horizontalLayout_3.addWidget(self.diff_mode_rbtn)
        self.verticalLayout_14.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_4 = QtWidgets.QLabel(self.groupBox_5)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_15.addWidget(self.label_4)
        self.filename_combo = QtWidgets.QComboBox(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filename_combo.sizePolicy().hasHeightForWidth())
        self.filename_combo.setSizePolicy(sizePolicy)
        self.filename_combo.setObjectName("filename_combo")
        self.horizontalLayout_15.addWidget(self.filename_combo)
        self.verticalLayout_14.addLayout(self.horizontalLayout_15)
        self.verticalLayout_15.addLayout(self.verticalLayout_14)
        self.horizontalLayout_7.addWidget(self.groupBox_5)
        self.log_appearance_box = QtWidgets.QGroupBox(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.log_appearance_box.sizePolicy().hasHeightForWidth())
        self.log_appearance_box.setSizePolicy(sizePolicy)
        self.log_appearance_box.setCheckable(False)
        self.log_appearance_box.setObjectName("log_appearance_box")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.log_appearance_box)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.log_realdate_rbtn = QtWidgets.QRadioButton(self.log_appearance_box)
        self.log_realdate_rbtn.setObjectName("log_realdate_rbtn")
        self.horizontalLayout_10.addWidget(self.log_realdate_rbtn)
        self.log_reldate_rbtn = QtWidgets.QRadioButton(self.log_appearance_box)
        self.log_reldate_rbtn.setObjectName("log_reldate_rbtn")
        self.horizontalLayout_10.addWidget(self.log_reldate_rbtn)
        self.verticalLayout_4.addLayout(self.horizontalLayout_10)
        self.stats_check = QtWidgets.QCheckBox(self.log_appearance_box)
        self.stats_check.setObjectName("stats_check")
        self.verticalLayout_4.addWidget(self.stats_check)
        self.verticalLayout_16.addLayout(self.verticalLayout_4)
        self.horizontalLayout_7.addWidget(self.log_appearance_box)
        self.verticalLayout_17.addLayout(self.horizontalLayout_7)
        self.gridLayout.addWidget(self.groupBox_3, 0, 0, 1, 1)
        self.splitter_2 = QtWidgets.QSplitter(self.page_3)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.groupBox = QtWidgets.QGroupBox(self.splitter)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 100))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 100))
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout()
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.name_const_lbl = QtWidgets.QLabel(self.groupBox)
        self.name_const_lbl.setObjectName("name_const_lbl")
        self.verticalLayout_19.addWidget(self.name_const_lbl)
        self.machine_const_lbl = QtWidgets.QLabel(self.groupBox)
        self.machine_const_lbl.setObjectName("machine_const_lbl")
        self.verticalLayout_19.addWidget(self.machine_const_lbl)
        self.horizontalLayout_11.addLayout(self.verticalLayout_19)
        self.verticalLayout_18 = QtWidgets.QVBoxLayout()
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.name_lbl = QtWidgets.QLabel(self.groupBox)
        self.name_lbl.setText("")
        self.name_lbl.setObjectName("name_lbl")
        self.verticalLayout_18.addWidget(self.name_lbl)
        self.machine_lbl = QtWidgets.QLabel(self.groupBox)
        self.machine_lbl.setText("")
        self.machine_lbl.setObjectName("machine_lbl")
        self.verticalLayout_18.addWidget(self.machine_lbl)
        self.horizontalLayout_11.addLayout(self.verticalLayout_18)
        self.horizontalLayout_13.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout()
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.ip_const_lbl = QtWidgets.QLabel(self.groupBox)
        self.ip_const_lbl.setObjectName("ip_const_lbl")
        self.verticalLayout_20.addWidget(self.ip_const_lbl)
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setText("")
        self.label_10.setObjectName("label_10")
        self.verticalLayout_20.addWidget(self.label_10)
        self.horizontalLayout_12.addLayout(self.verticalLayout_20)
        self.verticalLayout_21 = QtWidgets.QVBoxLayout()
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.ip_lbl = QtWidgets.QLabel(self.groupBox)
        self.ip_lbl.setText("")
        self.ip_lbl.setObjectName("ip_lbl")
        self.verticalLayout_21.addWidget(self.ip_lbl)
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        self.label_11.setText("")
        self.label_11.setObjectName("label_11")
        self.verticalLayout_21.addWidget(self.label_11)
        self.horizontalLayout_12.addLayout(self.verticalLayout_21)
        self.horizontalLayout_13.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_14.addLayout(self.horizontalLayout_13)
        self.windows_tree = QtWidgets.QTreeWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.windows_tree.sizePolicy().hasHeightForWidth())
        self.windows_tree.setSizePolicy(sizePolicy)
        self.windows_tree.setMinimumSize(QtCore.QSize(0, 100))
        self.windows_tree.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.windows_tree.setObjectName("windows_tree")
        self.windows_tree.headerItem().setText(0, "WIndows")
        self.file_content_widget = QtWidgets.QPlainTextEdit(self.splitter)
        self.file_content_widget.setMinimumSize(QtCore.QSize(0, 400))
        self.file_content_widget.setObjectName("file_content_widget")
        self.log_tree = QtWidgets.QTreeWidget(self.splitter_2)
        self.log_tree.setObjectName("log_tree")
        self.gridLayout.addWidget(self.splitter_2, 1, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.page_4)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.tabWidget = QtWidgets.QTabWidget(self.page_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.suspects_tab = QtWidgets.QWidget()
        self.suspects_tab.setObjectName("suspects_tab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.suspects_tab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtWidgets.QLabel(self.suspects_tab)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.insertions_limit_spin = QtWidgets.QSpinBox(self.suspects_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.insertions_limit_spin.sizePolicy().hasHeightForWidth())
        self.insertions_limit_spin.setSizePolicy(sizePolicy)
        self.insertions_limit_spin.setMaximum(10000)
        self.insertions_limit_spin.setObjectName("insertions_limit_spin")
        self.horizontalLayout_4.addWidget(self.insertions_limit_spin)
        self.horizontalLayout_16.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.suspects_tab)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        self.horizontalLayout_16.addLayout(self.horizontalLayout_5)
        self.analyze_suspects_btn = QtWidgets.QPushButton(self.suspects_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.analyze_suspects_btn.sizePolicy().hasHeightForWidth())
        self.analyze_suspects_btn.setSizePolicy(sizePolicy)
        self.analyze_suspects_btn.setObjectName("analyze_suspects_btn")
        self.horizontalLayout_16.addWidget(self.analyze_suspects_btn)
        self.verticalLayout_5.addLayout(self.horizontalLayout_16)
        self.suspects_tree = QtWidgets.QTreeWidget(self.suspects_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.suspects_tree.sizePolicy().hasHeightForWidth())
        self.suspects_tree.setSizePolicy(sizePolicy)
        self.suspects_tree.setAnimated(True)
        self.suspects_tree.setObjectName("suspects_tree")
        self.suspects_tree.header().setStretchLastSection(False)
        self.verticalLayout_5.addWidget(self.suspects_tree)
        self.tabWidget.addTab(self.suspects_tab, "")
        self.windows_tab = QtWidgets.QWidget()
        self.windows_tab.setObjectName("windows_tab")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.windows_tab)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_3 = QtWidgets.QLabel(self.windows_tab)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_6.addWidget(self.label_3)
        self.windows_searchkey_widget = QtWidgets.QLineEdit(self.windows_tab)
        self.windows_searchkey_widget.setText("")
        self.windows_searchkey_widget.setObjectName("windows_searchkey_widget")
        self.horizontalLayout_6.addWidget(self.windows_searchkey_widget)
        self.windows_search_btn = QtWidgets.QPushButton(self.windows_tab)
        self.windows_search_btn.setObjectName("windows_search_btn")
        self.horizontalLayout_6.addWidget(self.windows_search_btn)
        self.verticalLayout_9.addLayout(self.horizontalLayout_6)
        self.windows_search_tree = QtWidgets.QTreeWidget(self.windows_tab)
        self.windows_search_tree.setAnimated(True)
        self.windows_search_tree.setObjectName("windows_search_tree")
        self.windows_search_tree.headerItem().setText(1, "Name")
        self.verticalLayout_9.addWidget(self.windows_search_tree)
        self.verticalLayout_10.addLayout(self.verticalLayout_9)
        self.tabWidget.addTab(self.windows_tab, "")
        self.ip_tab = QtWidgets.QWidget()
        self.ip_tab.setObjectName("ip_tab")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.ip_tab)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.group_by_ip_btn = QtWidgets.QPushButton(self.ip_tab)
        self.group_by_ip_btn.setObjectName("group_by_ip_btn")
        self.verticalLayout_11.addWidget(self.group_by_ip_btn)
        self.group_by_ip_tree = QtWidgets.QTreeWidget(self.ip_tab)
        self.group_by_ip_tree.setAnimated(True)
        self.group_by_ip_tree.setObjectName("group_by_ip_tree")
        self.group_by_ip_tree.headerItem().setText(0, "IP Address")
        self.group_by_ip_tree.headerItem().setText(2, "Student ID")
        self.verticalLayout_11.addWidget(self.group_by_ip_tree)
        self.verticalLayout_12.addLayout(self.verticalLayout_11)
        self.tabWidget.addTab(self.ip_tab, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_23 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_23.setObjectName("verticalLayout_23")
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.label_5 = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_18.addWidget(self.label_5)
        self.horizontalLayout_22.addLayout(self.horizontalLayout_18)
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.label_8 = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_19.addWidget(self.label_8)
        self.horizontalLayout_22.addLayout(self.horizontalLayout_19)
        self.horizontalLayout_24.addLayout(self.horizontalLayout_22)
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.label_7 = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_21.addWidget(self.label_7)
        self.horizontalLayout_23.addLayout(self.horizontalLayout_21)
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.label_9 = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_20.addWidget(self.label_9)
        self.horizontalLayout_23.addLayout(self.horizontalLayout_20)
        self.horizontalLayout_24.addLayout(self.horizontalLayout_23)
        self.horizontalLayout_25.addLayout(self.horizontalLayout_24)
        self.compare_editdistance_btn = QtWidgets.QPushButton(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.compare_editdistance_btn.sizePolicy().hasHeightForWidth())
        self.compare_editdistance_btn.setSizePolicy(sizePolicy)
        self.compare_editdistance_btn.setObjectName("compare_editdistance_btn")
        self.horizontalLayout_25.addWidget(self.compare_editdistance_btn)
        self.verticalLayout_23.addLayout(self.horizontalLayout_25)
        self.verticalLayout_22 = QtWidgets.QVBoxLayout()
        self.verticalLayout_22.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.verticalLayout_23.addLayout(self.verticalLayout_22)
        self.compared_ed_savegraph_btn = QtWidgets.QPushButton(self.tab)
        self.compared_ed_savegraph_btn.setObjectName("compared_ed_savegraph_btn")
        self.verticalLayout_23.addWidget(self.compared_ed_savegraph_btn)
        self.tabWidget.addTab(self.tab, "")
        self.verticalLayout_13.addWidget(self.tabWidget)
        self.stackedWidget.addWidget(self.page_4)
        self.horizontalLayout_2.addWidget(self.stackedWidget)
        self.verticalLayout_7.addLayout(self.horizontalLayout_2)
        self.spinner_stack = QtWidgets.QStackedWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinner_stack.sizePolicy().hasHeightForWidth())
        self.spinner_stack.setSizePolicy(sizePolicy)
        self.spinner_stack.setMaximumSize(QtCore.QSize(16777215, 40))
        self.spinner_stack.setObjectName("spinner_stack")
        self.page_6 = QtWidgets.QWidget()
        self.page_6.setObjectName("page_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.page_6)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.spinner_stack.addWidget(self.page_6)
        self.page_7 = QtWidgets.QWidget()
        self.page_7.setObjectName("page_7")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.page_7)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.spinner_lbl = QtWidgets.QLabel(self.page_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinner_lbl.sizePolicy().hasHeightForWidth())
        self.spinner_lbl.setSizePolicy(sizePolicy)
        self.spinner_lbl.setText("")
        self.spinner_lbl.setPixmap(QtGui.QPixmap("../img/hourglass2.svg"))
        self.spinner_lbl.setObjectName("spinner_lbl")
        self.horizontalLayout.addWidget(self.spinner_lbl)
        self.label_6 = QtWidgets.QLabel(self.page_7)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.horizontalLayout_17.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem)
        self.spinner_stack.addWidget(self.page_7)
        self.verticalLayout_7.addWidget(self.spinner_stack)
        self.verticalLayout_8.addLayout(self.verticalLayout_7)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1324, 19))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuStorage = QtWidgets.QMenu(self.menubar)
        self.menuStorage.setObjectName("menuStorage")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.open_records_action = QtWidgets.QAction(MainWindow)
        self.open_records_action.setObjectName("open_records_action")
        self.quit_action = QtWidgets.QAction(MainWindow)
        self.quit_action.setObjectName("quit_action")
        self.light_theme_action = QtWidgets.QAction(MainWindow)
        self.light_theme_action.setObjectName("light_theme_action")
        self.dark_theme_action = QtWidgets.QAction(MainWindow)
        self.dark_theme_action.setObjectName("dark_theme_action")
        self.load_editdistance_action = QtWidgets.QAction(MainWindow)
        self.load_editdistance_action.setObjectName("load_editdistance_action")
        self.export_editdistance_action = QtWidgets.QAction(MainWindow)
        self.export_editdistance_action.setObjectName("export_editdistance_action")
        self.menuMenu.addAction(self.open_records_action)
        self.menuMenu.addAction(self.quit_action)
        self.menuStorage.addAction(self.load_editdistance_action)
        self.menuStorage.addAction(self.export_editdistance_action)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuStorage.menuAction())

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.spinner_stack.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Lupv"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Appearance"))
        self.main_reldate_rbtn.setText(_translate("MainWindow", "Re&lative DateTime"))
        self.main_realdate_rbtn.setText(_translate("MainWindow", "Real &DateTime"))
        self.main_table.setSortingEnabled(True)
        item = self.main_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.main_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Student ID"))
        item = self.main_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Total Records"))
        item = self.main_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "First Record"))
        item = self.main_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "First Record"))
        item = self.main_table.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Last Record"))
        item = self.main_table.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Last Record"))
        item = self.main_table.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Work Duration"))
        item = self.main_table.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "Work Duration"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Appearance"))
        self.groupBox_5.setTitle(_translate("MainWindow", "File Contens"))
        self.show_mode_rbtn.setText(_translate("MainWindow", "Show Mode"))
        self.diff_mode_rbtn.setText(_translate("MainWindow", "&Diff Mode"))
        self.label_4.setText(_translate("MainWindow", "Filename:"))
        self.log_appearance_box.setTitle(_translate("MainWindow", "Log Appearance"))
        self.log_realdate_rbtn.setText(_translate("MainWindow", "Rea&l DateTime"))
        self.log_reldate_rbtn.setText(_translate("MainWindow", "Re&lative DateTime"))
        self.stats_check.setText(_translate("MainWindow", "Line Insertion and Deletion"))
        self.groupBox.setTitle(_translate("MainWindow", "Auth Information"))
        self.name_const_lbl.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Login Name:</span></p></body></html>"))
        self.machine_const_lbl.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Device name:</span></p></body></html>"))
        self.ip_const_lbl.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">IP Address:</span></p></body></html>"))
        self.log_tree.setSortingEnabled(True)
        self.log_tree.headerItem().setText(0, _translate("MainWindow", "Relative DateTime"))
        self.log_tree.headerItem().setText(1, _translate("MainWindow", "DateTime"))
        self.log_tree.headerItem().setText(2, _translate("MainWindow", "SHA"))
        self.log_tree.headerItem().setText(3, _translate("MainWindow", "Insertions"))
        self.log_tree.headerItem().setText(4, _translate("MainWindow", "Deletions"))
        self.label.setText(_translate("MainWindow", "Line Insetions Limit:"))
        self.label_2.setText(_translate("MainWindow", "Filename:"))
        self.analyze_suspects_btn.setText(_translate("MainWindow", "Search"))
        self.suspects_tree.headerItem().setText(0, _translate("MainWindow", "Name"))
        self.suspects_tree.headerItem().setText(1, _translate("MainWindow", "Student ID"))
        self.suspects_tree.headerItem().setText(2, _translate("MainWindow", "Filename"))
        self.suspects_tree.headerItem().setText(3, _translate("MainWindow", "Line Insertions"))
        self.suspects_tree.headerItem().setText(4, _translate("MainWindow", "DateTime"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.suspects_tab), _translate("MainWindow", "Suspects"))
        self.label_3.setText(_translate("MainWindow", "Window Name:"))
        self.windows_search_btn.setText(_translate("MainWindow", "Search"))
        self.windows_search_tree.headerItem().setText(0, _translate("MainWindow", "Window Name"))
        self.windows_search_tree.headerItem().setText(2, _translate("MainWindow", "Student ID"))
        self.windows_search_tree.headerItem().setText(3, _translate("MainWindow", "DateTime"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.windows_tab), _translate("MainWindow", "Windows"))
        self.group_by_ip_btn.setText(_translate("MainWindow", "Show all IP Addresses"))
        self.group_by_ip_tree.headerItem().setText(1, _translate("MainWindow", "Name"))
        self.group_by_ip_tree.headerItem().setText(3, _translate("MainWindow", "DateTime"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ip_tab), _translate("MainWindow", "IP Address"))
        self.label_5.setText(_translate("MainWindow", "Current Student:"))
        self.label_8.setText(_translate("MainWindow", "Filename"))
        self.label_7.setText(_translate("MainWindow", "Previous Student:"))
        self.label_9.setText(_translate("MainWindow", "Filename:"))
        self.compare_editdistance_btn.setText(_translate("MainWindow", "Show"))
        self.compared_ed_savegraph_btn.setText(_translate("MainWindow", "Save Graph"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Edit-distance"))
        self.label_6.setText(_translate("MainWindow", "working . . ."))
        self.menuMenu.setTitle(_translate("MainWindow", "Me&nu"))
        self.menuStorage.setTitle(_translate("MainWindow", "Stora&ge"))
        self.open_records_action.setText(_translate("MainWindow", "&Open Records"))
        self.quit_action.setText(_translate("MainWindow", "&Quit"))
        self.light_theme_action.setText(_translate("MainWindow", "&Light"))
        self.dark_theme_action.setText(_translate("MainWindow", "&Dark"))
        self.load_editdistance_action.setText(_translate("MainWindow", "&Load Edit-distance File"))
        self.export_editdistance_action.setText(_translate("MainWindow", "&Export Edit-distance"))

