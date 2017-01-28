import scipy.stats as ss

PER_SLOT_PROCESSING = 10
MAX_BOOKED = 25
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


if __name__ == "__main__":
    print "PER_SLOT_PROCESSING, MAX_BOOKED, p, MINIMUM_BOOKED", PER_SLOT_PROCESSING, MAX_BOOKED, show_up_prob, MINIMUM_BOOKED
    print calculate_optimal_n_and_cost()
