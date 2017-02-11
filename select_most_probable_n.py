import math
import sys

from scipy import stats as ss


def calculate_cost(show_up, capacity, over_time_power=2):
    return math.pow(show_up - capacity, over_time_power)


def calculate_below_min_value_cost(show_up, min_value, over_time_power=2):
    return math.pow(min_value - show_up, over_time_power)


def calculate_cost_of_under_utilization_and_over(capacity, max_value, min_value, n_value, prob):
    distribution = ss.binom(n_value, prob)
    cost = 0
    for x in range(0, min_value + 1):
        cost -= calculate_below_min_value_cost(x, min_value) * distribution.pmf(x)
    for x in range(max_value, n_value + 1):
        cost -= calculate_cost(x, capacity) * distribution.pmf(x)
    return cost


def compute_best_n_prob_maximized(loss_function_Type, max_value, min_value, n_associated_with_best_likelihood,
                                  n_start_point, prob):
    best_likelihood = -sys.maxint - 1
    while True:
        distribution = ss.binom(n_start_point, prob)
        likely_hood = 0
        if loss_function_Type == "PROB_MAXIMIZED":
            for patient_number in range(min_value + 1, max_value + 1):
                likely_hood += distribution.pmf(patient_number)

        if likely_hood > best_likelihood:
            best_likelihood = likely_hood
            n_associated_with_best_likelihood = n_start_point
        else:
            break

        n_start_point += 1
    if n_associated_with_best_likelihood == -1:
        raise StandardError("Best n_associated_with_best_likelihood not found")
    return int(n_associated_with_best_likelihood), best_likelihood


def compute_best_n(capacity, max_value, min_value, prob, n_start_point, loss_function_Type="PROB_MAXIMIZED"):
    if loss_function_Type not in ["PROB_MAXIMIZED", "GAIN_MINUS_LOSS", "LOSS_MAXIMIZED"]:
        raise Exception("loss_function_Type should be in [PROB_MAXIMIZED, GAIN_MINUS_LOSS, LOSS_MAXIMIZED]")

    n_associated_with_best_likelihood = -1
    up_to = int(float(capacity) / prob)
    up_to = max_value if max_value > up_to else up_to

    if loss_function_Type == "PROB_MAXIMIZED":
        return compute_best_n_prob_maximized(loss_function_Type, max_value, min_value,
                                             n_associated_with_best_likelihood, n_start_point, prob)

    elif loss_function_Type == "LOSS_MAXIMIZED":
        best_cost = -sys.maxint - 1
        cost_list = []
        for n_value in range(max_value, up_to + 1):

            cost = calculate_cost_of_under_utilization_and_over(capacity, max_value, min_value, n_value, prob)

            if cost > best_cost:
                best_cost = cost
                n_associated_with_best_likelihood = n_value
            else:
                break

            cost_list.append(cost)

        if n_associated_with_best_likelihood == -1:
            print "Best n_associated_with_best_likelihood not found"

        return int(n_associated_with_best_likelihood), best_cost

    else:
        best_payoff = -sys.maxint - 1
        payoff_list = []
        for n_value in range(max_value, up_to + 1):

            payoff = n_value * prob + calculate_cost_of_under_utilization_and_over(capacity, max_value, min_value,
                                                                                   n_value, prob)

            if payoff > best_payoff:
                best_payoff = payoff
                n_associated_with_best_likelihood = n_value
            else:
                break

            payoff_list.append(payoff)

        if n_associated_with_best_likelihood == -1:
            print "Best n_associated_with_best_likelihood not found"

        return int(n_associated_with_best_likelihood), best_payoff
