import os
import unittest

from text_editor.state.file_save_state import FileSaveState
from text_editor.state.state_persistence import StatePersistence
from text_editor.state.state_record import StateRecord


class StatePersistenceTester(unittest.TestCase):
    TEST_SUBDIR = "test_root"
    TEST_SOURCE_FILE_NAME = "shebang.txt"

    def setUp(self):
        self.test_root_path = self.get_test_root_path()
        self.state_persistence = StatePersistence(self.test_root_path)
        self.source_path = self.test_root_path + "/" + self.TEST_SOURCE_FILE_NAME
        self.saved_content = self.read_saved_content()
        self.create_valid_state_files()

    def test_read_valid_state_files(self):
        state, text_depot = self.state_persistence.load_app_state()
        self.assertEqual(state.valid, True)
        self.assertEqual(text_depot, self.saved_content)
        self.assertEqual(state.file_save_state, FileSaveState.NEVER_SAVED)

    def test_read_valid_state_for_new_file(self):
        state, text = self.state_persistence.load_app_state()
        state.text_source_path = ""
        self.state_persistence.save_state_file(state)

        state, text_depot = self.state_persistence.load_app_state()
        self.assertEqual(state.valid, True)
        self.assertEqual(text_depot, self.saved_content)
        self.assertEqual(state.file_save_state, FileSaveState.NEW)

    def test_read_when_depot_is_not_equal_to_saved_content(self):
        state, text = self.state_persistence.load_app_state()
        updated_text = text + "\nextra line"
        self.state_persistence.save_text_depot(state, updated_text)

        state, text = self.state_persistence.load_app_state()
        self.assertEqual(state.valid, True)
        self.assertEqual(text, updated_text)
        self.assertEqual(state.file_save_state, FileSaveState.NEVER_SAVED)

    def test_read_when_state_file_is_missing(self):
        os.remove(self.state_persistence.file_state_path)

        state, text_depot = self.state_persistence.load_app_state()
        self.assertEqual(state.valid, False)
        self.assertEqual(text_depot, "")
        self.assertEqual(state.file_save_state, FileSaveState.NEW)

    def test_read_when_state_len_doesnt_match(self):
        state, text = self.state_persistence.load_app_state()
        updated_text = text + "\nextra line"
        self.state_persistence.save_text_depot(state, updated_text)

        state, text = self.state_persistence.load_app_state()
        state.text_depot_len += 1
        self.state_persistence.save_state_file(state)

        state, text = self.state_persistence.load_app_state()
        self.assertEqual(state.valid, True)
        self.assertEqual(text, self.saved_content)
        self.assertEqual(state.file_save_state, FileSaveState.NEVER_SAVED)

    def test_read_when_state_hash_doesnt_match(self):
        state, text = self.state_persistence.load_app_state()
        updated_text = text + "\nextra line"
        self.state_persistence.save_text_depot(state, updated_text)

        state, text = self.state_persistence.load_app_state()
        state.text_depot_hash += 1
        self.state_persistence.save_state_file(state)

        state, text = self.state_persistence.load_app_state()
        self.assertEqual(state.valid, True)
        self.assertNotEqual(text, updated_text)
        self.assertEqual(text, self.saved_content)
        self.assertEqual(state.file_save_state, FileSaveState.NEVER_SAVED)

    def test_read_when_depot_file_is_missing(self):
        os.remove(self.state_persistence.file_depot_path)

        state, text_depot = self.state_persistence.load_app_state()
        self.assertEqual(state.valid, True)
        self.assertEqual(text_depot, self.saved_content)
        self.assertEqual(state.file_save_state, FileSaveState.NEVER_SAVED)

    def test_read_when_source_file_is_missing(self):
        state, text_depot = self.state_persistence.load_app_state()
        state.text_source_path += "???"
        self.state_persistence.save_state_file(state)

        state, text_depot = self.state_persistence.load_app_state()
        self.assertEqual(state.valid, True)
        self.assertEqual(text_depot, self.saved_content)
        self.assertEqual(state.file_save_state, FileSaveState.NEVER_SAVED)

    def test_read_when_depot_and_source_file_are_missing(self):
        state, text_depot = self.state_persistence.load_app_state()
        state.text_source_path += "???"
        self.state_persistence.save_state_file(state)

        os.remove(self.state_persistence.file_depot_path)

        state, text_depot = self.state_persistence.load_app_state()
        self.assertEqual(state.valid, True)
        self.assertEqual(text_depot, "")
        self.assertEqual(state.file_save_state, FileSaveState.NEVER_SAVED)

    def get_test_root_path(self):
        parts = os.path.realpath(__file__).split("/")[:-1]
        str_parts = []
        for part in parts:
            str_parts.append(part)
        str_parts.append(self.TEST_SUBDIR)
        return "/".join(str_parts)

    def read_saved_content(self):
        with open(self.source_path, 'tr') as source:
            content = source.read()
        return content

    def create_valid_state_files(self):
        app_state = StateRecord()
        app_state.main_X = 10
        app_state.main_Y = 10
        app_state.main_Width = 400
        app_state.main_Height = 300
        app_state.text_source_path = self.source_path
        app_state.file_open_folder = ""
        app_state.file_open_selected_filter = ""
        app_state.text_depot_len = len(self.saved_content)
        app_state.text_depot_hash = self.state_persistence.hash_it(self.saved_content)

        outcome = self.state_persistence.save_state_file(app_state)
        if not outcome[0]:
            raise RuntimeError(outcome[1])

        outcome = self.state_persistence.save_depot_file(self.saved_content)
        if not outcome[0]:
            raise RuntimeError(outcome[1])
