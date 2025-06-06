# File: test_fine_tuning.py

import unittest
from unittest.mock import patch, mock_open, MagicMock

import fine_tuning


class TestFineTuning(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='dummy data')
    @patch('openai.File.create')
    def test_upload_training_data_success(self, mock_file_create, _):
        # Mock the response of openai.File.create
        mock_response = MagicMock()
        mock_response.id = 'file-123'
        mock_file_create.return_value = mock_response

        result = fine_tuning.upload_training_data()
        self.assertEqual(result, 'file-123')

    @patch('builtins.open', new_callable=mock_open, read_data='dummy data')
    @patch('openai.File.create', side_effect=Exception('Upload failed'))
    def test_upload_training_data_failure(self, _):
        result = fine_tuning.upload_training_data()
        self.assertIsNone(result)

    @patch('openai.FineTune.create')
    @patch('fine_tuning.upload_training_data', return_value='file-123')
    def test_start_finetuning_job_success(self, mock_finetune_create):
        # Mock the response of openai.FineTune.create
        mock_response = MagicMock()
        mock_response.id = 'fine-tune-456'
        mock_finetune_create.return_value = mock_response

        result = fine_tuning.start_finetuning_job()
        self.assertEqual(result, 'fine-tune-456')

    @patch('fine_tuning.upload_training_data', return_value=None)
    def test_start_finetuning_job_failure(self):
        result = fine_tuning.start_finetuning_job()
        self.assertIsNone(result)

    @patch('openai.FineTune.list')
    def test_list_finetuning_jobs(self, mock_finetune_list):
        # Mock the response of openai.FineTune.list
        mock_response = MagicMock()
        mock_response.data = [
            {'id': 'fine-tune-456', 'status': 'pending'},
            {'id': 'fine-tune-789', 'status': 'succeeded'},
        ]
        mock_finetune_list.return_value = mock_response

        with patch('builtins.print') as mock_print:
            fine_tuning.list_finetuning_jobs()
            mock_print.assert_any_call("Current fine-tuning jobs:")
            mock_print.assert_any_call("ID: fine-tune-456, Status: pending")
            mock_print.assert_any_call("ID: fine-tune-789, Status: succeeded")


if __name__ == '__main__':
    unittest.main()
