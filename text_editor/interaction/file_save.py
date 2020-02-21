from text_editor.state.file_save_state import FileSaveState
from text_editor.util.file_utils import FileUtils


class FileSaveTask:

    def __init__(self, app_context):
        self.app_context = app_context

    def do_save(self):
        state_master = self.app_context.state_master
        app_state = state_master.get_app_state()
        if app_state.file_save_state != FileSaveState.SAVED:
            return self.app_context.task_handler.file_save_as()
        else:
            flag_saved = False
            file_name = app_state.text_source_path
            try:
                text = self.app_context.main_window.plainTextEdit.toPlainText()
                with open(file_name, 'tw') as trg:
                    trg.write(text)

                app_state.text_saved_content = text
                self.app_context.main_window.display_file_name(app_state)
                flag_saved = True

            except Exception as e:
                FileUtils.display_error_dialog("File save error:", file_name, "File Save", str(e))

            return flag_saved