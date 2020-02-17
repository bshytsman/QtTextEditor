from text_editor.state.state_record import StateRecord
from text_editor.util.file_utils import FileUtils


class StatePersistence:
    FILE_STATE_NAME = "text_editor.cfg"

    def __init__(self):
        self.root_path = FileUtils.get_app_root_path()
        self.file_state_path = self.root_path + "/" + StatePersistence.FILE_STATE_NAME

    def read_state(self):
        byte_list = None
        try:
            with open(self.file_state_path, 'br') as config:
                byte_list = config.read()
        except IOError:
            pass

        return StateRecord.from_byte_list(byte_list)

    def save_state(self, state):
        byte_list = state.to_dump()
        with open(self.file_state_path, 'bw') as config:
            config.write(byte_list)
