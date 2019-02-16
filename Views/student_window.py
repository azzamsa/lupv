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
        Form.resize(1132, 771)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.diff_ptextexit = QtWidgets.QPlainTextEdit(Form)
        self.diff_ptextexit.setReadOnly(True)
        self.diff_ptextexit.setObjectName("diff_ptextexit")
        self.horizontalLayout.addWidget(self.diff_ptextexit)
        self.log_tree = QtWidgets.QTreeWidget(Form)
        self.log_tree.setObjectName("log_tree")
        self.log_tree.headerItem().setText(0, "Name")
        self.horizontalLayout.addWidget(self.log_tree)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.close_btn = QtWidgets.QPushButton(Form)
        self.close_btn.setObjectName("close_btn")
        self.verticalLayout_2.addWidget(self.close_btn)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Lupv"))
        self.log_tree.headerItem().setText(1, _translate("Form", "Machine"))
        self.log_tree.headerItem().setText(2, _translate("Form", "Bar"))
        self.log_tree.headerItem().setText(3, _translate("Form", "SHA"))
        self.close_btn.setText(_translate("Form", "OK"))

