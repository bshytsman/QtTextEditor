from text_editor.interaction.file_new_task import FileNewTask
from text_editor.interaction.file_open_task import FileOpenTask


class TaskHandler:

    def __init__(self, app_context):
        self.app_context = app_context

    def file_open(self):
        task = FileOpenTask(self.app_context)
        task.do_open()

    def file_new(self):
        task = FileNewTask(self.app_context)
        task.do_new()