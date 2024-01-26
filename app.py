from flask import Flask, request, render_template, abort
import requests
from config import *

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home_page():
    if request.method == "POST":
        user_email = request.form.get("username")

        # Basic input validation
        if not user_email or not "@" in user_email:
            abort(400, "Invalid email format")

        try:
            REQUEST_URL = f"https://api.emailvalidation.io/v1/info?apikey={EMAIL_API_KEY}&email={user_email}"

            # Make API request to Email Validation API
            response = requests.get(REQUEST_URL)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()

            return render_template("index.html", data=data)
        
        except requests.exceptions.RequestException as e:
            print("Check your INTERNET CONNECTION!")
            # Server error status code
            return render_template("error.html"), 500
        
        except Exception as e:
            print("An unexpected error occurred:", str(e))
            # Server error status code
            return render_template("error.html"), 500

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
