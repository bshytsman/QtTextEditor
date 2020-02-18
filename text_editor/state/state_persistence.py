import os

from text_editor.state.state_record import StateRecord
from text_editor.util.file_utils import FileUtils


class StatePersistence:
    FOLDER_STATE_NAME = ".text_editor_cfg"
    FILE_STATE_NAME = "app.state"
    FILE_DEPOT_NAME = "app.depot"

    def __init__(self):
        self.root_path = FileUtils.get_app_root_path()
        self.folder_state_name = self.root_path + "/" + StatePersistence.FOLDER_STATE_NAME
        self.file_state_path = self.folder_state_name + "/" + StatePersistence.FILE_STATE_NAME
        self.file_depot_path = self.folder_state_name + "/" + StatePersistence.FILE_DEPOT_NAME

    def read_state(self):
        byte_list = None
        try:
            with open(self.file_state_path, 'br') as config:
                byte_list = config.read()
        except IOError:
            pass

        return StateRecord.from_byte_list(byte_list)

    def save_state(self, state):
        try:
            if not os.path.exists(self.folder_state_name):
                os.makedirs(self.folder_state_name)
            byte_list = state.to_dump()
            with open(self.file_state_path, 'bw') as config:
                config.write(byte_list)

        except Exception as e:
            FileUtils.display_error_dialog("Error saving state:", self.file_state_path, "Saving state error", str(e))

    def read_depot(self):
        text_depot = None
        try:
            with open(self.file_depot_path, 'tr') as depot:
                text_depot = depot.read()
        except IOError:
            pass
        return text_depot

    def save_depot(self, text_depot):
        try:
            if not os.path.exists(self.folder_state_name):
                os.makedirs(self.folder_state_name)
            with open(self.file_depot_path, 'tw') as depot:
                depot.write(text_depot)
        except Exception as e:
            FileUtils.display_error_dialog("Error saving save:", self.file_depot_path, "Saving state error", str(e))
