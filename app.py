from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from flask_bcrypt import Bcrypt
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)

bcrypt = Bcrypt(app)

# Session Configuration
app.config["SECRET_KEY"] = os.urandom(24)
app.config["SESSION_TYPE"] = "filesystem"

# Session Initialization
Session(app)

# MySQL Configuration
db_config = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
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


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed_password),
            )
            conn.commit()
            cursor.close()
            conn.close()

            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for("login"))

        except mysql.connector.IntegrityError:
            flash("Username or email already exists!", "danger")

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and bcrypt.check_password_hash(user["password"], password):
            session["user"] = user["username"]
            flash("Login successful!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password!", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/", methods=["GET"])
def index():
    if "user" not in session:
        return redirect(url_for("login"))

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


def fetch_from_db():

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

    predictions = fetch_from_db()

    return render_template("output.html", predictions=predictions)
