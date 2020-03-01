from datetime import timedelta

from text_editor.core.app_signal import AppSignal
from text_editor.core.timer_job import TimerJob
from text_editor.interface.about_dialog import AboutDialog


class AboutInfoTask:
    WAIT_TIME_MILLISECONDS = 25

    def __init__(self, app_context):
        self.app_context = app_context
        self.about_dialog = AboutDialog()
        self.timer_signal = AppSignal()
        self.job = TimerJob(interval=timedelta(milliseconds=self.WAIT_TIME_MILLISECONDS),
                            execute=self.timer_signal.emit)
        self.counter = 0
        self.counterMax = 0

    def do_info(self):
        self.locate_dialog_window()
        self.about_dialog.pushButton.released.connect(self.button_is_released)
        self.timer_signal.connect(self.timer_job)

        maximum = self.about_dialog.progressBar.size().width()
        self.about_dialog.progressBar.setMaximum(maximum)
        self.counterMax = maximum

        self.job.start()
        self.job.enable()

        self.about_dialog.exec_()

        self.job.destroy()

    def button_is_released(self):
        self.about_dialog.close()

    def locate_dialog_window(self):
        parent_pos = self.app_context.main_window.pos()
        parent_size = self.app_context.main_window.size()
        xc = parent_pos.x() + parent_size.width() // 2
        yc = parent_pos.y() + parent_size.height() // 2
        size = self.about_dialog.size()
        self.about_dialog.move(xc - size.width() // 2, yc - size.height() // 2)

    def timer_job(self):
        self.counter += 1
        if self.counter > self.counterMax:
            self.counter = 0
        self.about_dialog.progressBar.setValue(self.counter)
