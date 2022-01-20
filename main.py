# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,
                             QPushButton, QApplication, QLabel, QComboBox, QLineEdit, QFileDialog)
from PyQt5.QtGui import QFont, QIcon
from pathlib import Path
from ls_savefile_parser import *


class Interface(QWidget):

    def __init__(self):
        super().__init__()

        self.file_name = ""

        self.window_title = "LiveSplit Runs Counter"
        self.real_times = []
        self.game_times = []
        self.times_count = {}

        # label/text
        self.label = QLabel('', self)
        self.label.move(50, 20)

        # line for user input
        self.qle = QLineEdit(self)

        # button to search file
        self.btn_open_file = QPushButton('Open File', self)

        # default settings
        self.timing_method = "real"
        self.counter_type = "h"
        self.file_name = ""

        # load settings
        if exists("settings.txt"):
            f_settings = open("settings.txt", "r")

            for line in f_settings:
                line = line.strip()
                if line == "game" or line == "real":
                    self.timing_method = line
                elif line == "h" or line == "m" or line == "s":
                    self.counter_type = line
                elif line.find("file:") != -1:
                    # leave only the file name, remove "file:"
                    line = line.replace("file:", "", 1)
                    self.on_file_name_change(line)

                else:
                    print("Unknown setting: " + line)

            f_settings.close()
        else:
            print("Settings file not found, using defaults.")

        self.init_ui()

    def init_ui(self):

        QToolTip.setFont(QFont('SansSerif', 10))

        # tool top for the while ui
        self.setToolTip('gaming')

        # line for user input
        self.qle.move(50, 50)
        self.qle.setText(self.file_name)
        self.qle.textChanged[str].connect(self.on_file_name_change)

        # open file button
        self.btn_open_file.setToolTip('This will open a windows explorer window to search for a file')
        self.btn_open_file.resize(self.btn_open_file.sizeHint())
        self.btn_open_file.move(200, 50)
        self.btn_open_file.clicked.connect(self.search_file_gui)

        # combo box for timing method
        combo_t_method = QComboBox(self)
        combo_t_method.addItem('Real Time')
        combo_t_method.addItem('Game Time')
        if self.timing_method == "game":
            combo_t_method.setCurrentIndex(1)
        combo_t_method.activated[str].connect(self.on_timing_method_change)
        combo_t_method.move(50, 100)

        # combo box for time type counter
        combo_type_time = QComboBox(self)
        combo_type_time.addItem('Hours')
        combo_type_time.addItem('Minutes')
        combo_type_time.addItem('Seconds')
        if self.counter_type == "m":
            combo_type_time.setCurrentIndex(1)
        elif self.counter_type == "s":
            combo_type_time.setCurrentIndex(2)
        combo_type_time.activated[str].connect(self.on_counter_type_change)

        combo_type_time.move(50, 150)

        # button to create file
        btn_get_goals = QPushButton('Create File', self)
        btn_get_goals.setToolTip('This will create a file with the name <b>split_times.txt</b>')
        btn_get_goals.resize(btn_get_goals.sizeHint())
        btn_get_goals.move(50, 200)
        btn_get_goals.clicked.connect(lambda: self.write_output_file(self.file_name))

        # button to save settings
        btn_defaults = QPushButton('Save Defaults', self)
        btn_defaults.setToolTip('This will set default settings when opening the program')
        btn_defaults.resize(btn_defaults.sizeHint())
        btn_defaults.move(50, 300)
        btn_defaults.clicked.connect(lambda: self.save_settings())

        self.setGeometry(300, 300, 300, 400)
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle(self.window_title)
        self.show()

    def on_file_name_change(self, text):
        self.file_name = text
        self.qle.setText(text)
        # get file metadata to show in label
        metadata = get_game_data(self.file_name)
        self.label.setText(metadata["game"] + " - " + metadata["category"])
        self.label.resize(self.label.sizeHint())

    def on_timing_method_change(self, text):
        if text == "Real Time":
            self.timing_method = "real"
        elif text == "Game Time":
            self.timing_method = "game"

    def on_counter_type_change(self, text):
        if text == "Hours":
            self.counter_type = "h"
        if text == "Minutes":
            self.counter_type = "m"
        if text == "Seconds":
            self.counter_type = "s"

    def write_output_file(self, file_name):

        # get all the finished run times in 2 dicts
        self.real_times, self.game_times = get_final_run_times(file_name)

        # get all the count of the runs
        if self.timing_method == "real":
            self.times_count = count_time_barriers(self.real_times, self.counter_type)
        elif self.timing_method == "game":
            self.times_count = count_time_barriers(self.game_times, self.counter_type)

        # write them to a file that OBS reads
        write_times_file(self.times_count)

    def search_file_gui(self):

        if self.file_name != "":
            path = self.file_name.rstrip("/")
        else:
            path = str(Path.parent)
        file = QFileDialog.getOpenFileName(self, 'Open save file', path, "LiveSplit Save (*.lss)")[0]

        if file != "":
            self.on_file_name_change(file)

    def save_settings(self):

        f_settings = open("settings.txt", "w")

        f_settings.write("file:" + self.file_name + "\n" + self.timing_method + "\n" + self.counter_type + "\n")

        f_settings.close()

        return


def main():
    app = QApplication(sys.argv)
    ex = Interface()
    sys.exit(app.exec_())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    main()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
