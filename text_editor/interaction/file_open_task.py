import os

from PyQt5.QtWidgets import QFileDialog

from text_editor.state.file_save_state import FileSaveState
from text_editor.util.file_utils import FileUtils


class FileOpenTask:

    def __init__(self, app_context):
        self.app_context = app_context

    def do_open(self):
        quit_flag = FileUtils.save_changes_dialog(self.app_context)
        if quit_flag:
            return

        state_master = self.app_context.state_master
        app_state = state_master.get_app_state()
        success_flag = False

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, selected_filter = QFileDialog.getOpenFileName(
            parent=self.app_context.main_window,
            caption="",
            directory=app_state.file_open_folder,
            filter=FileUtils.get_file_dialog_filters(),
            initialFilter=app_state.file_open_selected_filter,
            options=options)

        if file_name:
            app_state.file_open_folder = os.path.dirname(file_name)
            app_state.file_open_selected_filter = selected_filter

            try:
                with open(file_name, 'tr') as src:
                    saved_content = src.read()

                self.app_context.active_editing = False
                edit = self.app_context.main_window.plainTextEdit
                edit.setPlainText(saved_content)
                app_state.text_source_path = file_name
                app_state.file_save_state = FileSaveState.NEVER_SAVED
                app_state.text_saved_content = saved_content
                self.app_context.main_window.display_file_name(app_state)
                self.app_context.active_editing = True
                success_flag = True

            except Exception as e:
                FileUtils.display_error_dialog("File open error:", file_name, "File Open", str(e))

            if success_flag:
                state_master.save_app_depot()
            else:
                state_master.save_app_state()
