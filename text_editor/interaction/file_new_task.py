import os

from text_editor.state.file_save_state import FileSaveState


class FileNewTask:
    def __init__(self, app_context):
        self.app_context = app_context

    def do_new(self):
        self.app_context.active_editing = False
        state_master = self.app_context.state_master
        app_state = state_master.get_app_state()

        self.app_context.main_window.plainTextEdit.setPlainText("")
        app_state.file_save_state = FileSaveState.NEW
        file_dir = os.path.dirname(app_state.text_source_path)
        app_state.text_source_path = file_dir + "/"
        app_state.text_saved_content = ""

        state_master.save_app_state()
        self.app_context.main_window.display_file_name(app_state)
        self.app_context.active_editing = True
