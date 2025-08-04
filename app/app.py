from flask import Flask, render_template, request
from scraper import fetch_and_save_case_details

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("form.html")  # your input form

@app.route("/search", methods=["POST"])
def search():
    print("🧾 Request form keys:", list(request.form.keys()))
    case_type = request.form["case_type"]
    case_number = request.form["case_number"]
    year = request.form["year"]
    court_type = request.form["court_type"]
    court_code = request.form.get("court_complex")

    case_data = fetch_and_save_case_details(case_type, case_number, year, court_type, court_code)

    # if this is a list of dicts (which it is now), pass it to template
    if isinstance(case_data, dict) and case_data.get("error"):
        return render_template("result.html", cases=[], error=case_data["error"])
    
    return render_template("result.html", cases=case_data, error=None)

if __name__ == "__main__":
    app.run(debug=True)
