# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/azzamsya/code-coba-home/skripsi/Lupv/Resources/ui/student_window.ui'
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
        self.splitter_2 = QtWidgets.QSplitter(Form)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.groupBox = QtWidgets.QGroupBox(self.splitter)
        self.groupBox.setObjectName("groupBox")
        self.all_windows_tw = QtWidgets.QTreeWidget(self.splitter)
        self.all_windows_tw.setObjectName("all_windows_tw")
        self.all_windows_tw.headerItem().setText(0, "All Windows")
        self.file_tw = QtWidgets.QTreeWidget(self.splitter)
        self.file_tw.setObjectName("file_tw")
        self.file_tw.headerItem().setText(0, "File")
        self.diff_pte = QtWidgets.QPlainTextEdit(self.splitter)
        self.diff_pte.setObjectName("diff_pte")
        self.log_tw = QtWidgets.QTreeWidget(self.splitter_2)
        self.log_tw.setObjectName("log_tw")
        self.gridLayout.addWidget(self.splitter_2, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.close_btn = QtWidgets.QPushButton(Form)
        self.close_btn.setObjectName("close_btn")
        self.horizontalLayout.addWidget(self.close_btn)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "GroupBox"))
        self.log_tw.headerItem().setText(0, _translate("Form", "Name"))
        self.log_tw.headerItem().setText(1, _translate("Form", "Machine"))
        self.log_tw.headerItem().setText(2, _translate("Form", "New Column"))
        self.log_tw.headerItem().setText(3, _translate("Form", "SHA"))
        self.close_btn.setText(_translate("Form", "OK"))

