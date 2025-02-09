# Imports
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from flask_bcrypt import Bcrypt
import mysql.connector
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
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app.log",
)

# Load constants for form data
COUNTRY = config.COUNTRY
STORE = config.STORE
PRODUCT = config.PRODUCT


# Routes
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                        (username, email, hashed_password),
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
        username = request.form["username"]
        password = request.form["password"]

        with get_db_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()

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


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if "user" not in session:
        flash("Please log in to make a prediction", "warning")
        return redirect(url_for("login"))

    user_id = get_user_id(session.get("user"))

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


def get_user_id(username):
    """Retrieve the user ID for a given username."""
    try:
        with get_db_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()
                return user.get("id") if user else None

    except mysql.connector.Error as err:
        logging.error(f"Database error: {err}")
        return None


def insert_to_db(user_id, date, country, store, product, prediction):
    """Insert sales prediction data into the database."""
    try:
        with get_db_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    """
                    INSERT INTO predictions (user_id, date, country, store, product, prediction)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (user_id, date, country, store, product, prediction),
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
                    SELECT date, country, store, product, prediction
                    FROM predictions 
                    WHERE user_id = %s 
                    ORDER BY date DESC
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
