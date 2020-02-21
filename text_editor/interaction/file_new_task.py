from text_editor.state.file_save_state import FileSaveState
from text_editor.util.file_utils import FileUtils


class FileNewTask:
    def __init__(self, app_context):
        self.app_context = app_context

    def do_new(self):
        state_master = self.app_context.state_master
        if state_master.is_text_empty():
            return

        quit_flag = FileUtils.save_changes_dialog(self.app_context)
        if quit_flag:
            return

        self.app_context.active_editing = False
        state_master = self.app_context.state_master
        app_state = state_master.get_app_state()

        self.app_context.main_window.plainTextEdit.setPlainText("")
        app_state.file_save_state = FileSaveState.NEW
        app_state.text_source_path = ""
        app_state.text_saved_content = ""

        state_master.save_app_depot()
        self.app_context.main_window.display_file_name(app_state)
        self.app_context.active_editing = True
