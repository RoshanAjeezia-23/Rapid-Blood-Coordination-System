from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/donor", methods=["GET", "POST"])
def donor():
    if request.method == "POST":
        blood_group = request.form["blood_group"]
        contact_number = request.form["contact_number"]

        connection = sqlite3.connect("blood_system.db")
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO donors (blood_group, contact_number) VALUES (?, ?)",
            (blood_group, contact_number)
        )

        connection.commit()
        connection.close()

        return "Donor Registration Successful!"

    return render_template("donor.html")


@app.route("/bloodsearch", methods=["GET", "POST"])
def bloodsearch():
    donors = []

    if request.method == "POST":
        blood_group = request.form["blood_group"]

        connection = sqlite3.connect("blood_system.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT blood_group, contact_number FROM donors WHERE blood_group = ?",
            (blood_group,)
        )

        donors = cursor.fetchall()
        connection.close()

    return render_template("bloodsearch.html", donors=donors)


@app.route("/emergency", methods=["GET", "POST"])
def emergency():
    if request.method == "POST":
        blood_group = request.form["blood_group"]
        required_units = request.form["required_units"]
        hospital_name = request.form["hospital_name"]
        contact_number = request.form["contact_number"]

        connection = sqlite3.connect("blood_system.db")
        cursor = connection.cursor()

        cursor.execute(
            """INSERT INTO emergency_requests
            (blood_group, required_units, hospital_name, contact_number)
            VALUES (?, ?, ?, ?)""",
            (blood_group, required_units, hospital_name, contact_number)
        )

        connection.commit()
        connection.close()

        return "Emergency Blood Request Submitted Successfully!"

    return render_template("emergency.html")


@app.route("/admin")
def admin():
    connection = sqlite3.connect("blood_system.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM donors")
    total_donors = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM emergency_requests")
    total_requests = cursor.fetchone()[0]

    connection.close()

    return render_template(
        "admin.html",
        total_donors=total_donors,
        total_requests=total_requests
    )


@app.route("/matching", methods=["GET", "POST"])
def matching():
    donors = []
    selected_blood = ""

    if request.method == "POST":
        selected_blood = request.form["blood_group"]

        connection = sqlite3.connect("blood_system.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT blood_group, contact_number FROM donors WHERE blood_group = ?",
            (selected_blood,)
        )

        donors = cursor.fetchall()
        connection.close()

    return render_template(
        "matching.html",
        donors=donors,
        selected_blood=selected_blood
    )


if __name__ == "__main__":
    app.run(debug=True)