import csv
import math
import time

import scipy.stats as ss
from matplotlib import pyplot as plt

MAX_BOOKED = 375
PER_SLOT_PROCESSING = 67
NUMBER_OF_SLOTS = 3
p = 0.6

MINIMUM_BOOKED = PER_SLOT_PROCESSING
MINIMUM_SHOW = 0
permutation_dictionary = []
stop_at_optimal_N_for_level_by_level_calculation = False
debug_logger = False


def initialize_permutation_dictionary():
    global permutation_dictionary
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


def get_previous_waiting(earlier_slot_waiting, slot_number, probability_dict):
    if not probability_dict.has_key((slot_number, earlier_slot_waiting)):
        # todo Will this Ever Happen?
        raise Exception(
            "Earlier Probability not found. Key: (earlier_slot_waiting, slot_number), and past_probabilities_dict",
            earlier_slot_waiting, slot_number, probability_dict)

    return probability_dict.get((slot_number, earlier_slot_waiting))


# all values from 0 to per_slot for previous slot
def get_theta_summation(probability_dict, slot_number):
    if slot_number == -1:
        return 1

    theta_summation = get_previous_waiting(0, slot_number - 1, probability_dict)
    return theta_summation


def get_present_waiting(number_show_up, appointments_booked_in_slot, slot_show_up_distribution):
    if appointments_booked_in_slot < number_show_up:
        raise Exception(
            "Number Show Up somehow greater than total booking",
            number_show_up, appointments_booked_in_slot, slot_show_up_distribution)
    else:
        return slot_show_up_distribution.pmf(number_show_up)


def estimate_loss(schedule, probability_dict):
    if len(schedule) != NUMBER_OF_SLOTS or NUMBER_OF_SLOTS < 1: raise Exception("len(schedule) != NUMBER_OF_SLOTS")
    max_possible_carry_over = 0
    total_wait_loss = 0
    for slot_number in range(NUMBER_OF_SLOTS):
        booked_appointments = schedule[slot_number]
        if max_possible_carry_over + booked_appointments <= PER_SLOT_PROCESSING:
            probability_dict[(slot_number, 0)] = 1
            max_possible_carry_over = 0
            continue

        prob_of_at_least_one_over_load = 0
        patient_show_up_distribution = ss.binom(booked_appointments, p)
        for over_load in range(PER_SLOT_PROCESSING + 1, max_possible_carry_over + booked_appointments + 1):
            lower_bound = max(over_load - max_possible_carry_over, 0)
            upper_bound = min(booked_appointments, over_load)
            if lower_bound > upper_bound:
                continue

            prob = 0
            for show_up in range(lower_bound, upper_bound + 1):
                if show_up == over_load:
                    alpha = get_present_waiting(show_up, booked_appointments, patient_show_up_distribution)
                    theta_summation = get_theta_summation(probability_dict, slot_number)
                    prob += theta_summation * alpha
                if show_up < over_load:
                    earlier_slot_waiting = over_load - show_up
                    theta = get_previous_waiting(earlier_slot_waiting, slot_number - 1, probability_dict)
                    alpha = get_present_waiting(show_up, booked_appointments, patient_show_up_distribution)
                    prob += theta * alpha

            total_waiting_at_slot_end = over_load - PER_SLOT_PROCESSING
            probability_dict[(slot_number, total_waiting_at_slot_end)] = prob
            total_wait_loss += total_waiting_at_slot_end * prob
            prob_of_at_least_one_over_load += prob

        max_possible_carry_over = max(max_possible_carry_over + booked_appointments - PER_SLOT_PROCESSING, 0)

        probability_dict[(slot_number, 0)] = 1 - prob_of_at_least_one_over_load

    over_time_loss = 0
    for over_book in range(1, max_possible_carry_over + 1):
        theta = get_previous_waiting(over_book, NUMBER_OF_SLOTS - 1, probability_dict)
        over_time_loss += theta * math.pow(over_book, 2)

        overbooked_wait_cascading_cost = 0
        over_book_wait_loss = over_book - PER_SLOT_PROCESSING
        while over_book_wait_loss > 0:
            overbooked_wait_cascading_cost += over_book_wait_loss
            over_book_wait_loss -= PER_SLOT_PROCESSING

        total_wait_loss += overbooked_wait_cascading_cost * theta

    return total_wait_loss, over_time_loss


def get_perturbation_list(present_configuration, earlier_configuration):
    perturbation_list = []
    for variation in permutation_dictionary:
        generate_unique_permutation(earlier_configuration, perturbation_list, present_configuration, variation)
    if debug_logger:
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


def estimate_payoff(variation):
    gain = sum(variation) * p
    wait_loss, over_time_loss = estimate_loss(variation, {(-1, 0): 1})
    return gain - wait_loss - over_time_loss


def optimize_from_given_start_vector(present_configuration, present_benefit, previous_configuration):
    perturbation_list = get_perturbation_list(present_configuration, previous_configuration)
    best_variation = []
    value_for_best_perturbation = -1
    improvement_possible = False
    for variation in perturbation_list:
        perturbation_benefit = estimate_payoff(variation)
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
        NUMBER_OF_SLOTS, p, time.time()

    heading = ["N", "PAYOFF"]
    for slot_number in range(NUMBER_OF_SLOTS): heading.append("Optimal Slot" + str(slot_number + 1))
    csv_file.writerow(heading)

    n_point = []
    payoff_point = []

    highest_benefit = -1
    highest_benefit_config = []
    for total_number_of_bookings in range(0, MAX_BOOKED - NUMBER_OF_SLOTS * PER_SLOT_PROCESSING + 1):
        initial_configuration = get_initial_configuration(total_number_of_bookings)
        initial_benefit = estimate_payoff(initial_configuration)
        optimal_config, optimal_benefit = optimize_from_given_start_vector(initial_configuration, initial_benefit, [])
        print "\nFinal, Most Optimal Output for N ", MAX_BOOKED - total_number_of_bookings, "configuration and payoff ", \
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

    print "\n\tFinal Output for Optimal N configuration and payoff ", highest_benefit_config, highest_benefit

    plt.plot(n_point, payoff_point)
    plt.show()
    print "\n\tParameters : MAX_BOOKED, PER_SLOT_PROCESSING, NUMBER_OF_SLOTS, p ", MAX_BOOKED, PER_SLOT_PROCESSING, NUMBER_OF_SLOTS, p


def populate_permutations(incomplete_list, recursive_level):
    for term in range(-1, 2, 1):
        permutation = incomplete_list[:]
        permutation.append(term)
        if recursive_level == NUMBER_OF_SLOTS - 1:
            permutation_dictionary.append(permutation)
        else:
            populate_permutations(permutation, recursive_level + 1)


def filter_permutations():
    global permutation_dictionary
    filtered_permutation_list = []
    for permutation in permutation_dictionary:
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


initialize_permutation_dictionary()

filename = "MAX_BOOKED_" + str(MAX_BOOKED) + "_" + "PER_SLOT_" + str(
    PER_SLOT_PROCESSING) + "_" + "NUMBER_OF_SLOTS_" + str(NUMBER_OF_SLOTS) + "_" + "prob_" + str(p) + ".csv"
output_file = open(filename, 'w')
csv_file = csv.writer(output_file)
execute(csv_file)
output_file.close()
