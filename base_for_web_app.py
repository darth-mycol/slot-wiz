from flask import Flask, jsonify, render_template, request

import data_read_estimate_dictionary

app = Flask(__name__)


@app.route('/_add_numbers')
def add_numbers():
    """Add two numbers server side, ridiculous but well..."""
    prob = request.args.get('a', 0, type=float)
    capacity = request.args.get('b', 0, type=int)

    optimal_n, prob_range = data_read_estimate_dictionary.retrieve_values(prob, capacity)
    return jsonify(result=optimal_n, prob_range=prob_range)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
