import sys

from PyQt5.QtWidgets import QApplication

from text_editor.core.app_context import AppContext

app = QApplication(sys.argv)

app_context = AppContext()
app_context.start_()

app.exec_()

app_context.stop_()
