from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

import os
import os.path
from PyQt5.uic import loadUiType
import urllib.request

ui,_ = loadUiType('main.ui')


class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.init_ui()
        self.handle_buttons()

    def init_ui(self):
        # Contain all ui changes in loading
        pass

    def handle_buttons(self):
        # handle all buttons in the app
        self.pushButton.clicked.connect(self.download)
        self.pushButton_2.clicked.connect(self.handle_browse)

    def handle_progress(self, block_num, block_size, total_size):
        # calculate the progress
        read_data = block_num * block_size
        if total_size > 0:
            download_percentage = read_data * 100 / total_size
            self.progressBar.setValue(download_percentage)

    def handle_browse(self):
        # enable browsing to our os, pick save location
        save_location = QFileDialog.getSaveFileName(self, caption="Save As", directory=".", filter="All Files(*.*)")
        self.lineEdit_2.setText(save_location)

    def download(self):
        # download any file
        download_url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()

        urllib.request.urlretrieve(download_url, save_location, self.handle_progress)

    def save_browse(self):
        # save location in the line edit
        pass


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
