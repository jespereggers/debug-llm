import logging
from typing import Optional

import openai
import environment


def upload_training_data() -> Optional[str]:
    """
    Upload the training data file to OpenAI and return the file ID.

    :return: The file ID of the uploaded training data, or None if upload fails.
    """
    try:
        with open(environment.TRAINING_PATH, 'rb') as file:
            response = openai.File.create(
                file=file,
                purpose='fine-tune'
            )
        logging.info(f"Training data uploaded successfully. File ID: {response.id}")
        return response.id
    except Exception as e:
        logging.error(f"Failed to upload training data: {e}")
        return None


def start_finetuning_job() -> Optional[str]:
    """
    Start a fine-tuning job using the uploaded training data.

    :return: The ID of the fine-tuning job, or None if the job creation fails.
    """
    file_id = upload_training_data()
    if not file_id:
        print("File upload failed. Cannot start fine-tuning job.")
        return None

    try:
        # Create fine-tuning job
        response = openai.FineTune.create(
            training_file=file_id,
            model=environment.OPENAI_MODEL
        )
        fine_tune_id = response.id
        logging.info(f"Fine-tuning job created successfully. Job ID: {fine_tune_id}")
        return fine_tune_id
    except Exception as e:
        logging.error(f"Failed to create fine-tuning job: {e}")
        return None


def list_finetuning_jobs():
    """
    List all fine-tuning jobs and their statuses.
    """
    try:
        response = openai.FineTune.list()
        jobs = response.data
        print("Current fine-tuning jobs:")
        for job in jobs:
            print(f"ID: {job['id']}, Status: {job['status']}")
    except Exception as e:
        logging.error(f"Failed to list fine-tuning jobs: {e}")


def main():
    """
    Main function to execute the fine-tuning process.
    """
    # Set up OpenAI API key
    openai.api_key = environment.OPENAI_API_KEY

    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    # Start fine-tuning job
    fine_tune_id = start_finetuning_job()
    if fine_tune_id:
        # Optionally list fine-tuning jobs
        list_finetuning_jobs()
    else:
        print("Fine-tuning job creation failed.")


if __name__ == '__main__':
    # Warning: this costs actual money!
    main()
