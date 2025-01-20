from flask import Flask, render_template, request

app = Flask(__name__)


COUNTRY = ["Canada", "Finland", "Italy", "Kenya", "Norway", "Singapore"]
STORE = ["Discount Stickers", "Premium Sticker Mart", "Stickers for Less"]
PRODUCT = [
    "Holographic Goose",
    "Kaggle",
    "Kaggle Tiers",
    "Kerneler",
    "Kerneler Dark Mode",
]
PREDICTIONS = {}


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html", countries=COUNTRY, stores=STORE, products=PRODUCT
    )


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
        # error page to be done

    sales_prediction = 100  # code to be done

    PREDICTIONS[date] = [country, store, product, sales_prediction]

    return render_template("output.html", predictions=PREDICTIONS)
