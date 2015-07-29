from journal_ui import Ui_MainWindow
from PySide import QtGui

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, sys.argv[1])
    MainWindow.show()
    sys.exit(app.exec_())
