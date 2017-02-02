import csv
import time

import scipy.stats as ss

from matplotlib import pyplot as plt

MAX_BOOKED = 108
PER_SLOT_PROCESSING = 20
NUMBER_OF_SLOTS = 3
show_up_prob = 0.5

MINIMUM_BOOKED = PER_SLOT_PROCESSING
MINIMUM_SHOW = 0
permutation_dictionary_list = []
stop_at_optimal_N_for_level_by_level_calculation = False
debug_logger = False


def initialize_permutation_dictionary():
    global permutation_dictionary_list
    if NUMBER_OF_SLOTS == 1:
        permutation_dictionary = []
    elif NUMBER_OF_SLOTS == 2:
        permutation_dictionary = [[1, -1], [-1, 1]]
    elif NUMBER_OF_SLOTS == 3:
        permutation_dictionary = [[1, -1, 0], [1, 0, -1], [0, 1, -1]]
    else:
        raise ValueError('Permutations Dictionary Not Defined For Chosen Number of Slots')


def get_initial_configuration(iterator):
    if NUMBER_OF_SLOTS == 1:
        return [MAX_BOOKED - iterator]
    elif NUMBER_OF_SLOTS == 2:
        return [(MAX_BOOKED - iterator) / 2, (MAX_BOOKED + 1 - iterator) / 2]
    elif NUMBER_OF_SLOTS == 3:
        return [(MAX_BOOKED - iterator) / 3, (MAX_BOOKED + 1 - iterator) / 3, (MAX_BOOKED + 2 - iterator) / 3]
    else:
        raise ValueError('Initial Configuration Not Defined For Chosen Number of Slots')


def calculate_payoff(gain, wait_loss, loss):
    if wait_loss == 0:
        return gain - loss
    else:
        overbooked_wait_cascading_cost = 0
        wait_copy = wait_loss - PER_SLOT_PROCESSING
        while wait_copy > 0:
            overbooked_wait_cascading_cost += wait_copy
            wait_copy -= PER_SLOT_PROCESSING

        overbooked_cost = wait_loss * wait_loss
        return gain + wait_loss - (overbooked_wait_cascading_cost + loss + overbooked_cost)


def initialize_and_get_recursive_benefit(slot_booked_list):
    slot_distribution_list = []
    for term in slot_booked_list:
        slot_distribution_list.append(ss.binom(term, show_up_prob))
    return recursive_benefit_calculation(1, 0, 0, 0, slot_distribution_list, slot_booked_list, 0)


def recursive_benefit_calculation(prob, gain, wait, loss, slot_distribution_list, slot_booked_list, recursive_level):
    # eliminate the recursive_level later. - buggy
    slot_booked = slot_booked_list[recursive_level]
    slot_distribution = slot_distribution_list[recursive_level]

    total_present_level_benefit = 0
    for slot_show_up in range(slot_booked + 1):
        slot_probability = slot_distribution.pmf(slot_show_up)
        attendance = slot_show_up + wait
        slot_gain = min(attendance, PER_SLOT_PROCESSING)
        slot_over_load = attendance - slot_gain

        if recursive_level == NUMBER_OF_SLOTS - 1:
            total_present_level_benefit += prob * slot_probability * calculate_payoff(slot_gain + gain, slot_over_load,
                                                                                      loss + slot_over_load)
        else:
            total_present_level_benefit += recursive_benefit_calculation(prob * slot_probability, slot_gain + gain,
                                                                         slot_over_load,
                                                                         loss + slot_over_load, slot_distribution_list,
                                                                         slot_booked_list,
                                                                         recursive_level + 1)
    return total_present_level_benefit


def get_perturbation_list(present_configuration, earlier_configuration):
    perturbation_list = []
    for variation in permutation_dictionary_list:
        generate_unique_permutation(earlier_configuration, perturbation_list, present_configuration, variation)
    if debug_logger == True:
        print "LOGGER perturbation_list : ", perturbation_list
    return perturbation_list


def generate_unique_permutation(earlier_configuration, perturbation_list, present_configuration, variation):
    permutation = present_configuration[:]
    for index, term in enumerate(permutation):
        term += variation[index]
        permutation[index] = term
        if term < 0:
            return
    if not (earlier_configuration is not None and len(
            earlier_configuration) > 0 and earlier_configuration == permutation) and not (
                        present_configuration is not None and len(
                    present_configuration) > 0 and present_configuration == permutation):
        perturbation_list.append(permutation)


def optimize_from_given_start_vector(present_configuration, present_benefit, previous_configuration):
    perturbation_list = get_perturbation_list(present_configuration, previous_configuration)
    best_variation = []
    value_for_best_perturbation = -1
    improvement_possible = False
    for variation in perturbation_list:
        perturbation_benefit = initialize_and_get_recursive_benefit(variation)
        if perturbation_benefit > present_benefit:
            best_variation = variation[:]
            value_for_best_perturbation = perturbation_benefit
            improvement_possible = True

        if debug_logger == True:
            print "LOGGER Calculated for perturbation : ", perturbation_benefit, variation

    if improvement_possible:
        if debug_logger == True:
            print "LOGGER best_variation, value_for_best_perturbation, present_configuration, time", best_variation, value_for_best_perturbation, present_configuration, time.time()
        return optimize_from_given_start_vector(best_variation, value_for_best_perturbation, present_configuration)
    else:
        return present_configuration, present_benefit


