# Imports
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from flask_bcrypt import Bcrypt
import mysql.connector
import os
import logging
import config

# Initialize Flask App
app = Flask(__name__)
bcrypt = Bcrypt(app)

# Load Configuration
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["SESSION_TYPE"] = config.SESSION_TYPE
Session(app)

# Load MySQL Configuration
db_config = config.DB_CONFIG

# Set up logging configuration
if not os.path.exists("logging"):
    os.makedirs("logging")

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="logging/app.log",
    filemode="a",
)

# Load constants for form data
COUNTRY = config.COUNTRY
STORE = config.STORE
PRODUCT = config.PRODUCT


# Routes
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user_name = request.form["user_name"]
        user_email = request.form["user_email"]
        user_password = request.form["user_password"]
        hashed_user_password = bcrypt.generate_password_hash(user_password).decode(
            "utf-8"
        )

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO user (user_name, user_email, user_password) VALUES (%s, %s, %s)",
                        (user_name, user_email, hashed_user_password),
                    )
                    conn.commit()

                    # Save sign-up action
                    user_id = cursor.lastrowid
                    cursor.execute(
                        "INSERT INTO activity (activity_user_id, activity_action) VALUES (%s, %s)",
                        (user_id, "Signed up"),
                    )
                    conn.commit()

                    flash("Account created successfully! Please log in.", "success")
                    return redirect(url_for("login"))

        except mysql.connector.IntegrityError:
            flash("Username or email already exists!", "danger")

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        user_name = request.form.get("user_name", "").strip()
        user_password = request.form.get("user_password", "").strip()

        if not user_name or not user_password:
            flash("Username and password are required!", "danger")
            return render_template("login.html"), 400

        with get_db_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM user WHERE user_name = %s", (user_name,))
                current_user = cursor.fetchone()

        if current_user and bcrypt.check_password_hash(
            current_user["user_password"], user_password
        ):
            # Create a user session
            session["user_name"] = current_user["user_name"]
            session["user_id"] = current_user["user_id"]

            # Save successful login action
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(
                        "INSERT INTO activity (activity_user_id, activity_action) VALUES (%s, %s)",
                        (current_user["user_id"], "Logged in"),
                    )
                    conn.commit()

            flash("Login successful!", "success")

            return redirect(url_for("index"))

        else:
            flash("Invalid username or password!", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    user_id = session.get("user_id")

    if user_id is not None:
        # Log logout action
        with get_db_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    "INSERT INTO activity (activity_user_id, activity_action) VALUES (%s, %s)",
                    (user_id, "Logged out"),
                )
                conn.commit()

    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/", methods=["GET"])
def index():
    if "user_name" not in session:
        return redirect(url_for("login"))

    return render_template(
        "index.html", countries=COUNTRY, stores=STORE, products=PRODUCT
    )


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if "user_name" not in session:
        flash("Please log in to make a prediction", "warning")
        return redirect(url_for("login"))

    user_id = session.get("user_id")

    if not user_id:
        flash("User not found. Please log in again.", "danger")
        return redirect(url_for("login"))

    if request.method == "POST":
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
            flash("All fields are required!", "danger")
            return redirect(url_for("index"))

        prediction = calculate_prediction(date, country, store, product)
        insert_to_db(user_id, date, country, store, product, prediction)

    predictions = fetch_from_db(user_id)
    return render_template("output.html", predictions=predictions)


# Helper functions
def get_db_connection():
    """Establish and return a database connection."""
    return mysql.connector.connect(**db_config)


def insert_to_db(user_id, date, country, store, product, prediction):
    """Insert sales prediction data into the database."""
    try:
        with get_db_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    """
                    INSERT INTO prediction (prediction_date, prediction_country, prediction_store, prediction_product, prediction_prediction, prediction_user_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (date, country, store, product, prediction, user_id),
                )
                conn.commit()
                flash("Prediction saved successfully!", "success")

    except mysql.connector.Error as err:
        logging.error(f"Database error: {err}")


def fetch_from_db(user_id):
    """Fetch predictions for the logged-in user."""
    predictions = []

    try:
        with get_db_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    """
                    SELECT prediction_date, prediction_country, prediction_store, prediction_product, prediction_prediction
                    FROM prediction 
                    WHERE prediction_user_id = %s 
                    ORDER BY prediction_date DESC
                    LIMIT 10
                    """,
                    (user_id,),
                )

                predictions = cursor.fetchall()

    except mysql.connector.Error as err:
        logging.error(f"Database error: {err}")
        predictions = []

    return predictions


def calculate_prediction(date, country, store, product):
    """Dummy function for sales prediction logic."""
    return 100  # Placeholder prediction


if __name__ == "__main__":
    app.run(debug=True)
