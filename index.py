from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

import os
import os.path
from PyQt5.uic import loadUiType
import urllib.request
import pafy
import humanize

ui, _ = loadUiType('main.ui')


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
        self.pushButton_3.clicked.connect(self.get_video_data)
        self.pushButton_4.clicked.connect(self.save_browse)
        self.pushButton_5.clicked.connect(self.download_video)

    def handle_progress(self, block_num, block_size, total_size):
        # calculate the progress
        read_data = block_num * block_size
        if total_size > 0:
            download_percentage = read_data * 100 / total_size
            self.progressBar.setValue(download_percentage)
            QApplication.processEvents()

    def handle_browse(self):
        # enable browsing to our os, pick save location
        save_location = QFileDialog.getSaveFileName(self, caption="Save As", directory=".", filter="All Files(*.*)")
        self.lineEdit_2.setText(str(save_location[0]))

    def download(self):
        # download any file
        download_url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()

        if download_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid URL or save location")
        else:
            try:
                urllib.request.urlretrieve(download_url, save_location, self.handle_progress)
            except Exception:
                QMessageBox.warning(self, "Download Error", "Provide a valid URL or save location")
                return

        QMessageBox.information(self, "Download Completed", "The Download Completed Successfully")
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.progressBar.setValue(0)

    #######################################################
    ############ Download Youtbe single Video #############

    def get_video_data(self):
        video_url = self.lineEdit_3.text()

        if video_url == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid Video URL")
        else:
            video = pafy.new(video_url)

            print(video.title)
            print(video.duration)
            print(video.author)
            print(video.length)
            print(video.viewcount)
            print(video.likes)
            print(video.dislikes)

            video_streams = video.videostreams
            for stream in video_streams:
                size = humanize.naturalsize(stream.get_filesize())
                data = "{} {} {} {}".format(stream.mediatype, stream.extension, stream.quality, size)
                self.comboBox.addItem(data)

    def download_video(self):
        video_url = self.lineEdit_3.text()
        save_location = self.lineEdit_4.text()

        if video_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid Video URL or save location")
        else:
            video = pafy.new(video_url)
            video_stream = video.videostreams
            video_quality = self.comboBox.currentIndex()
            download = video_stream[video_quality].download(filepath=save_location, callback=self.video_progress)

    def video_progress(self, total, received, ratio, rate, time):
        read_data = received
        if total > 0:
            download_percentage = read_data
            self.progressBar_2.setValue(download_percentage)
            remaining_time = round(time / 60, 2)

            self.label_5.setText(str('{} minutes remaining'.format(remaining_time)))
            QApplication.processEvents()

    def save_browse(self):
        # save location in the line edit
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")
        self.lineEdit_4.setText(str(save_location[0]))


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
