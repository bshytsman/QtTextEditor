from datetime import timedelta

from text_editor.core.app_signal import AppSignal
from text_editor.core.timer_job import TimerJob
from text_editor.state.file_save_state import FileSaveState
from text_editor.state.state_persistence import StatePersistence


class StateMaster():
    WAIT_TIME_MILLISECONDS = 100

    def __init__(self, app_context):
        self.app_context = app_context
        self.state_persistence = StatePersistence()
        self.app_state = None
        self.job = TimerJob(interval=timedelta(milliseconds=StateMaster.WAIT_TIME_MILLISECONDS), execute=self.job_exec)
        self.resize_signal = AppSignal()
        self.save_state_count = 0
        self.rearrange_count = 0

    def start(self):
        self.resize_signal.connect(self.app_context.main_window.rearrange_components)
        self.job.start()
        self.job.enable()

    def stop(self):
        self.job.destroy()

    def window_moved(self):
        if self.app_context.started:
            pos = self.app_context.main_window.pos()
            self.app_state.main_X = pos.x()
            self.app_state.main_Y = pos.y()
            self.save_state_count = 5

    def window_resized(self):
        if self.app_context.started:
            size = self.app_context.main_window.size()
            self.app_state.main_Width = size.width()
            self.app_state.main_Height = size.height()
            self.save_state_count = 5
            self.rearrange_count = 2

    def load_app_state(self):
        self.app_state = self.state_persistence.read_state()

        if not self.app_state.valid:
            self.app_state = self.app_context.main_window.retrieve_window_state()
            self.app_state.text_source_path = ""
            self.app_state.file_open_selected_filter = ""
            self.state_persistence.save_state(self.app_state)

        self.app_context.main_window.apply_window_state(self.app_state)

    def load_text_file(self):
        self.app_state.file_save_state = FileSaveState.NEW

        file_name = self.app_state.text_source_path

        if file_name != "":
            try:
                with open(file_name, 'tr') as src:
                    self.app_context.main_window.plainTextEdit.setPlainText(src.read())
                self.app_state.file_save_state = FileSaveState.NEVER_SAVED
            except:
                pass

        self.app_context.main_window.display_file_name(self.app_state)

    def get_app_state(self):
        return self.app_state

    def save_app_state(self):
        self.state_persistence.save_state(self.app_state)

    def job_exec(self):
        if self.save_state_count > 0:
            self.save_state_count -= 1
            if self.save_state_count == 0:
                self.state_persistence.save_state(self.app_state)

        if self.rearrange_count > 0:
            self.rearrange_count -= 1
            if self.rearrange_count == 0:
                self.resize_signal.emit()
