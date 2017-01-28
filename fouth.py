import itertools
import time

import scipy.stats as ss

PER_SLOT_PROCESSING = 200
MAX_BOOKED = 400
MINIMUM_BOOKED = 100
MINIMUM_SHOW = 0


def calculate_cost(probability, show_up):
    if (show_up < PER_SLOT_PROCESSING):
        return show_up * probability
    cost = (show_up - (show_up - PER_SLOT_PROCESSING) * (show_up - PER_SLOT_PROCESSING))
    return cost * probability


list(itertools.permutations([1, 2, 3]))


def get_optimal_cost(event_prob):
    expected_cost = 0
    optimal_N = 0

    for booked in range(MINIMUM_BOOKED, MAX_BOOKED + 1):
        distribution = ss.binom(booked, event_prob)
        booked_cost = 0
        for show_up in range(MINIMUM_SHOW, booked + 1):
            prob = distribution.pmf(show_up)
            cost = calculate_cost(prob, show_up)
            # print booked, "\t", show_up, "\t", prob, "\t", cost
            booked_cost += cost

        if booked_cost > expected_cost:
            expected_cost = booked_cost
            optimal_N = booked
    return expected_cost, optimal_N


p_unit = 0.1

event_calculation_start_time = time.time()
expected_cost, optimal_N = get_optimal_cost(p_unit)
