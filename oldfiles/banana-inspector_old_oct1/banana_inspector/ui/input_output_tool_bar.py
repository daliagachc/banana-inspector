# Form implementation generated from reading ui file 'input_output_tool_bar.ui'
#
# Created by: PyQt6 UI code generator 6.1.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(417, 238)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.sel_out_dir = QtWidgets.QPushButton(Form)
        self.sel_out_dir.setObjectName("sel_out_dir")
        self.gridLayout_2.addWidget(self.sel_out_dir, 4, 0, 1, 1)
        self.input_dir = QtWidgets.QLineEdit(Form)
        self.input_dir.setObjectName("input_dir")
        self.gridLayout_2.addWidget(self.input_dir, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 6, 0, 1, 1)
        self.sel_input_dir = QtWidgets.QPushButton(Form)
        self.sel_input_dir.setObjectName("sel_input_dir")
        self.gridLayout_2.addWidget(self.sel_input_dir, 0, 0, 1, 1)
        self.input_file = QtWidgets.QLineEdit(Form)
        self.input_file.setObjectName("input_file")
        self.gridLayout_2.addWidget(self.input_file, 3, 0, 1, 1)
        self.sel_input_file = QtWidgets.QPushButton(Form)
        self.sel_input_file.setObjectName("sel_input_file")
        self.gridLayout_2.addWidget(self.sel_input_file, 2, 0, 1, 1)
        self.output_dir = QtWidgets.QLineEdit(Form)
        self.output_dir.setObjectName("output_dir")
        self.gridLayout_2.addWidget(self.output_dir, 5, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 1, 1, 1)

        self.retranslateUi(Form)
        self.sel_input_dir.clicked.connect(Form.sel_dir)
        self.sel_input_file.clicked.connect(Form.sel_file)
        self.sel_out_dir.clicked.connect(Form.sel_out_dir)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.sel_input_dir, self.input_dir)
        Form.setTabOrder(self.input_dir, self.sel_input_file)
        Form.setTabOrder(self.sel_input_file, self.input_file)
        Form.setTabOrder(self.input_file, self.sel_out_dir)
        Form.setTabOrder(self.sel_out_dir, self.output_dir)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.sel_out_dir.setText(_translate("Form", "Select output directory"))
        self.sel_input_dir.setText(_translate("Form", "Select input directory"))
        self.sel_input_file.setText(_translate("Form", "Select input file"))
