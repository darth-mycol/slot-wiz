from flask import Flask, jsonify, render_template, request

import data_interaction_module_aiims

app = Flask(__name__)


@app.route('/_by_date')
def by_date_look_up():
    try:
        date = request.args.get('date', 0, type=str)
        capacity = request.args.get('capacity', 0, type=int)
        department = request.args.get('department', 0, type=int)

        optimal_n, prob_range = data_interaction_module_aiims.retrieve_values_by_date(date, department, capacity)
        return jsonify(success="true", result=optimal_n, prob_range=prob_range)
    except Exception:
        return jsonify(success="false", result=-1, prob_range=-1)


@app.route('/_add_date_data')
def by_date():
    try:
        date = request.args.get('date', 0, type=str)
        department = request.args.get("department", 0, type=str)
        booked = request.args.get("daybooked", 0, type=str)
        show_up = request.args.get("dayshowup", 0, type=str)

        data_interaction_module_aiims.save_values_by_date(date, department, booked, show_up)
        return jsonify(success="true")
    except Exception:
        return jsonify(success="false")


@app.route('/_add_numbers')
def add_numbers():
    try:
        prob = request.args.get('probability', 0, type=float)
        capacity = request.args.get('capacity', 0, type=int)
        optimal_n, prob_range = data_interaction_module_aiims.retrieve_values(prob, capacity)
        return jsonify(success="true", result=optimal_n, prob_range=prob_range)
    except Exception:
        return jsonify(success="false", result=-1, prob_range=-1)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
