import pandas as pd
import os
import logging
import joblib
from sklearn.model_selection import train_test_split

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

    # Ensure cleaned data folder exists
    cleaned_data_folder = "data/cleaned"
    if not os.path.exists(cleaned_data_folder):
        os.makedirs(cleaned_data_folder)
        logging.info(f"Created directory: {cleaned_data_folder}")

    # Separate features and target
    X = train_data.drop(columns=["num_sold"])
    y = train_data["num_sold"]

    # Split train and validation sets
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    logging.info("Split data into train and validation sets.")

    # Save cleaned data
    cleaned_data_file_path = f"{cleaned_data_folder}/cleaned_data.pkl"
    joblib.dump((X_train, X_val, y_train, y_val), cleaned_data_file_path)
    logging.info(f"Saved cleaned and split data to {cleaned_data_file_path}")


if __name__ == "__main__":
    clean_data()
