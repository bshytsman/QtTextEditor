class StateRecord:
    ENCODING = 'utf-8'

    def __init__(self):
        self.main_X = None
        self.main_Y = None
        self.main_Width = None
        self.main_Height = None
        self.text_source_path = None
        self.file_open_folder = None
        self.file_open_selected_filter = None
        self.text_depot_len = None
        self.text_depot_hash = None
        self.file_save_state = None
        self.text_saved_content = None
        self.valid = False
        self.byte_dump = None
        self.index = 0

    @staticmethod
    def from_byte_list(byte_list):
        state = StateRecord()
        if byte_list is not None:
            state.from_dump(byte_list)
        return state

    def use_default_values(self):
        self.text_source_path = ""
        self.file_open_folder = ""
        self.file_open_selected_filter = ""
        self.text_depot_len = 0
        self.text_depot_hash = 0

    def to_dump(self):
        self.byte_dump = bytearray()
        self.append_int(self.main_X)
        self.append_int(self.main_Y)
        self.append_int(self.main_Width)
        self.append_int(self.main_Height)
        self.append_string(self.text_source_path)
        self.append_string(self.file_open_folder)
        self.append_string(self.file_open_selected_filter)
        self.append_int(self.text_depot_len)
        self.append_int(self.text_depot_hash)
        return self.byte_dump

    def from_dump(self, byte_dump):
        self.valid = False
        if byte_dump is None:
            return

        self.byte_dump = byte_dump
        self.index = 0
        try:
            self.main_X = self.retrieve_int()
            self.main_Y = self.retrieve_int()
            self.main_Width = self.retrieve_int()
            self.main_Height = self.retrieve_int()
            self.text_source_path = self.retrieve_string()
            self.file_open_folder = self.retrieve_string()
            self.file_open_selected_filter = self.retrieve_string()
            self.text_depot_len = self.retrieve_int()
            self.text_depot_hash = self.retrieve_int()
        except IndexError:
            return

        self.valid = True

    def append_int(self, int_value):
        if int_value is None:
            raise ValueError("None value provided")

        length = int_value.bit_length() // 8 + 1
        self.byte_dump.extend(length.to_bytes(1, byteorder="little", signed=True))
        self.byte_dump.extend(int_value.to_bytes(length, byteorder="little", signed=True))

    def append_string(self, str_value):
        if str_value is None:
            raise ValueError("None value provided")

        byte_list = bytes(str_value, StateRecord.ENCODING)
        self.append_int(len(byte_list))
        self.byte_dump.extend(byte_list)

    def retrieve_int(self):
        return self.pull_int(self.pull_int(1))

    def retrieve_string(self):
        length = self.retrieve_int()
        if self.index + length > len(self.byte_dump):
            raise IndexError()

        chunk = self.byte_dump[self.index:self.index + length]
        str_value = chunk.decode(StateRecord.ENCODING)
        self.index += length
        return str_value

    def pull_int(self, length):
        if self.index + length > len(self.byte_dump):
            raise IndexError()

        chunk = self.byte_dump[self.index:self.index + length]
        value = int.from_bytes(chunk, byteorder="little", signed=True)
        self.index += length
        return value
