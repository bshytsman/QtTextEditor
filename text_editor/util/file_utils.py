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
    def save_changes_dialog(app_context):
        if app_context.state_master.is_text_saved():
            return False

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Do you want to save the changes you made?")
        msg.setInformativeText("Your changes will be lost if you don't save them.")
        msg.setWindowTitle("Save your changes?")
        msg.setStandardButtons(QMessageBox.Discard | QMessageBox.Save | QMessageBox.Cancel)
        button = msg.exec_()

        if button == QMessageBox.Cancel:
            return True

        if button == QMessageBox.Save:
            if not app_context.task_handler.file_save():
                return True

        return False

    @staticmethod
    def get_file_dialog_filters():
        filters = ["Text Files (*{})".format(FileUtils.TEXT_EXTENSION), "All Files (*)"]
        return ";;".join(filters)
