from PyQt5.QtWidgets import QFileDialog

from text_editor.state.source_file_state import SourceFileState
from text_editor.util.file_utils import FileUtils


class FileSaveAsTask:

    def __init__(self, app_context):
        self.app_context = app_context

    def do_save_as(self):
        state_master = self.app_context.state_master
        app_state = state_master.get_app_state()
        flag_saved = False

        if app_state.file_save_state == SourceFileState.NEW:
            directory = app_state.file_open_folder
        else:
            directory = app_state.text_source_path

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, selected_filter = QFileDialog.getSaveFileName(
            parent=self.app_context.main_window,
            caption="",
            directory=directory,
            filter=FileUtils.get_file_dialog_filters(),
            initialFilter=app_state.file_open_selected_filter,
            options=options)

        if file_name:
            app_state.file_open_selected_filter = selected_filter

            try:
                text = self.app_context.main_window.plainTextEdit.toPlainText()
                with open(file_name, 'tw') as trg:
                    trg.write(text)

                app_state.text_source_path = file_name
                app_state.file_save_state = SourceFileState.SAVED
                app_state.text_saved_content = text
                self.app_context.main_window.display_file_name(app_state)
                flag_saved = True

            except Exception as e:
                FileUtils.display_error_dialog("File save error:", file_name, "File Save", str(e))

            state_master.save_app_state()

        return flag_saved
