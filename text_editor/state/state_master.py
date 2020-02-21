from datetime import timedelta

from text_editor.core.app_signal import AppSignal
from text_editor.core.timer_job import TimerJob
from text_editor.state.file_save_state import FileSaveState
from text_editor.state.state_persistence import StatePersistence
from text_editor.util.file_utils import FileUtils


class StateMaster:
    WAIT_TIME_MILLISECONDS = 100

    def __init__(self, app_context):
        self.app_context = app_context
        self.main_window = app_context.main_window
        self.state_persistence = StatePersistence(FileUtils.get_app_root_path())
        self.app_state = None
        self.job = TimerJob(interval=timedelta(milliseconds=StateMaster.WAIT_TIME_MILLISECONDS), execute=self.job_exec)
        self.resize_signal = AppSignal()
        self.save_state_signal = AppSignal()
        self.save_depot_signal = AppSignal()
        self.resize_count = 0
        self.reshape_count = 0
        self.save_depot_count = 0
        self.save_state_count = 0

    def start(self):
        self.resize_signal.connect(self.main_window.rearrange_components)
        self.save_state_signal.connect(self.save_app_state)
        self.save_depot_signal.connect(self.save_app_depot)
        self.job.start()
        self.job.enable()

    def stop(self):
        self.job.destroy()

    def window_moved(self):
        if self.app_context.started:
            self.reshape_count = 5

    def window_resized(self):
        if self.app_context.started:
            self.reshape_count = 5
            self.resize_count = 2

    def text_changed(self):
        if self.app_context.active_editing:
            self.save_depot_count = 20                  # will be auto-saved in 2 seconds
            if self.app_state.file_save_state != FileSaveState.NEW:
                self.main_window.display_file_name(self.app_state, not self.is_text_saved())

    def is_text_saved(self):
        return self.app_state.text_saved_content == self.main_window.plainTextEdit.toPlainText()

    def is_text_empty(self):
        return self.main_window.plainTextEdit.toPlainText() == ""

    def load_app_state(self):
        self.app_state, text_depot = self.state_persistence.load_app_state()

        if not self.app_state.valid:
            self.main_window.retrieve_window_state(self.app_state)
            self.state_persistence.save_state(self.app_state)

        self.main_window.apply_window_state(self.app_state)
        self.main_window.plainTextEdit.setPlainText(text_depot)
        self.main_window.display_file_name(self.app_state, text_depot != self.app_state.text_saved_content)

    def get_app_state(self):
        return self.app_state

    def save_app_state(self):
        self.state_persistence.save_state(self.app_state)

    def save_app_depot(self):
        text_depot = self.main_window.plainTextEdit.toPlainText()
        self.state_persistence.save_text_depot(self.app_state, text_depot)

    def job_exec(self):
        if self.reshape_count > 0:
            self.reshape_count -= 1
            if self.reshape_count == 0 and (not self.main_window.isMaximized()):
                pos = self.main_window.pos()
                self.app_state.main_X = pos.x()
                self.app_state.main_Y = pos.y()
                size = self.main_window.size()
                self.app_state.main_Width = size.width()
                self.app_state.main_Height = size.height()
                self.save_state_count = 2

        if self.resize_count > 0:
            self.resize_count -= 1
            if self.resize_count == 0:
                self.resize_signal.emit()

        if self.save_state_count > 0:
            self.save_state_count -= 1
            if self.save_state_count == 0:
                self.save_state_signal.emit()

        if self.save_depot_count > 0:
            self.save_depot_count -= 1
            if self.save_depot_count == 0:
                self.save_depot_signal.emit()
