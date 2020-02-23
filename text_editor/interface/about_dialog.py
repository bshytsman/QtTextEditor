from PyQt5.QtWidgets import QDialog

from text_editor.ui.about import Ui_AboutDialog


class AboutDialog(QDialog, Ui_AboutDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.progressBar.setValue(0)
