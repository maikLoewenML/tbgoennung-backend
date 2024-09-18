import unittest
from unittest.mock import patch, Mock

import pandas as pd

import excel_product_finisher


class TestExcelProductFinisher(unittest.TestCase):
    @patch('os.listdir')
    @patch('excel_product_finisher.create_50_tags')
    @patch('excel_product_finisher.create_product_description_200_characters')
    @patch('excel_product_finisher.create_product_description_250_characters')
    @patch('pandas.read_excel')
    def test_edit_excel_sheet(self, mock_read_excel, mock_create_250_chars, mock_create_200_chars, mock_create_50_tags, mock_listdir):
        # Mock the responses from the functions
        mock_read_excel.return_value = pd.DataFrame()
        mock_create_250_chars.return_value = "Test description 250"
        mock_create_200_chars.return_value = "Test description 200"
        mock_create_50_tags.return_value = "tag1, tag2, tag3"
        mock_listdir.return_value = ['image1.png', 'image2.jpg']

        # Call the function with test data
        excel_product_finisher.edit_excel_sheet("test_directory_path", "test_niche", "test_output_file_path")

        # Assert that the mocked functions were called with the correct arguments
        mock_read_excel.assert_called_once_with("/Users/maiklowen/3_Resources/T-Shirt Business Gönnung/FlyingUploadMBA.xlsx")
        mock_create_250_chars.assert_called_with("test_niche")
        mock_create_200_chars.assert_called_with("test_niche")
        mock_create_50_tags.assert_called_with("test_niche")
        mock_listdir.assert_called_with("test_directory_path")
