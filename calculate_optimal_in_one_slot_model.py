import csv

import scipy.stats as ss

import slot_distribution_calculator as distribution_calc

PER_SLOT_PROCESSING = 201
MAX_BOOKED = 500
show_up_prob = 0.4

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


def get_optimal_for_probability_list():
    global show_up_prob
    probability_list = []
    for prob in range(40, 71, 5):
        probability_list.append(float(prob) / 100)
    for prob in range(80, 96, 5):
        probability_list.append(float(prob) / 100)
    probability_list.append(0.99)

    NUMBER_OF_SLOTS = 3

    heading = ["Prob", "N", "PAYOFF"]
    for slot_number in range(NUMBER_OF_SLOTS): heading.append("Optimal Slot" + str(slot_number + 1))
    heading.append("Distributed Payoff")
    output_rows = [heading]

    for probability in probability_list:
        show_up_prob = probability
        print "PER_SLOT_PROCESSING, MAX_BOOKED, p, MINIMUM_BOOKED", PER_SLOT_PROCESSING, MAX_BOOKED, show_up_prob, MINIMUM_BOOKED
        expected_cost, optimal_N = calculate_optimal_n_and_cost()

        distributed_configuration, payoff = distribution_calc.set_parameters_and_estimate_payoff(
            show_up_prob_PARAM=probability, PER_SLOT_PROCESSING_PARAM=PER_SLOT_PROCESSING/NUMBER_OF_SLOTS,
            NUMBER_OF_SLOTS_PARAM=NUMBER_OF_SLOTS, total_booking=optimal_N, max_booked_param=MAX_BOOKED)

        row_value = [show_up_prob, optimal_N, expected_cost]
        for slot in range(NUMBER_OF_SLOTS): row_value.append(distributed_configuration[slot])
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
