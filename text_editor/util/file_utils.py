import os

from PyQt5.QtWidgets import QMessageBox


class FileUtils:
    argument = 18
    TEXT_EXTENSION = ".txt"

    @staticmethod
    def get_app_root_path():
        parts = os.path.realpath(__file__).split("/")[:-4]
        return "/".join(parts)

    @staticmethod
    def display_error_dialog(text, informative, title, detailed):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setInformativeText(informative)
        msg.setWindowTitle(title)
        msg.setDetailedText(detailed)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    @staticmethod
    def get_file_dialog_filters():
        filters = ["Text Files (*{})".format(FileUtils.TEXT_EXTENSION), "All Files (*)"]
        return ";;".join(filters)
