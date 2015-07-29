#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
import sys
import gnupg
import datetime

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):

    def initialize(self, passphrase):
        self.password = passphrase
        self.currentDate = QtCore.QDate(datetime.date.today().year,
                                        datetime.date.today().month, datetime.date.today().day)
        day = self.currentDate.day()
        month = self.currentDate.month()
        year = self.currentDate.year()
        try:
            filename = "journal_%s_%s_%s" % (day, month, year)
            datefile = open(filename, 'r')
            filecontent = self.decrypt(datefile.read(), self.password)
            datefile.close()
        except:
            filecontent = ""
        self.textEdit.setText(filecontent)

    def confirm(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setText("The entry has been modified.")
        msgBox.setInformativeText("Do you want to save your changes?")
        msgBox.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtGui.QMessageBox.Save)
        ret = msgBox.exec_()
        return ret

    def quit(self):
        content = self.textEdit.toPlainText()
        date = self.calendar1.selectedDate()
        day = date.day()
        month = date.month()
        year = date.year()
        try:
            filename = "journal_%s_%s_%s" % (day, month, year)
            datefile = open(filename, 'r')
            filecontent = self.decrypt(datefile.read(), self.password)
            datefile.close()
        except:
            filecontent = ''
        if content != filecontent:
            ret = self.confirm()
            if ret == 2048:
                self.save()
                sys.exit(0)
            elif ret == 8388608:
                sys.exit(0)
        else:
            sys.exit(0)

    def encrypt(self, text, recipient):
        gpg = gnupg.GPG()
        enc = gpg.encrypt(text, recipient)
        return str(enc)

    def decrypt(self, content, password):
        gpg = gnupg.GPG()
        orig = gpg.decrypt(content, passphrase=password)
        return str(orig)

    def edit(self):
        self.textEdit.setReadOnly(False)

    def save(self, oldDate=''):
        if oldDate != '':
            date = oldDate
        else:
            date = self.calendar1.selectedDate()
        day = date.day()
        month = date.month()
        year = date.year()
        content = self.textEdit.toPlainText()
        encryptedcontent = self.encrypt(content, 'balasankarc@autistici.org')
        filename = "journal_%s_%s_%s" % (day, month, year)
        datefile = open(filename, 'w')
        datefile.write(encryptedcontent)
        datefile.close()

    def calendarclicked(self, date):
        currentday = self.currentDate.day()
        currentmonth = self.currentDate.month()
        currentyear = self.currentDate.year()
        try:
            currentfile = open("journal_%s_%s_%s" % (currentday, currentmonth, currentyear))
            currentcontent = self.decrypt(currentfile.read(), self.password)
        except:
            currentcontent = ""
        content = self.textEdit.toPlainText()
        if content != currentcontent:
            ret = self.confirm()
            if ret == 2048:
                self.save(self.currentDate)
                day = date.day()
                month = date.month()
                year = date.year()
                try:
                    filename = "journal_%s_%s_%s" % (day, month, year)
                    datefile = open(filename, 'r')
                    filecontent = self.decrypt(datefile.read(), self.password)
                    datefile.close()
                    self.textEdit.setReadOnly(True)
                    self.btnCreate.setEnabled(False)
                    self.btnEdit.setEnabled(True)
                except:
                    self.btnCreate.setEnabled(True)
                    self.btnEdit.setEnabled(False)
                    filecontent = ""
                self.textEdit.clear()
                self.textEdit.setText(filecontent)
                self.currentDate = date

            elif ret == 8388608:
                day = date.day()
                month = date.month()
                year = date.year()
                try:
                    filename = "journal_%s_%s_%s" % (day, month, year)
                    datefile = open(filename, 'r')
                    filecontent = self.decrypt(datefile.read(), self.password)
                    datefile.close()
                    self.textEdit.setReadOnly(True)
                    self.btnCreate.setEnabled(False)
                    self.btnEdit.setEnabled(True)
                except:
                    self.btnCreate.setEnabled(True)
                    self.btnEdit.setEnabled(False)
                    filecontent = ""
                self.textEdit.clear()
                self.textEdit.setText(filecontent)
                self.currentDate = date
        else:
            day = date.day()
            month = date.month()
            year = date.year()
            try:
                filename = "journal_%s_%s_%s" % (day, month, year)
                datefile = open(filename, 'r')
                filecontent = self.decrypt(datefile.read(), self.password)
                datefile.close()
                self.textEdit.setReadOnly(True)
                self.btnCreate.setEnabled(False)
                self.btnEdit.setEnabled(True)
            except:
                self.btnCreate.setEnabled(True)
                self.btnEdit.setEnabled(False)
                filecontent = ""
            self.textEdit.clear()
            self.textEdit.setText(filecontent)
            self.currentDate = date

    def textclicked(self):
        print "Clicked"

    def setupUi(self, MainWindow, passphrase):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.calendar1 = QtGui.QCalendarWidget(self.centralwidget)
        self.calendar1.setGeometry(QtCore.QRect(20, 20, 336, 148))
        self.calendar1.setObjectName(_fromUtf8("calendar1"))
        self.calendar1.clicked.connect(self.calendarclicked)
        self.btnCreate = QtGui.QPushButton(self.centralwidget)
        self.btnCreate.setGeometry(QtCore.QRect(390, 70, 75, 24))
        self.btnCreate.setObjectName(_fromUtf8("btnCreate"))
        self.btnCreate.clicked.connect(self.edit)
        self.btnEdit = QtGui.QPushButton(self.centralwidget)
        self.btnEdit.setGeometry(QtCore.QRect(490, 70, 75, 24))
        self.btnEdit.setObjectName(_fromUtf8("btnEdit"))
        self.btnEdit.clicked.connect(self.edit)
        self.btnSave = QtGui.QPushButton(self.centralwidget)
        self.btnSave.setGeometry(QtCore.QRect(590, 70, 75, 24))
        self.btnSave.setObjectName(_fromUtf8("btnSave"))
        self.btnSave.clicked.connect(self.save)
        self.btnExit = QtGui.QPushButton(self.centralwidget)
        self.btnExit.setGeometry(QtCore.QRect(690, 70, 75, 24))
        self.btnExit.setObjectName(_fromUtf8("btnExit"))
        self.btnExit.clicked.connect(self.quit)
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 180, 751, 361))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Manjari"))
        font.setPointSize(12)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuHelp.menuAction())
        self.initialize(passphrase)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Daily Journal", None))
        self.btnCreate.setText(_translate("MainWindow", "&Create", None))
        self.btnEdit.setText(_translate("MainWindow", "&Edit", None))
        self.btnSave.setText(_translate("MainWindow", "&Save", None))
        self.btnExit.setText(_translate("MainWindow", "E&xit", None))
        self.textEdit.setToolTip(
            _translate("MainWindow", "Your Content goes here", None))
        self.calendarclicked(self.calendar1.selectedDate())
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))
