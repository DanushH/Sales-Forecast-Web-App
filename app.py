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


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html", countries=COUNTRY, stores=STORE, products=PRODUCT
    )


@app.route("/predict", methods=["POST"])
def predict():
    if (
        not request.form.get("date")
        or request.form.get("country") not in COUNTRY
        or request.form.get("store") not in STORE
        or request.form.get("product") not in PRODUCT
    ):
        pass
        # error page to be done

    return render_template("output.html")
