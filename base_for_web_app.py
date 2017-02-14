from flask import Flask, jsonify, render_template, request

import data_interaction_module_aiims
import data_interaction_module_slotting
import slot_distribution_calculator
import slot_schedule_payoff_calculator

app = Flask(__name__)


@app.route('/_by_date')
def by_date_look_up():
    try:
        date = request.args.get('date', 0, type=str)
        capacity = request.args.get('capacity', 0, type=int)
        department = request.args.get('department', 0, type=int)

        optimal_n, prob_range = data_interaction_module_aiims.retrieve_values_by_date(date, department, capacity)
        if optimal_n is None:
            return jsonify(success="false", result="Data Not Previously Calculated",
                           prob_range="Data Not Previously Calculated")
        return jsonify(success="true", result=optimal_n, prob_range=round(float(prob_range), 2))
    except Exception:
        return jsonify(success="false", result="Internal Error - Please check parameters",
                       prob_range="Internal Error - Please check parameters")


@app.route('/_add_numbers')
def add_numbers():
    try:
        prob = request.args.get('probability', 0, type=float)
        capacity = request.args.get('capacity', 0, type=int)
        optimal_n, prob_range = data_interaction_module_aiims.retrieve_values(prob, capacity)
        if optimal_n is None:
            return jsonify(success="false",
                           result="Data Not Previously Calculated. Calculated probability range - 0.1 to 0.99, both inclusive, with a step of 0.01",
                           prob_range="Data Not Previously Calculated")

        return jsonify(success="true", result=optimal_n, prob_range=round(float(prob_range), 2))
    except Exception:
        return jsonify(success="false", result="Internal Error. Please check parameters.",
                       prob_range="Internal Error. Please check parameters.")


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


@app.route('/_lookup_optimal_slotting_schedule')
def lookup_optimal_slotting_schedule():
    try:
        prob = request.args.get('probability', 0, type=float)
        total_capacity = request.args.get('total_capacity', 0, type=int)
        over_time_constant = request.args.get('over_time_constant', 1, type=float)
        wait_time_constant = request.args.get('wait_time_constant', 1, type=float)
        over_time_power = request.args.get('over_time_power', 2, type=float)

        schedule, pay_off = data_interaction_module_slotting.look_up_dictionary(prob, 3, total_capacity,
                                                                                over_time_constant, wait_time_constant,
                                                                                over_time_power)
        if schedule is None or len(schedule) == 0:
            return jsonify(success="false", result="Optimal Value not previously calculated",
                           prob_range="Optimal Value not previously calculated")
        return jsonify(success="true", result=', '.join(map(str, schedule)), prob_range=round(float(pay_off), 2))
    except Exception:
        return jsonify(success="false", result="Internal Error. Please check parameters.",
                       prob_range="Internal Error. Please check parameters.")


@app.route('/_calculate_payoff')
def calculate_payoff():
    try:
        number_of_slots = request.args.get('number_of_slots', 3, type=int)
        input_schedule = request.args.get('schedule', 2, type=str)
        schedule = []
        for term in input_schedule.split(","):
            if term.strip() == "":
                continue
            schedule.append(int(term.strip()))

        if len(schedule) != number_of_slots:
            return jsonify(success="false", result="No of Slots in Schedule not equal to total number of slots.")
        if number_of_slots < 1:
            return jsonify(success="false", result="No of Slots cannot be less than 0")

        prob = request.args.get('probability', 0, type=float)
        total_capacity = request.args.get('total_capacity', 0, type=int)
        over_time_constant = request.args.get('over_time_constant', 1, type=float)
        wait_time_constant = request.args.get('wait_time_constant', 1, type=float)
        over_time_power = request.args.get('over_time_power', 2, type=float)
        per_slot_processing_list = \
            slot_distribution_calculator.get_initial_configuration(number_of_slots, total_capacity)
        pay_off = slot_schedule_payoff_calculator.estimate_payoff(schedule, prob, per_slot_processing_list,
                                                                  over_time_constant, wait_time_constant,
                                                                  over_time_power)
        return jsonify(success="true", result=round(float(pay_off), 2))
    except Exception:
        return jsonify(success="false", result="Internal Error. Please check parameters.")


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
