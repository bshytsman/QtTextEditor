import unittest

from text_editor.state.state_record import StateRecord


class StateRecordTester(unittest.TestCase):

    def setUp(self):
        self.state_rec = StateRecord()
        self.state_rec.main_X = 30
        self.state_rec.main_Y = 10
        self.state_rec.main_Width = 500
        self.state_rec.main_Height = 300
        self.state_rec.text_source_path = "/local/Users/dummy.txt"
        self.state_rec.file_open_folder = "/local/Users/"
        self.state_rec.file_open_selected_filter = "All Files (*.*)"
        self.state_rec.valid = True

    def test_dump_valid_record(self):
        dump = self.state_rec.to_dump()
        self.assertTrue(dump is not None)
        self.assertTrue(len(dump) > 10)

    def test_dump_negative_int_record(self):
        self.state_rec.main_X = -10
        dump = self.state_rec.to_dump()
        self.assertTrue(dump is not None)
        self.assertTrue(len(dump) > 10)

    def test_raise_error_for_none_int_field(self):
        state = self.state_rec
        state.main_X = None
        self.assertRaises(ValueError, state.to_dump)

    def test_raise_error_for_none_string_field(self):
        state = self.state_rec
        state.text_source_path = None
        self.assertRaises(ValueError, state.to_dump)

    def test_retrieve_from_valid_dump(self):
        dump = self.state_rec.to_dump()

        state = StateRecord()
        state.from_dump(dump)

        self.assertEqual(self.state_rec.main_X, state.main_X)
        self.assertEqual(self.state_rec.main_Y, state.main_Y)
        self.assertEqual(self.state_rec.main_Width, state.main_Width)
        self.assertEqual(self.state_rec.main_Height, state.main_Height)
        self.assertEqual(self.state_rec.text_source_path, state.text_source_path)
        self.assertEqual(self.state_rec.file_open_folder, state.file_open_folder)
        self.assertEqual(self.state_rec.file_open_selected_filter, state.file_open_selected_filter)
        self.assertEqual(self.state_rec.valid, True)

    def test_store_and_retrieve_negative_ints(self):
        self.state_rec.main_X = -10
        self.state_rec.main_Y = -100
        self.state_rec.main_Width = -1000
        self.state_rec.main_Height = -10000000

        dump = self.state_rec.to_dump()

        state = StateRecord()
        state.from_dump(dump)

        self.assertEqual(self.state_rec.main_X, state.main_X)
        self.assertEqual(self.state_rec.main_Y, state.main_Y)
        self.assertEqual(self.state_rec.main_Width, state.main_Width)
        self.assertEqual(self.state_rec.main_Height, state.main_Height)
        self.assertEqual(self.state_rec.text_source_path, state.text_source_path)
        self.assertEqual(self.state_rec.file_open_folder, state.file_open_folder)
        self.assertEqual(self.state_rec.file_open_selected_filter, state.file_open_selected_filter)
        self.assertEqual(self.state_rec.valid, True)

    def test_retrieve_from_none(self):
        state = StateRecord()
        state.from_dump(None)
        self.assertEqual(state.valid, False)

    def test_retrieve_from_invalid_dump(self):
        dump = bytearray([0, 1, 2, 3, 4])
        state = StateRecord()
        state.from_dump(dump)
        self.assertEqual(state.valid, False)

        dump = bytearray('some text here !???', StateRecord.ENCODING)
        state = StateRecord()
        state.from_dump(dump)
        self.assertEqual(state.valid, False)

    def test_retrieve_from_empty_dump(self):
        dump = bytearray(0)
        state = StateRecord()
        state.from_dump(dump)
        self.assertEqual(state.valid, False)

    def test_retrieve_from_truncated_dump(self):
        dump = self.state_rec.to_dump()
        dump = dump[:-1]
        state = StateRecord()
        state.from_dump(dump)
        self.assertEqual(state.valid, False)
