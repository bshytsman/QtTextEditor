import os

from PyQt5.QtWidgets import QFileDialog, QMessageBox

from text_editor.state.file_save_state import FileSaveState


class FileOpenTask:

    def __init__(self, app_context):
        self.app_context = app_context
        self.filters = []
        self.filters.append("Text Files (*.txt)")
        self.filters.append("All Files (*)")

    def do_open(self):
        state_master = self.app_context.state_master
        app_state = state_master.get_app_state()

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, selected_filter = QFileDialog.getOpenFileName(
            parent=self.app_context.main_window,
            caption="",
            directory=os.path.dirname(app_state.text_source_path),
            filter=";;".join(self.filters),
            initialFilter=app_state.file_open_selected_filter,
            options=options)

        if file_name:
            edit = self.app_context.main_window.plainTextEdit
            app_state.text_source_path = file_name
            app_state.file_open_selected_filter = selected_filter

            try:
                with open(file_name, 'tr') as src:
                    edit.setPlainText(src.read())
                app_state.file_save_state = FileSaveState.NEVER_SAVED

            except Exception as e:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("File open error:")
                msg.setInformativeText(file_name)
                msg.setWindowTitle("File open")
                msg.setDetailedText(str(e))
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

                edit.setPlainText("")
                app_state.file_save_state = FileSaveState.NEW
                app_state.text_source_path = os.path.dirname(app_state.text_source_path) + "/"

            state_master.save_app_state()
            self.app_context.main_window.display_file_name(app_state)