from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow

from text_editor.state.file_save_state import FileSaveState
from text_editor.ui.editor import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app_context):
        QMainWindow.__init__(self)
        self.app_context = app_context
        self.setupUi(self)

    def assign_signals(self):
        self.actionOpen.triggered.connect(self.app_context.task_handler.file_open)
        self.actionNew_file.triggered.connect(self.app_context.task_handler.file_new)
        self.actionSave.triggered.connect(self.app_context.task_handler.file_save)
        self.actionSave_As.triggered.connect(self.app_context.task_handler.file_save_as)
        self.plainTextEdit.textChanged.connect(self.app_context.state_master.text_changed)
        # self.pushButton.clicked.connect(self.app_context.test_worker.button_pressed)
        pass

    def moveEvent(self, move_event):
        self.app_context.state_master.window_moved()
        move_event.ignore()

    def resizeEvent(self, resize_event):
        self.app_context.state_master.window_resized()
        resize_event.ignore()

    def retrieve_window_state(self, state):
        geo = self.geometry()
        state.main_X = geo.x()
        state.main_Y = geo.y()
        state.main_Width = geo.width()
        state.main_Height = geo.height()
        state.valid = True

    def apply_window_state(self, state):
        self.move(state.main_X, state.main_Y)
        self.resize(state.main_Width, state.main_Height)
        self.rearrange_components()

    def display_file_name(self, app_state, is_changed=False):
        file_name = "[new]"
        if app_state.file_save_state != FileSaveState.NEW:
            file_name = app_state.text_source_path
            if is_changed:
                file_name += "*"

        self.setWindowTitle(file_name)

    @pyqtSlot()
    def rearrange_components(self):
        side_gap = 9
        client_size = self.size()
        button_size = self.pushButton.size()
        status_bar_height = self.statusbar.size().height()

        x = client_size.width() - button_size.width() - side_gap
        y = client_size.height() - button_size.height() - status_bar_height - side_gap

        self.pushButton.move(x, y)

        self.plainTextEdit.move(side_gap, side_gap)
        self.plainTextEdit.resize(client_size.width() - side_gap * 2, y - side_gap * 2)
