import math
import numpy as np
import joblib
import logging
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import make_pipeline
from xgboost import XGBRegressor


# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logging/train_model.log")],
)


def root_mean_squared_log_error(y_true, y_pred):

    log_true = np.log1p(y_true)

    y_pred = np.maximum(y_pred, 0)  # Ensure no negative values
    log_pred = np.log1p(y_pred)

    squared_diff = (log_true - log_pred) ** 2

    return np.sqrt(np.mean(squared_diff))


def train_model():
    RSEED = 42

    try:
        X_train, X_val, y_train, y_val = joblib.load("data/cleaned/cleaned_data.pkl")
        preprocessor = joblib.load("data/preprocessor/preprocessor.pkl")
        logging.info("Data and preprocessor loaded.")

    except FileNotFoundError as e:
        logging.error(f"File loading error: {e}")
        return

    best_params = {
        "n_estimators": 900,
        "max_depth": 10,
        "learning_rate": 0.01,
        "subsample": 0.57,
        "colsample_bytree": 0.88,
    }

    best_xgb = XGBRegressor(random_state=RSEED, **best_params)

    pipeline = make_pipeline(preprocessor, best_xgb)

    logging.info("Model training started.")

    try:
        pipeline.fit(X_train, y_train)
        logging.info("Model training ended.")

    except Exception as e:
        logging.error(f"Error during model training: {e}")
        return

    y_pred = pipeline.predict(X_val)

    xgb_rmse = math.sqrt(mean_squared_error(y_val, y_pred))
    xgb_rmsle = root_mean_squared_log_error(y_val, y_pred)

    logging.info(f"Prediction accuracy - RMSE: {xgb_rmse}")
    logging.info(f"Prediction accuracy - RMSLE: {xgb_rmsle}")

    joblib.dump(pipeline, "models/pipeline.pkl")

    logging.info("XGBoost model trained and saved.")


if __name__ == "__main__":
    train_model()
