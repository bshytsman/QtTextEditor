import os

from text_editor.state.file_save_state import FileSaveState
from text_editor.state.state_record import StateRecord
from text_editor.util.file_utils import FileUtils


class StatePersistence:
    FOLDER_STATE_NAME = ".text_editor_cfg"
    FILE_STATE_NAME = "app.state"
    FILE_DEPOT_NAME = "app.depot"

    def __init__(self, root_path):
        self.folder_state_name = root_path + "/" + StatePersistence.FOLDER_STATE_NAME
        self.file_state_path = self.folder_state_name + "/" + StatePersistence.FILE_STATE_NAME
        self.file_depot_path = self.folder_state_name + "/" + StatePersistence.FILE_DEPOT_NAME

    def load_app_state(self):
        app_state = self.read_state()
        if not app_state.valid:
            app_state.use_default_values()

        text_depot = self.read_depot()
        valid = text_depot is not None
        if valid:
            valid = len(text_depot) == app_state.text_depot_len
            valid = valid and (self.hash_it(text_depot) == app_state.text_depot_hash)
        if not valid:
            text_depot = ""

        file_name = app_state.text_source_path
        app_state.text_saved_content = ""

        if file_name == "":
            app_state.file_save_state = FileSaveState.NEW
        else:
            app_state.file_save_state = FileSaveState.NEVER_SAVED
            try:
                with open(file_name, 'tr') as src:
                    saved_content = src.read()
                app_state.text_saved_content = saved_content
                if not valid:
                    text_depot = saved_content
            except IOError:
                pass

        return app_state, text_depot

    def save_text_depot(self, app_state, text):
        app_state.text_depot_len = len(text)
        app_state.text_depot_hash = self.hash_it(text)
        self.save_depot(text)
        self.save_state(app_state)

    def read_state(self):
        byte_list = None
        try:
            with open(self.file_state_path, 'br') as config:
                byte_list = config.read()
        except IOError:
            pass

        return StateRecord.from_byte_list(byte_list)

    def save_state(self, state):
        outcome = self.save_state_file(state)
        if not outcome[0]:
            FileUtils.display_error_dialog("Error saving state:", self.file_state_path, "Saving state error",
                                           outcome[1])

    def read_depot(self):
        text_depot = None
        try:
            with open(self.file_depot_path, 'tr') as depot:
                text_depot = depot.read()
        except IOError:
            pass
        return text_depot

    def save_depot(self, text_depot):
        outcome = self.save_depot_file(text_depot)
        if not outcome[0]:
            FileUtils.display_error_dialog("Error saving state:", self.file_depot_path, "Saving state error",
                                           outcome[1])

    def save_state_file(self, state):
        flag = False
        error_msg = ""
        try:
            if not os.path.exists(self.folder_state_name):
                os.makedirs(self.folder_state_name)
            byte_list = state.to_dump()
            with open(self.file_state_path, 'bw') as config:
                config.write(byte_list)
            flag = True
        except Exception as e:
            error_msg = str(e)

        return flag, error_msg

    def save_depot_file(self, text):
        flag = False
        error_msg = ""
        try:
            if not os.path.exists(self.folder_state_name):
                os.makedirs(self.folder_state_name)
            with open(self.file_depot_path, 'tw') as depot:
                depot.write(text)
            flag = True
        except Exception as e:
            error_msg = str(e)

        return flag, error_msg

    @staticmethod
    def hash_it(obj):
        str_value = str(obj)
        int_value = 0
        length = max(len(str_value), 100)
        for index, char in enumerate(str_value):
            int_value += ((index % length) + 1) * ord(char)
        return int_value
