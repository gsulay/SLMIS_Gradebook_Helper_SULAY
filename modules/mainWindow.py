# Form implementation generated from reading ui file 'UI.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1182, 922)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.sections = QtWidgets.QListWidget(parent=self.centralwidget)
        self.sections.setObjectName("sections")
        self.horizontalLayout_2.addWidget(self.sections)
        self.mainFrame = QtWidgets.QFrame(parent=self.centralwidget)
        self.mainFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.mainFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.mainFrame.setObjectName("mainFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.mainFrame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=self.mainFrame)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.generateTemplateBttn = QtWidgets.QPushButton(parent=self.mainFrame)
        self.generateTemplateBttn.setObjectName("generateTemplateBttn")
        self.horizontalLayout.addWidget(self.generateTemplateBttn)
        self.loadGradeBttn = QtWidgets.QPushButton(parent=self.mainFrame)
        self.loadGradeBttn.setObjectName("loadGradeBttn")
        self.horizontalLayout.addWidget(self.loadGradeBttn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.currentWorkbookLabel = QtWidgets.QLabel(parent=self.mainFrame)
        self.currentWorkbookLabel.setObjectName("currentWorkbookLabel")
        self.verticalLayout.addWidget(self.currentWorkbookLabel)
        self.gradeView = QtWidgets.QTableView(parent=self.mainFrame)
        self.gradeView.setObjectName("gradeView")
        self.verticalLayout.addWidget(self.gradeView)
        self.gradeBttn = QtWidgets.QPushButton(parent=self.mainFrame)
        self.gradeBttn.setObjectName("gradeBttn")
        self.verticalLayout.addWidget(self.gradeBttn)
        self.progressBar = QtWidgets.QProgressBar(parent=self.mainFrame)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.horizontalLayout_2.addWidget(self.mainFrame)
        self.horizontalLayout_2.setStretch(1, 8)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1182, 21))
        self.menubar.setObjectName("menubar")
        self.menuSettings = QtWidgets.QMenu(parent=self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionRelogin = QtGui.QAction(parent=MainWindow)
        self.actionRelogin.setObjectName("actionRelogin")
        self.menuSettings.addAction(self.actionRelogin)
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Section"))
        self.generateTemplateBttn.setText(_translate("MainWindow", "Generate Template"))
        self.loadGradeBttn.setText(_translate("MainWindow", "Load Gradebook"))
        self.currentWorkbookLabel.setText(_translate("MainWindow", "Current Workbook:"))
        self.gradeBttn.setText(_translate("MainWindow", "Grade!"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionRelogin.setText(_translate("MainWindow", "Relogin"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
