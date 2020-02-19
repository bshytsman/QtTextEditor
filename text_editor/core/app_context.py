from text_editor.interface.main_window import MainWindow
from text_editor.interface.task_handler import TaskHandler
from text_editor.state.state_master import StateMaster


class AppContext:

    def __init__(self):
        self.main_window = MainWindow(self)
        self.task_handler = TaskHandler(self)
        self.state_master = StateMaster(self)
        self.started = False
        self.active_editing = False

    def start_(self):
        self.main_window.assign_signals()
        self.main_window.show()
        self.state_master.load_app_state()
        self.state_master.start()
        self.started = True
        self.active_editing = True

    def stop_(self):
        self.state_master.stop()
        self.state_master.save_app_depot()
