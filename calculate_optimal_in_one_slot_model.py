import csv

import scipy.stats as ss

import payoff_calculator

PER_SLOT_PROCESSING = 201
MAX_BOOKED = 377
show_up_prob = 0.5

MINIMUM_BOOKED = PER_SLOT_PROCESSING
MINIMUM_SHOW = 0


def calculate_cost(probability, show_up):
    if show_up < PER_SLOT_PROCESSING:
        return show_up * probability
    cost = (show_up - (show_up - PER_SLOT_PROCESSING) * (show_up - PER_SLOT_PROCESSING))
    return cost * probability


def calculate_optimal_n_and_cost():
    expected_cost = 0
    optimal_N = 0
    for booked in range(MINIMUM_BOOKED, MAX_BOOKED + 1):
        distribution = ss.binom(booked, show_up_prob)
        booked_cost = 0
        for show_up in range(MINIMUM_SHOW, booked + 1):
            prob = distribution.pmf(show_up)
            cost = calculate_cost(prob, show_up)
            booked_cost += cost

        if booked_cost > expected_cost:
            expected_cost = booked_cost
            optimal_N = booked

    return expected_cost, optimal_N


# entry point
def set_parameters_and_get_optimal_n(PER_SLOT_PROCESSING_PARAM, MAX_BOOKED_PARAM, p_PARAM):
    global PER_SLOT_PROCESSING, MAX_BOOKED, show_up_prob, MINIMUM_BOOKED
    PER_SLOT_PROCESSING = PER_SLOT_PROCESSING_PARAM
    MINIMUM_BOOKED = PER_SLOT_PROCESSING_PARAM
    MAX_BOOKED = MAX_BOOKED_PARAM
    show_up_prob = p_PARAM

    return calculate_optimal_n_and_cost()


# todo This should become an external point of this code.
def get_optimal_for_probability_list():
    global show_up_prob
    # Initialize Prob List
    probability_list = []
    for prob in range(40, 71, 5):
        probability_list.append(float(prob) / 100)
    for prob in range(80, 96, 5):
        probability_list.append(float(prob) / 100)
    probability_list.append(0.99)

    # Initialize Execution Params
    per_slot_processing_list = [67, 67, 66]
    number_of_slots = 3
    over_time_constant = 1
    wait_time_constant = 1

    heading = ["Prob", "N", "PAYOFF"]
    for slot_number in range(number_of_slots): heading.append("Optimal Slot" + str(slot_number + 1))
    heading.append("Distributed Payoff")
    output_rows = [heading]

    for probability in probability_list:
        show_up_prob = probability
        print "PER_SLOT_PROCESSING, MAX_BOOKED, p, MINIMUM_BOOKED", PER_SLOT_PROCESSING, MAX_BOOKED, show_up_prob, MINIMUM_BOOKED
        expected_cost, optimal_N = calculate_optimal_n_and_cost()

        distributed_configuration, payoff = payoff_calculator.set_parameters_and_estimate_payoff(
            show_up_prob_PARAM=probability, per_slot_processing_list=per_slot_processing_list,
            NUMBER_OF_SLOTS_PARAM=number_of_slots, total_booking=optimal_N, wait_time_constant=wait_time_constant,
            over_time_constant=over_time_constant)

        row_value = [show_up_prob, optimal_N, expected_cost]
        for slot in range(number_of_slots): row_value.append(distributed_configuration[slot])
        row_value.append(payoff)
        output_rows.append(row_value)

    TAG = "ONE_SLOT_BOOKING_"
    filename = TAG + "PER_SLOT_" + str(PER_SLOT_PROCESSING)
    output_file = open("Aggregated-csv/" + filename + ".csv", 'w')
    csv_file = csv.writer(output_file)
    csv_file.writerows(output_rows)
    output_file.close()


def get_optimal_for_single_given_prob():
    print "PER_SLOT_PROCESSING, MAX_BOOKED, p, MINIMUM_BOOKED", PER_SLOT_PROCESSING, MAX_BOOKED, show_up_prob, MINIMUM_BOOKED
    print calculate_optimal_n_and_cost()


if __name__ == "__main__":
    get_optimal_for_probability_list()
    # get_optimal_for_single_given_prob()
