import joblib


def predict_num_sold(input_data):
    pipeline = joblib.load("models/pipeline.pkl")

    predictions = pipeline.predict(input_data)

    return predictions
