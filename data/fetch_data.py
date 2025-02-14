import os
import logging
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logging/fetch_data.log")],
)


def download_dataset():

    # Set up the Kaggle API client
    api = KaggleApi()
    api.authenticate()

    competition_name = "playground-series-s5e1"
    extract_folder = "./data/raw_data/"
    zip_file_path = f"./data/raw_data/{competition_name}.zip"

    # Create a folder for the dataset if it doesn't exist
    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)
        logging.info(f"Created directory: {extract_folder}")

    # Download the dataset
    try:
        api.competition_download_files(competition_name, path=extract_folder)
        logging.info("Dataset downloaded successfully!")
    except Exception as e:
        logging.error(f"Failed to download dataset: {e}")
        return

    # Extract the ZIP file
    try:
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(extract_folder)
        logging.info(f"Dataset extracted successfully to {extract_folder}")
    except zipfile.BadZipFile:
        logging.error(f"{zip_file_path} is not a valid ZIP file")
    except Exception as e:
        logging.error(f"Failed to extract dataset: {e}")


if __name__ == "__main__":
    download_dataset()
