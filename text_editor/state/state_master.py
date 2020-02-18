from datetime import timedelta

from text_editor.core.app_signal import AppSignal
from text_editor.core.timer_job import TimerJob
from text_editor.state.file_save_state import FileSaveState
from text_editor.state.state_persistence import StatePersistence


class StateMaster:
    WAIT_TIME_MILLISECONDS = 100

    def __init__(self, app_context):
        self.app_context = app_context
        self.state_persistence = StatePersistence()
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
        self.resize_signal.connect(self.app_context.main_window.rearrange_components)
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
            self.save_depot_count = 10
            if self.app_state.file_save_state != FileSaveState.NEW:
                is_changed = self.app_state.text_saved_content != \
                             self.app_context.main_window.plainTextEdit.toPlainText()
                self.app_context.main_window.display_file_name(self.app_state, is_changed)

    def load_app_state(self):
        self.app_state = self.state_persistence.read_state()

        if not self.app_state.valid:
            self.app_state = self.app_context.main_window.retrieve_window_state()
            self.app_state.text_source_path = ""
            self.app_state.file_open_folder = ""
            self.app_state.file_open_selected_filter = ""
            self.app_state.text_depot_len = 0
            self.app_state.text_depot_hash = 0
            self.state_persistence.save_state(self.app_state)

        self.app_context.main_window.apply_window_state(self.app_state)

    def load_text(self):
        text_depot, valid = self.load_app_depot()

        file_name = self.app_state.text_source_path
        self.app_state.text_saved_content = ""

        if file_name == "":
            self.app_state.file_save_state = FileSaveState.NEW
            self.app_state.text_saved_content = ""
        else:
            self.app_state.file_save_state = FileSaveState.NEVER_SAVED
            try:
                with open(file_name, 'tr') as src:
                    saved_content = src.read()
                self.app_state.text_saved_content = saved_content
                if not valid:
                    text_depot = saved_content

            except IOError:
                pass

        self.app_context.main_window.plainTextEdit.setPlainText(text_depot)
        self.app_context.main_window.display_file_name(self.app_state, text_depot != self.app_state.text_saved_content)

    def get_app_state(self):
        return self.app_state

    def save_app_state(self):
        self.state_persistence.save_state(self.app_state)

    def save_app_depot(self):
        text_depot = self.app_context.main_window.plainTextEdit.toPlainText()
        self.app_state.text_depot_len = len(text_depot)
        self.app_state.text_depot_hash = self.hash_it(text_depot)
        self.state_persistence.save_depot(text_depot)
        self.state_persistence.save_state(self.app_state)

    def load_app_depot(self):
        text_depot = self.state_persistence.read_depot()
        if text_depot is None:
            return "", False

        valid = len(text_depot) == self.app_state.text_depot_len
        valid = valid and (self.hash_it(text_depot) == self.app_state.text_depot_hash)
        if not valid:
            text_depot = ""
        return text_depot, valid

    @staticmethod
    def hash_it(obj):
        str_value = str(obj)
        int_value = 0
        length = max(len(str_value), 100)
        for index, char in enumerate(str_value):
            int_value += ((index % length) + 1) * ord(char)
        return int_value

    def job_exec(self):
        if self.reshape_count > 0:
            self.reshape_count -= 1
            if self.reshape_count == 0 and (not self.app_context.main_window.isMaximized()):
                pos = self.app_context.main_window.pos()
                self.app_state.main_X = pos.x()
                self.app_state.main_Y = pos.y()
                size = self.app_context.main_window.size()
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
