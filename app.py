from flask import Flask, render_template, request
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)


# MySQL Configuration
db_config = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME")
}


COUNTRY = ["Canada", "Finland", "Italy", "Kenya", "Norway", "Singapore"]
STORE = ["Discount Stickers", "Premium Sticker Mart", "Stickers for Less"]
PRODUCT = [
    "Holographic Goose",
    "Kaggle",
    "Kaggle Tiers",
    "Kerneler",
    "Kerneler Dark Mode",
]


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html", countries=COUNTRY, stores=STORE, products=PRODUCT
    )


def insert_to_db(date, country, store, product, prediction):

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO predictions
            (date, country, store, product, prediction)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (date, country, store, product, prediction))
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        conn.close()


def fetch_frm_db():

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        select_query = """
        SELECT DISTINCT date, country, store, product, prediction
        FROM predictions 
        ORDER BY date DESC
        """
        cursor.execute(select_query)
        predictions = cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        predictions = []

    finally:
        cursor.close()
        conn.close()

    return predictions


def calculate_prediction(date, country, store, product):

    return 100


@app.route("/predict", methods=["POST"])
def predict():

    date = request.form.get("date")
    country = request.form.get("country")
    store = request.form.get("store")
    product = request.form.get("product")

    if (
        not date
        or country not in COUNTRY
        or store not in STORE
        or product not in PRODUCT
    ):
        pass
        # return render_template("error.html")
        # error page to be done

    prediction = calculate_prediction(date, country, store, product)

    insert_to_db(date, country, store, product, prediction)

    predictions = fetch_frm_db()

    return render_template("output.html", predictions=predictions)
