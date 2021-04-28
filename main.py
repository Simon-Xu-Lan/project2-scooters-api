from flask import Flask, render_template, jsonify
from flask_cors import CORS

from retrieve_data import get_all, get_by_name, get_latest, get_last_hours
from retrieve_trips import get_all_trips, get_recent_trips_by_hours, get_trips_by_company, get_summary, get_trip_summary, get_trip_hours


app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/all", methods=["GET"])
def get_all_records():
    data = get_all()
    return jsonify(data=data)

@app.route("/api/company/<name>/<limit>")
def get_by_company_name(name, limit):
    return jsonify(data=get_by_name(name, limit))

@app.route("/api/latest")
def get_latest_records():
    return jsonify(data=get_latest())

@app.route("/api/recent_hours/<number>")
def get_by_hours(number):
    return jsonify(data=get_last_hours(number))

@app.route("/api/trips/all")
def get_trips():
    return jsonify(data=get_all_trips())

@app.route("/api/trips/recent_hours/<number>")
def get_recent_trips(number):
    return jsonify(data=get_recent_trips_by_hours(number))

@app.route("/api/trips/company/<name>/<number>")
def get_company_trips(name, number):
    return jsonify(data=get_trips_by_company(name, number))

@app.route("/api/trips/summary")
def get_sums():
    return jsonify(data=get_summary())

@app.route("/api/trips/trip-summary")
def get_trip_sums():
    return jsonify(data=get_trip_summary())

@app.route("/api/trips/trip-hours")
def get_trip_by_hours():
    return jsonify(data=get_trip_hours())


if __name__ == '__main__':
    app.run(debug=True)
