import csv

import scipy.stats as ss

MAX_BOOKED = 50
MINIMUM_BOOKED = 0

MINIMUM_SHOW = 0

AVAILABLE_SLOT = 1
MAX_PER_SLOT = 1

INCLUDE_LAST_VALUE = 1

show_up_prob = 0.5


def validate_parameters(loss, gain, wait, prob, configuration):
    pass


def calculate_filled_till_now(configuration):
    if configuration is None or len(configuration) < 1:
        return 0

    filled = 0
    for term in configuration:
        filled += term
    return filled


def update_gain(wait, show_up):
    present = wait + show_up
    return MAX_PER_SLOT if present >= MAX_PER_SLOT else present


def validate_generation_parameters(existing_seq, summation):
    pass


def generate_sequence(existing_seq, summation):
    validate_generation_parameters(existing_seq, summation)
    cloned_seq = existing_seq[:]
    cloned_seq.append(-1)
    for slot_value in range(MINIMUM_BOOKED, MAX_BOOKED - summation + INCLUDE_LAST_VALUE):
        cloned_seq[-1] = slot_value


def propagate(loss, gain, presently_waiting, prob, configuration):
    validate_parameters(loss, gain, presently_waiting, prob, configuration)
    # BASE CASE
    if len(configuration) == AVAILABLE_SLOT - 1:
        empty = MAX_BOOKED - calculate_filled_till_now(configuration)
        for slot_value in range(MINIMUM_BOOKED, empty):
            slot_distribution = ss.binom(slot_value, show_up_prob)
            for show_up in range(0, slot_value + INCLUDE_LAST_VALUE):
                slot_prob = slot_distribution.pmf(show_up)

                prob = prob * slot_prob

                show_up += presently_waiting
                gain = show_up

                leftover = show_up - MAX_PER_SLOT if show_up > MAX_PER_SLOT else 0
                loss += leftover*(leftover + 1)/2

                cost_for_expectation = (gain - loss) * prob


    else:
        pass


output_file = open('output.csv', 'w')
csv_file = csv.writer(output_file)

print "x,\ty,\tTotal"

max_total = 0
max_x = 0
max_y = 0

for x in range(MINIMUM_BOOKED, MAX_BOOKED + 1):
    x_distribution = ss.binom(x, show_up_prob)
    for y in range(MINIMUM_BOOKED, MAX_BOOKED - x + 1):
        y_distribution = ss.binom(y, show_up_prob)
        xy_total = 0

        for x_value in range(MINIMUM_BOOKED, x + 1):
            x_prob = x_distribution.pmf(x_value)

            x_wait = x_value - 1 if x_value - 1 > 0 else 0
            # x_gain = 1 if x_value != 0 else 0

            for y_value in range(MINIMUM_BOOKED, y + 1):
                y_prob = y_distribution.pmf(y_value)
                # y_gain = 1 if y_value + x_wait !=0 else 0

                y_wait = y_value + x_wait - 1 if y_value + x_wait - 1 > 0 else 0

                y_over = y_wait * (y_wait + 1) / 2

                xy_total += ((x_value + y_value) - (x_wait + y_over)) * x_prob * y_prob

        csv_file.writerow([x, y, xy_total])
        # print x,y,xy_total
        if xy_total > max_total:
            max_y = y
            max_x = x
            max_total = xy_total

print max_x, max_y, max_total
output_file.close()
