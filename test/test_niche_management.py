import json
import unittest
from unittest.mock import patch, mock_open

import niche_management


class TestNicheManagement(unittest.TestCase):
    def setUp(self):
        self.niche = "test_niche"
        self.data_file = "test_kanban_data.json"

        niche_management.initialize_kanban_data()

        # Beispieldaten
        self.kanban_test_data = {
            niche_management.Step.TODO.value: ["Nische1", "Niche2"],
            niche_management.Step.DOWNLOADS_ERFOLGT.value: ["Nische3"],
            niche_management.Step.UPSCALING_ERFOLGT.value: [],
            niche_management.Step.EXCEL_ERSTELLT.value: [],
            niche_management.Step.ARCHIVE.value: ["Nische4", "Nische5"]
        }

        # Speichern der Daten in einer JSON-Datei
        with open(self.data_file, 'w') as file:
            json.dump(self.kanban_test_data, file)

    @patch('niche_management.save_data')
    def test_set_download_success(self, mock_save_data):
        self.niche = "Nische2"
        niche_management.set_download_success(self.niche)
        self.assertIn(self.niche, niche_management.kanban_data[niche_management.Step.DOWNLOADS_ERFOLGT.value])
        self.assertNotIn(self.niche, niche_management.kanban_data[niche_management.Step.TODO.value])
        mock_save_data.assert_called_once()

    @patch('niche_management.save_data')
    def test_set_upscaling_success(self, mock_save_data):
        self.niche = "Nische3"
        niche_management.set_upscaling_success(self.niche)
        self.assertIn(self.niche, niche_management.kanban_data[niche_management.Step.UPSCALING_ERFOLGT.value])
        self.assertNotIn(self.niche, niche_management.kanban_data[niche_management.Step.DOWNLOADS_ERFOLGT.value])
        mock_save_data.assert_called_once()

    @patch('niche_management.save_data')
    def test_set_excel_success(self, mock_save_data):
        self.niche = "Nische4"
        niche_management.set_excel_success(self.niche)
        self.assertIn(self.niche, niche_management.kanban_data[niche_management.Step.EXCEL_ERSTELLT.value])
        self.assertNotIn(self.niche, niche_management.kanban_data[niche_management.Step.UPSCALING_ERFOLGT.value])
        mock_save_data.assert_called_once()

    @patch('niche_management.save_data')
    def test_set_archive(self, mock_save_data):
        self.niche = "Nische5"
        niche_management.set_archive(self.niche)
        self.assertIn(self.niche, niche_management.kanban_data[niche_management.Step.ARCHIVE.value])
        self.assertNotIn(self.niche, niche_management.kanban_data[niche_management.Step.EXCEL_ERSTELLT.value])
        mock_save_data.assert_called_once()

    @patch('niche_management.save_data')
    def test_add_task(self, mock_save_data):
        self.niche = "Nische6"
        niche_management.add_task(self.niche)
        mock_save_data.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_save_data(self, mock_file):
        niche_management.kanban_data = {niche_management.Step.TODO.value: ["Nische6"]}
        expected_data = json.dumps(niche_management.kanban_data)
        niche_management.save_data()
        actual_data = ''.join(call[0][0] for call in mock_file().write.call_args_list)
        self.assertEqual(expected_data, actual_data)

    from unittest.mock import patch, mock_open
    import json

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({"ToDo": ["Nische6"]}))
    def test_load_data(self, mock_file):
        result = niche_management.load_data()
        self.assertEqual(result, {"ToDo": ["Nische6"]})

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_data_file_not_found(self, mock_file):
        result = niche_management.load_data()
        self.assertEqual(result, niche_management.kanban_data)

    @patch('builtins.open', new_callable=mock_open, read_data="invalid json")
    def test_load_data_json_decode_error(self, mock_file):
        result = niche_management.load_data()
        self.assertEqual(result, niche_management.kanban_data)

    @patch('niche_management.load_data')
    def test_get_status_of_niche(self, mock_load_data):
        # Set up mock data
        mock_load_data.return_value = {
            niche_management.Step.TODO.value: ["Nische1", "Niche2"],
            niche_management.Step.DOWNLOADS_ERFOLGT.value: ["Nische3"],
            niche_management.Step.UPSCALING_ERFOLGT.value: [],
            niche_management.Step.EXCEL_ERSTELLT.value: [],
            niche_management.Step.ARCHIVE.value: ["Nische4", "Nische5"]
        }

        # Test with a niche that is in the TODO_ step
        result = niche_management.get_status_of_niche("Nische1")
        self.assertEqual(result, niche_management.Step.TODO.value)

        # Test with a niche that is in the DOWNLOADS_ERFOLGT step
        result = niche_management.get_status_of_niche("Nische3")
        self.assertEqual(result, niche_management.Step.DOWNLOADS_ERFOLGT.value)

        # Test with a niche that is in the ARCHIVE step
        result = niche_management.get_status_of_niche("Nische4")
        self.assertEqual(result, niche_management.Step.ARCHIVE.value)

        # Test with a niche that is not in any step
        result = niche_management.get_status_of_niche("Nische6")
        self.assertIsNone(result)

    def tearDown(self):
        import os
        os.remove(self.data_file)
