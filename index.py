from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

import os
from os import path
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
        self.tabWidget.tabBar().setVisible(False)
        self.apply_qdark_style()
        self.move_box_1()
        self.move_box_2()
        self.move_box_3()
        self.move_box_4()

    def handle_buttons(self):
        # handle all buttons in the app
        self.pushButton.clicked.connect(self.download)
        self.pushButton_2.clicked.connect(self.handle_browse)
        self.pushButton_3.clicked.connect(self.get_video_data)
        self.pushButton_4.clicked.connect(self.save_browse)
        self.pushButton_5.clicked.connect(self.download_video)
        self.pushButton_7.clicked.connect(self.playlist_download)
        self.pushButton_6.clicked.connect(self.playlist_save_browse)

        self.pushButton_8.clicked.connect(self.open_home)
        self.pushButton_9.clicked.connect(self.open_download)
        self.pushButton_10.clicked.connect(self.open_youtube)
        self.pushButton_11.clicked.connect(self.open_settings)
        self.pushButton_11.clicked.connect(self.open_settings)

        self.pushButton_12.clicked.connect(self.apply_darkgray_style)
        self.pushButton_13.clicked.connect(self.apply_qdark_style)
        self.pushButton_14.clicked.connect(self.apply_darkorange_style)
        self.pushButton_15.clicked.connect(self.apply_classic)

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

    #######################################################
    ############ Download Youtube playlist #############

    def playlist_download(self):
        playlist_url = self.lineEdit_5.text()
        save_location = self.lineEdit_6.text()

        if playlist_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid Playlist URL or save location")
        else:
            playlist = pafy.get_playlist(playlist_url)
            playlist_videos = playlist['items']

            self.lcdNumber_2.display(len(playlist_videos))

        os.chdir(save_location)
        if os.path.exists(str(playlist['title'])):
            os.chdir(str(playlist['title']))
        else:
            os.mkdir(str(playlist['title']))
            os.chdir(str(playlist['title']))

        current_video_in_download = 1
        quality = self.comboBox_2.currentIndex()
        QApplication.processEvents()

        for video in playlist_videos:
            current_video = video['pafy']
            current_video_stream = current_video.videostreams
            self.lcdNumber.display(current_video_in_download)
            download = current_video_stream[quality].download(callback=self.playlist_progress)
            QApplication.processEvents()

            current_video_in_download += 1

    def playlist_progress(self, total, received, ratio, rate, time):
        read_data = received
        if total > 0:
            download_percentage = read_data * 100 / total
            self.progressBar_3.setValue(download_percentage)
            remaining_time = round(time / 60, 2)

            self.label_6.setText(str('{} minutes remaining'.format(remaining_time)))
            QApplication.processEvents()

    def playlist_save_browse(self):
        playlist_save_location = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        self.lineEdit_6.setText(playlist_save_location)

    #######################################################
    ############ UI Changes Methods #############

    def open_home(self):
        self.tabWidget.setCurrentIndex(0)

    def open_download(self):
        self.tabWidget.setCurrentIndex(1)

    def open_youtube(self):
        self.tabWidget.setCurrentIndex(2)

    def open_settings(self):
        self.tabWidget.setCurrentIndex(3)

    ########################################################
    ################## App Themes #########################
    def apply_darkorange_style(self):
        style = open('styles/darkorange.css')
        style = style.read()
        self.setStyleSheet(style)

    def apply_qdark_style(self):
        style = open('styles/qdark.css')
        style = style.read()
        self.setStyleSheet(style)

    def apply_darkgray_style(self):
        style = open('styles/qdarkgrey.css')
        style = style.read()
        self.setStyleSheet(style)

    def apply_classic(self):
        style = open('styles/classic.css')
        style = style.read()
        self.setStyleSheet(style)

    ####################################################
    ################### App Animation ##################

    def move_box_1(self):
        box_animation = QPropertyAnimation(self.groupBox_12, b"geometry")
        box_animation.setDuration(2000)
        box_animation.setStartValue(QRect(0, 0, 0, 0))
        box_animation.setEndValue(QRect(100, 80, 301, 161))
        box_animation.start()
        self.box_animation = box_animation

    def move_box_2(self):
        box_animation2 = QPropertyAnimation(self.groupBox_7, b"geometry")
        box_animation2.setDuration(2000)
        box_animation2.setStartValue(QRect(0, 0, 0, 0))
        box_animation2.setEndValue(QRect(500, 80, 301, 161))
        box_animation2.start()
        self.box_animation2 = box_animation2

    def move_box_3(self):
        box_animation3 = QPropertyAnimation(self.groupBox_3, b"geometry")
        box_animation3.setDuration(2000)
        box_animation3.setStartValue(QRect(0, 0, 0, 0))
        box_animation3.setEndValue(QRect(100, 310, 301, 161))
        box_animation3.start()
        self.box_animation3 = box_animation3

    def move_box_4(self):
        box_animation4 = QPropertyAnimation(self.groupBox_11, b"geometry")
        box_animation4.setDuration(2000)
        box_animation4.setStartValue(QRect(0, 0, 0, 0))
        box_animation4.setEndValue(QRect(500, 310, 301, 161))
        box_animation4.start()
        self.box_animation4 = box_animation4


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
