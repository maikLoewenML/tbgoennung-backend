import unittest
from datetime import datetime
from unittest.mock import patch, Mock, mock_open

import main


class MockDateTime:
    @classmethod
    def now(cls):
        return datetime(2023, 1, 1)


class TestMain(unittest.TestCase):
    @patch('os.path.exists')
    @patch('requests.get')
    @patch('main.create_folder_with_date')
    @patch('main.read_first_todo_item')
    @patch('builtins.open', new_callable=mock_open)
    def test_download_image(self, mock_open, mock_read_first_todo_item, mock_create_folder_with_date, mock_get, mock_exists):
        # Mock the responses from the functions
        mock_read_first_todo_item.return_value = "test_todo_item"
        mock_create_folder_with_date.return_value = "/test/path"
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"test content"
        mock_exists.return_value = False

        # Call the function with test data
        main.download_image("test_url", "test_dateiname")

        # Assert that the mocked functions were called with the correct arguments
        mock_read_first_todo_item.assert_called_once()
        mock_create_folder_with_date.assert_called_once_with("test_todo_item")
        mock_get.assert_called_once_with("test_url")
        mock_exists.assert_called()

        # Assert that the file was written
        mock_open().write.assert_called_once_with(b"test content")

    @patch('main.press_button')
    @patch('main.job_status_retriever.wait_for_image_completion')
    @patch('main.job_status_retriever.fetch_job_details')
    @patch('main.press_upscale_button')
    @patch('main.download_image')
    def test_process_image(self, mock_download_image, mock_press_upscale_button, mock_fetch_job_details, mock_wait_for_image_completion, mock_press_button):
        # Mock the responses from the functions
        mock_press_button.return_value = {'jobid': 'test_jobid'}
        mock_fetch_job_details.return_value = {'attachments': [{'url': 'test_url'}]}
        mock_press_upscale_button.return_value = {'jobid': 'test_jobid'}

        # Call the function with test data
        main.process_image("test_initial_job_id", "test_button_name")

        # Assert that the mocked functions were called with the correct arguments
        mock_press_button.assert_called_once_with("test_initial_job_id", "test_button_name")
        mock_wait_for_image_completion.assert_called()
        mock_fetch_job_details.assert_called()
        mock_press_upscale_button.assert_called_once_with('test_jobid')
        mock_download_image.assert_called_once_with('test_url', 'download')

    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('datetime.datetime', new=MockDateTime)
    def test_create_folder_with_date(self, mock_makedirs, mock_exists):
        # Mock the responses from the functions
        mock_exists.side_effect = [False, False]  # The first call is for the base folder, the second call is for the downloads subfolder

        # Call the function with test data
        response = main.create_folder_with_date("test_todo_item")

        formatted_date = datetime.now().strftime("%Y%m%d")

        # Assert that the function returned the correct data
        expected_response = f"/Users/maiklowen/1_Projects/T-Shirt Business/{formatted_date}_test_todo_item/downloads"
        self.assertEqual(response, expected_response)

        # Assert that the mocked functions were called with the correct arguments
        mock_exists.assert_any_call(f"/Users/maiklowen/1_Projects/T-Shirt Business/{formatted_date}_test_todo_item")
        mock_exists.assert_any_call(f"/Users/maiklowen/1_Projects/T-Shirt Business/{formatted_date}_test_todo_item/downloads")
        mock_makedirs.assert_any_call(f"/Users/maiklowen/1_Projects/T-Shirt Business/{formatted_date}_test_todo_item")
        mock_makedirs.assert_any_call(f"/Users/maiklowen/1_Projects/T-Shirt Business/{formatted_date}_test_todo_item/downloads")

    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_check_or_create_subfolder(self, mock_makedirs, mock_exists):
        # Mock the responses from the functions
        mock_exists.return_value = False  # Assume the folder does not exist

        # Call the function with test data
        response = main.check_or_create_subfolder("/Users/maiklowen/1_Projects/T-Shirt Business", "test_subfolder")

        # Assert that the function returned the correct data
        expected_response = "/Users/maiklowen/1_Projects/T-Shirt Business/test_subfolder"
        self.assertEqual(response, expected_response)

        # Assert that the mocked functions were called with the correct arguments
        mock_exists.assert_called_once_with("/Users/maiklowen/1_Projects/T-Shirt Business/test_subfolder")
        mock_makedirs.assert_called_once_with("/Users/maiklowen/1_Projects/T-Shirt Business/test_subfolder")

    @patch('main.read_first_todo_item')
    @patch('main.niche_management.get_status_of_niche')
    @patch('main.downloads_erstellen')
    @patch('main.niche_management.set_download_success')
    @patch('main.upscaling_starten')
    @patch('main.niche_management.set_upscaling_success')
    @patch('main.excel_erstellen')
    @patch('main.niche_management.set_excel_success')
    @patch('main.downloads_ordner_loeschen')
    @patch('main.niche_management.set_archive')
    def test_process_first_niche(self, mock_set_archive, mock_downloads_ordner_loeschen, mock_set_excel_success, mock_excel_erstellen, mock_set_upscaling_success, mock_upscaling_starten, mock_set_download_success, mock_downloads_erstellen, mock_get_status_of_niche, mock_read_first_todo_item):
        # Mock the responses from the functions
        mock_read_first_todo_item.return_value = "test_todo_item"
        mock_get_status_of_niche.return_value = main.niche_management.Step.TODO.value

        # Call the function with test data
        main.process_first_niche(5)

        # Assert that the mocked functions were called with the correct arguments
        mock_read_first_todo_item.assert_called_once()
        mock_get_status_of_niche.assert_called_once_with("test_todo_item")
        mock_downloads_erstellen.assert_called_once_with(5, "test_todo_item")
        mock_set_download_success.assert_called_once_with("test_todo_item")

    @patch('main.imagine.send_prompt_to_api')
    @patch('main.job_status_retriever.wait_for_image_completion')
    @patch('main.job_status_retriever.fetch_job_details')
    @patch('main.process_image')
    def test_downloads_erstellen(self, mock_process_image, mock_fetch_job_details, mock_wait_for_image_completion, mock_send_prompt_to_api):
        # Mock the responses from the functions
        mock_send_prompt_to_api.return_value = (200, "test_jobid")
        mock_fetch_job_details.return_value = {"jobid": "test_jobid"}

        # Call the function with test data
        main.downloads_erstellen(5, "test_todo_item")

        # Assert that the mocked functions were called with the correct arguments
        assert mock_send_prompt_to_api.call_count == 5
        for _ in range(5):
            mock_send_prompt_to_api.assert_any_call("test_todo_item")
        mock_wait_for_image_completion.assert_called()
        mock_fetch_job_details.assert_called()
        mock_process_image.assert_any_call("test_jobid", 'U1')
        mock_process_image.assert_any_call("test_jobid", 'U2')
        mock_process_image.assert_any_call("test_jobid", 'U3')
        mock_process_image.assert_any_call("test_jobid", 'U4')

    @patch('main.check_or_create_subfolder')
    @patch('main.process_images_in_folder')
    def test_upscaling_starten(self, mock_process_images_in_folder, mock_check_or_create_subfolder):
        # Mock the responses from the functions
        mock_check_or_create_subfolder.return_value = "/test/path"

        # Call the function
        main.upscaling_starten()

        # Assert that the mocked functions were called with the correct arguments
        mock_check_or_create_subfolder.assert_any_call(main.base_folder_path, "downloads")
        mock_check_or_create_subfolder.assert_any_call(main.base_folder_path, "processed_images")
        mock_process_images_in_folder.assert_called_once_with("/test/path", "/test/path")

    @patch('main.read_first_todo_item')
    @patch('main.excel_product_finisher.edit_excel_sheet')
    def test_excel_erstellen(self, mock_edit_excel_sheet, mock_read_first_todo_item):
        # Mock the responses from the functions
        mock_read_first_todo_item.return_value = "test_todo_item"

        # Call the function with test data
        main.excel_erstellen("/test/path")

        # Assert that the mocked functions were called with the correct arguments
        assert mock_read_first_todo_item.call_count == 2
        for _ in range(2):
            mock_read_first_todo_item.assert_any_call()
        mock_edit_excel_sheet.assert_called_once_with("/test/path", "test_todo_item", f"{main.base_folder_path}/ImportExcel.xlsx")

    @patch('os.path.exists')
    @patch('os.rmdir')
    def test_downloads_ordner_loeschen(self, mock_rmdir, mock_exists):
        # Mock the responses from the functions
        mock_exists.return_value = True

        # Call the function with test data
        main.downloads_ordner_loeschen("/test/path")

        # Assert that the mocked functions were called with the correct arguments
        mock_exists.assert_called_once_with("/test/path")
        mock_rmdir.assert_called_once_with("/test/path")