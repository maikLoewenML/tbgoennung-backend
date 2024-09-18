import unittest
from unittest.mock import patch, Mock
from midjouney_api_requests import job_status_retriever


class TestJobStatusRetriever(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_job_details(self, mock_get):
        # Mock the response from requests.get
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"job_id": "123"}

        # Call the function with a test job_id
        response = job_status_retriever.fetch_job_details("123")

        # Assert that the function returned the correct data
        self.assertEqual(response, {"job_id": "123"})

    @patch('requests.get')
    def test_check_image_status(self, mock_get):
        # Mock the response from requests.get
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"status": "completed"}

        # Call the function with a test job_id
        response = job_status_retriever.check_image_status("123")

        # Assert that the function returned the correct data
        self.assertEqual(response, {"status": "completed"})

    @patch('midjouney_api_requests.job_status_retriever.check_image_status')
    def test_wait_for_image_completion(self, mock_check_image_status):
        # Mock the response from check_image_status
        mock_check_image_status.return_value = {"status": "completed"}

        # Call the function with a test job_id
        job_status_retriever.wait_for_image_completion("123")

        # Assert that check_image_status was called
        mock_check_image_status.assert_called_once_with("123")
