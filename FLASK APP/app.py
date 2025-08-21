from flask import Flask, request, render_template, redirect, url_for
import config

app = Flask(__name__)

# ❌ Hardcoded login credentials
USERNAME = "admin"
PASSWORD = "password123"

# ❌ Insecure user storage (plain text, no hashing)
users = {"admin": "password123"}

# Route: Login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        # ❌ Log passwords into a file (very insecure)
        with open("login_attempts.txt", "a") as f:
            f.write(f"Username: {user}, Password: {pwd}\n")

        if user in users and users[user] == pwd:
            return redirect(url_for("dashboard", user=user))
        else:
            return "<h3>❌ Invalid Credentials</h3>"
    return render_template("login.html")

# Route: Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        new_user = request.form["username"]
        new_pass = request.form["password"]

        # ❌ Save credentials in plain text
        users[new_user] = new_pass

        return f"<h2>User {new_user} signed up successfully! 🚨 (Password stored in plain text)</h2>"

    return render_template("signup.html")

# Route: Dashboard
@app.route("/dashboard")
def dashboard():
    user = request.args.get("user", "Guest")
    return render_template("dashboard.html",
                           user=user,
                           api_key=config.API_KEY,
                           db_pass=config.DB_PASSWORD)

# Route: Search (XSS vulnerability)
@app.route("/search")
def search():
    query = request.args.get("q")
    return render_template("search.html", query=query)

if __name__ == "__main__":
    app.run(debug=True)