def execute(csv_file):
    print "\n\tParameters : MAX_BOOKED, PER_SLOT_PROCESSING, NUMBER_OF_SLOTS, p ", MAX_BOOKED, PER_SLOT_PROCESSING, \
        NUMBER_OF_SLOTS, show_up_prob, time.time()

    heading = ["N", "PAYOFF"]
    for slot_number in range(NUMBER_OF_SLOTS): heading.append("Optimal Slot" + str(slot_number + 1))
    csv_file.writerow(heading)

    n_point = []
    payoff_point = []

    highest_benefit = -1
    highest_benefit_config = []
    for total_number_of_bookings in range(0, MAX_BOOKED - NUMBER_OF_SLOTS * PER_SLOT_PROCESSING + 1):
        initial_configuration = get_initial_configuration(total_number_of_bookings)
        initial_benefit = initialize_and_get_recursive_benefit(initial_configuration)
        optimal_config, optimal_benefit = optimize_from_given_start_vector(initial_configuration, initial_benefit, [])
        print "\nFinal Output for N ", MAX_BOOKED - total_number_of_bookings, "optimal configuration and optimal payoff ", \
            optimal_config, optimal_benefit, time.time()

        row_value = [MAX_BOOKED - total_number_of_bookings, optimal_benefit]
        n_point.append(MAX_BOOKED - total_number_of_bookings)
        payoff_point.append(optimal_benefit)
        for slot in range(NUMBER_OF_SLOTS): row_value.append(optimal_config[slot])
        csv_file.writerow(row_value)

        if optimal_benefit > highest_benefit:
            highest_benefit = optimal_benefit
            highest_benefit_config = optimal_config
        elif stop_at_optimal_N_for_level_by_level_calculation:
            break

    csv_file.writerow([])
    row_value = [sum(highest_benefit_config), highest_benefit]
    for slot in range(NUMBER_OF_SLOTS): row_value.append(highest_benefit_config[slot])
    csv_file.writerow(row_value)

    plt.plot(n_point, payoff_point)
    plt.show()

    print "\n\tFinal Output for Optimal N configuration and payoff ", highest_benefit_config, highest_benefit
    print "\n\tParameters : MAX_BOOKED, PER_SLOT_PROCESSING, NUMBER_OF_SLOTS, p ", MAX_BOOKED, PER_SLOT_PROCESSING, NUMBER_OF_SLOTS, show_up_prob


def populate_permutations(incomplete_list, recursive_level):
    for term in range(-1, 2, 1):
        permutation = incomplete_list[:]
        permutation.append(term)
        if recursive_level == NUMBER_OF_SLOTS - 1:
            permutation_dictionary_list.append(permutation)
        else:
            populate_permutations(permutation, recursive_level + 1)


def filter_permutations():
    global permutation_dictionary_list
    filtered_permutation_list = []
    for permutation in permutation_dictionary_list:
        valid = True
        non_zero_elements = False
        for term in permutation:
            if term == 1:
                non_zero_elements = True
                break
            elif term == -1:
                non_zero_elements = True
                valid = False
                break
        if non_zero_elements and valid:
            filtered_permutation_list.append(permutation)
    permutation_dictionary = filtered_permutation_list


# populate_permutations([], 0)
# filter_permutations()
initialize_permutation_dictionary()

filename = "MAX_BOOKED_" + str(MAX_BOOKED) + "_" + "PER_SLOT_" + str(
    PER_SLOT_PROCESSING) + "_" + "NUMBER_OF_SLOTS_" + str(NUMBER_OF_SLOTS) + "_" + "prob_" + str(show_up_prob) + ".csv"
output_file = open(filename, 'w')
csv_file = csv.writer(output_file)
execute(csv_file)
output_file.close()

# def populate_permutations(total, incomplete_list, recursive_level):
#     max_range = MAX_BOOKED - total - (NUMBER_OF_SLOTS * MINIMUM_BOOKED) + 1
#     for term in range(-1, 1, 1):
#         permutation = incomplete_list[:]
#         permutation.append(term)
#         if recursive_level == NUMBER_OF_SLOTS - 1:
#             permutation_dictionary[permutation] = 1
#         else:
#             populate_permutations(total + term, incomplete_list, recursive_level + 1)
#
#
# def brute_producer():
#     populate_permutations(0, [], 0)
#     variation = []
#     value_with_best_permutation = -1
#     for permutation in permutation_dictionary.keys():
#         permutation_benefit = get_recursive_benefit(permutation)
#         if permutation_benefit > value_with_best_permutation:
#             value_with_best_permutation = permutation_benefit
#             variation = permutation_benefit
#
#     return variation, value_with_best_permutation
