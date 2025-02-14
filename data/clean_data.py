import pandas as pd
import os
import logging

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logging/clean_data.log")],
)


def clean_data():

    # Read train data
    train_data = pd.read_csv("data/raw_data/train.csv")
    logging.info("Raw data loaded successfully.")

    # Drop id column
    train_data.drop(columns=["id"], inplace=True)
    logging.info("Dropped 'id' column.")

    # Drop rows with missing target values
    initial_row_count = len(train_data)
    train_data.dropna(subset=["num_sold"], inplace=True)
    dropped_rows = initial_row_count - len(train_data)
    logging.info(f"Dropped {dropped_rows} rows with missing target values.")

    # Modify categorical data types
    for col in ["country", "store", "product"]:
        train_data[col] = train_data[col].astype("category")
        logging.info(f"Converted column '{col}' to categorical type.")

    # Extract date information
    train_data["date"] = pd.to_datetime(train_data["date"])
    train_data["year"] = train_data["date"].dt.year
    train_data["month"] = train_data["date"].dt.month
    train_data["day"] = train_data["date"].dt.day
    train_data["day_of_week"] = train_data["date"].dt.dayofweek
    train_data["is_weekend"] = train_data["day_of_week"].apply(
        lambda x: 1 if x >= 5 else 0
    )
    train_data.drop(columns=["date"], inplace=True)
    logging.info("Extracted date-related features and dropped 'date' column.")

    # Save cleaned data
    cleaned_data_folder = "data/cleaned"
    cleaned_data_file_path = f"{cleaned_data_folder}/train_cleaned.csv"

    # Create a folder for the dataset if it doesn't exist
    if not os.path.exists(cleaned_data_folder):
        os.makedirs(cleaned_data_folder)
        logging.info(f"Created directory: {cleaned_data_folder}")

    train_data.to_csv(cleaned_data_file_path, index=False)
    logging.info(f"Cleaned data saved to {cleaned_data_file_path}")


if __name__ == "__main__":
    clean_data()
