# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/azzamsya/code-coba-home/skripsi/Lupv/lupv/Resources/ui/student_window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1032, 771)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.close_btn = QtWidgets.QPushButton(Form)
        self.close_btn.setMinimumSize(QtCore.QSize(10, 0))
        self.close_btn.setObjectName("close_btn")
        self.horizontalLayout.addWidget(self.close_btn)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.splitter_2 = QtWidgets.QSplitter(Form)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.groupBox = QtWidgets.QGroupBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 85))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 8))
        self.groupBox.setBaseSize(QtCore.QSize(0, 0))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 30, 59, 14))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 71, 16))
        self.label_2.setObjectName("label_2")
        self.name_lbl = QtWidgets.QLabel(self.groupBox)
        self.name_lbl.setGeometry(QtCore.QRect(80, 30, 101, 16))
        self.name_lbl.setText("")
        self.name_lbl.setObjectName("name_lbl")
        self.machine_lbl = QtWidgets.QLabel(self.groupBox)
        self.machine_lbl.setGeometry(QtCore.QRect(80, 60, 101, 16))
        self.machine_lbl.setText("")
        self.machine_lbl.setObjectName("machine_lbl")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(190, 30, 91, 16))
        self.label_5.setObjectName("label_5")
        self.ip_lbl = QtWidgets.QLabel(self.groupBox)
        self.ip_lbl.setGeometry(QtCore.QRect(290, 30, 101, 16))
        self.ip_lbl.setText("")
        self.ip_lbl.setObjectName("ip_lbl")
        self.all_windows_tw = QtWidgets.QTreeWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.all_windows_tw.sizePolicy().hasHeightForWidth())
        self.all_windows_tw.setSizePolicy(sizePolicy)
        self.all_windows_tw.setMinimumSize(QtCore.QSize(0, 20))
        self.all_windows_tw.setMaximumSize(QtCore.QSize(16777215, 100))
        self.all_windows_tw.setObjectName("all_windows_tw")
        self.all_windows_tw.headerItem().setText(0, "Windows")
        self.file_tw = QtWidgets.QTreeWidget(self.splitter)
        self.file_tw.setMinimumSize(QtCore.QSize(0, 50))
        self.file_tw.setMaximumSize(QtCore.QSize(16777215, 100))
        self.file_tw.setObjectName("file_tw")
        self.file_tw.headerItem().setText(0, "File")
        self.diff_pte = QtWidgets.QPlainTextEdit(self.splitter)
        self.diff_pte.setObjectName("diff_pte")
        self.log_tw = QtWidgets.QTreeWidget(self.splitter_2)
        self.log_tw.setObjectName("log_tw")
        self.gridLayout.addWidget(self.splitter_2, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.close_btn.setText(_translate("Form", "OK"))
        self.groupBox.setTitle(_translate("Form", "Activity Info"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Name:</span></p></body></html>"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Machine:</span></p></body></html>"))
        self.label_5.setText(_translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">IP Address:</span></p></body></html>"))
        self.log_tw.headerItem().setText(0, _translate("Form", "Relative Time"))
        self.log_tw.headerItem().setText(1, _translate("Form", "Date Time"))
        self.log_tw.headerItem().setText(2, _translate("Form", "SHA"))

