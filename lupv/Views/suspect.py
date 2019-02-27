# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/azzamsya/code-coba-home/skripsi/Lupv/lupv/Resources/ui/suspect.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(338, 124)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.insertion_limit_widget = QtWidgets.QLineEdit(Dialog)
        self.insertion_limit_widget.setMinimumSize(QtCore.QSize(0, 0))
        self.insertion_limit_widget.setObjectName("insertion_limit_widget")
        self.verticalLayout_2.addWidget(self.insertion_limit_widget)
        self.filename_widget = QtWidgets.QLineEdit(Dialog)
        self.filename_widget.setMinimumSize(QtCore.QSize(0, 0))
        self.filename_widget.setObjectName("filename_widget")
        self.verticalLayout_2.addWidget(self.filename_widget)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cancel_action = QtWidgets.QPushButton(Dialog)
        self.cancel_action.setObjectName("cancel_action")
        self.horizontalLayout_2.addWidget(self.cancel_action)
        self.analyze_action = QtWidgets.QPushButton(Dialog)
        self.analyze_action.setObjectName("analyze_action")
        self.horizontalLayout_2.addWidget(self.analyze_action)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Insertion Limit"))
        self.label_2.setText(_translate("Dialog", "Filename"))
        self.cancel_action.setText(_translate("Dialog", "Cancel"))
        self.analyze_action.setText(_translate("Dialog", "Analyze"))

