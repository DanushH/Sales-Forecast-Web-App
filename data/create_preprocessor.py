import pandas as pd
import os
import logging
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer


# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logging/create_preprocessor.log")],
)


def create_preprocessor():
    RSEED = 42

    # Define categorical and numerical features
    cat_features = ["country", "store", "product"]
    num_features = ["year", "month", "day", "day_of_week", "is_weekend"]

    # Create preprocessor pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numerical",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                num_features,
            ),
            (
                "categorical",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        (
                            "encoder",
                            OneHotEncoder(drop="first", handle_unknown="ignore"),
                        ),
                    ]
                ),
                cat_features,
            ),
        ],
        remainder="passthrough",
    )

    logging.info("Created preprocessing pipeline.")

    # Ensure preprocessor directory exists
    preprocessor_dir = "data/preprocessor"
    if not os.path.exists(preprocessor_dir):
        os.makedirs(preprocessor_dir)
        logging.info(f"Created directory: {preprocessor_dir}")

    # Save preprocessor
    preprocessor_path = f"{preprocessor_dir}/preprocessor.pkl"
    joblib.dump(preprocessor, preprocessor_path)
    logging.info(f"Saved preprocessor to {preprocessor_path}")


if __name__ == "__main__":
    create_preprocessor()
