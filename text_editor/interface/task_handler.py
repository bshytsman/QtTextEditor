from text_editor.interaction.about_info_task import AboutInfoTask
from text_editor.interaction.file_new_task import FileNewTask
from text_editor.interaction.file_open_task import FileOpenTask
from text_editor.interaction.file_save import FileSaveTask
from text_editor.interaction.file_save_as_task import FileSaveAsTask


class TaskHandler:

    def __init__(self, app_context):
        self.app_context = app_context

    def file_open(self):
        task = FileOpenTask(self.app_context)
        task.do_open()

    def file_new(self):
        task = FileNewTask(self.app_context)
        task.do_new()

    def file_save(self):
        task = FileSaveTask(self.app_context)
        return task.do_save()

    def file_save_as(self):
        task = FileSaveAsTask(self.app_context)
        return task.do_save_as()

    def about_info(self):
        task = AboutInfoTask(self.app_context)
        return task.do_info()
