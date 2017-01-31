import csv
import itertools as itools
import sys
import time

from payoff_calculator import estimate_payoff

MAX_BOOKED = 20
PER_SLOT_PROCESSING = 1
NUMBER_OF_SLOTS = 2
show_up_prob = 0.5

N_CALCULATION_RANGE = MAX_BOOKED
MINIMUM_BOOKED = PER_SLOT_PROCESSING
stop_at_optimal_N_for_level_by_level_calculation = False
debug_logger = False

MINIMUM_SHOW = 0
permutation_dictionary = []


def initialize_permutation_dictionary():
    global permutation_dictionary
    permutation_dictionary = []
    if NUMBER_OF_SLOTS > 1:
        position_permutations = set(list(itools.permutations(range(NUMBER_OF_SLOTS), 2)))
        for position_configuration in position_permutations:
            configuration = [0 for x in range(NUMBER_OF_SLOTS)]
            configuration[position_configuration[0]] = -1
            configuration[position_configuration[1]] = 1
            permutation_dictionary.append(configuration[:])


def print_parameters(TAG, over_time_constant, over_time_power, wait_time_constant, previous_time):
    print "\n********Parameters : MAX_BOOKED, PER_SLOT_PROCESSING, NUMBER_OF_SLOTS, p, Over_Time_Power, over_time_constant, wait_time_constant, TAG, processing_time*******\n", \
        MAX_BOOKED, PER_SLOT_PROCESSING, NUMBER_OF_SLOTS, show_up_prob, over_time_power, over_time_constant, wait_time_constant, TAG, time.time() - previous_time, "\n"
    return time.time()

def get_initial_configuration(iterator):
    schedule = []
    for i in range(NUMBER_OF_SLOTS, 0, -1):
        schedule.append((MAX_BOOKED + (i - 1) - iterator) / NUMBER_OF_SLOTS)
    return schedule


def get_perturbation_list(present_configuration, previous_neighbourhood):
    perturbation_list = []
    for variation in permutation_dictionary:
        permutation = present_configuration[:]
        for index, term in enumerate(permutation):
            term += variation[index]
            permutation[index] = term
            if term < 0:
                return
        permutation_tuple = tuple(permutation)
        if not previous_neighbourhood.has_key(permutation_tuple):
            perturbation_list.append(permutation)
            previous_neighbourhood[permutation_tuple] = 1

    if debug_logger:
        print "LOGGER perturbation_list : ", perturbation_list
    return perturbation_list


def optimize_from_given_start_config(present_configuration, present_payoff, over_time_power,
                                     over_time_constant, wait_time_constant, previous_neighbourhood):
    perturbation_list = get_perturbation_list(present_configuration, previous_neighbourhood)
    best_variation = []
    value_for_best_perturbation = -sys.maxint - 1
    # noinspection PyTypeChecker
    for variation in perturbation_list:
        perturbation_payoff = estimate_payoff(variation, show_up_prob, PER_SLOT_PROCESSING, wait_time_constant,
                                              over_time_constant, over_time_power)
        if perturbation_payoff > present_payoff:
            best_variation = variation[:]
            value_for_best_perturbation = perturbation_payoff

    if value_for_best_perturbation > -sys.maxint - 1:
        if debug_logger == True:
            print "LOGGER best_variation, value_for_best_perturbation, present_configuration, time", best_variation, value_for_best_perturbation, present_configuration, time.time()
        return optimize_from_given_start_config(best_variation, value_for_best_perturbation, over_time_power,
                                                over_time_constant, wait_time_constant,
                                                previous_neighbourhood)
    else:
        return present_configuration, present_payoff


def execute(over_time_power, wait_time_constant, over_time_constant):
    # Initialize list of perturbations
    initialize_permutation_dictionary()

    heading = ["N", "PAYOFF"]
    for slot_number in range(NUMBER_OF_SLOTS): heading.append("Optimal Slot" + str(slot_number + 1))
    output_rows = [heading]

    # Initialize Execution Parameters
    n_value_list = []
    payoff_value_list = []

    highest_payoff = -sys.maxint - 1
    highest_payoff_config = []
    for total_number_of_bookings in range(0, min(MAX_BOOKED - NUMBER_OF_SLOTS * PER_SLOT_PROCESSING + 1,
                                                 N_CALCULATION_RANGE)):
        initial_configuration = get_initial_configuration(total_number_of_bookings)
        initial_payoff = estimate_payoff(initial_configuration, show_up_prob, PER_SLOT_PROCESSING, wait_time_constant,
                                         over_time_constant, over_time_power)
        optimal_config, optimal_payoff = optimize_from_given_start_config(initial_configuration, initial_payoff,
                                                                          over_time_power, over_time_constant,
                                                                          wait_time_constant, {tuple(initial_configuration) : 1})

        n_value_list.append(MAX_BOOKED - total_number_of_bookings)
        payoff_value_list.append(optimal_payoff)
        row_value = [MAX_BOOKED - total_number_of_bookings, optimal_payoff]
        for slot in range(NUMBER_OF_SLOTS): row_value.append(optimal_config[slot])
        output_rows.append(row_value)

        print "\nFinal, Most Optimal Output for N ", MAX_BOOKED - total_number_of_bookings, "configuration and payoff ", \
            optimal_config, optimal_payoff, time.time()
        if optimal_payoff > highest_payoff:
            highest_payoff = optimal_payoff
            highest_payoff_config = optimal_config
        elif stop_at_optimal_N_for_level_by_level_calculation:
            break

    return n_value_list, payoff_value_list, output_rows, highest_payoff_config, highest_payoff


# populate permutation terms in number of slots with values between -1, 0 ,1
def populate_permutations(incomplete_list, recursive_level):
    for term in range(-1, 2, 1):
        permutation = incomplete_list[:]
        permutation.append(term)
        if recursive_level == NUMBER_OF_SLOTS - 1:
            permutation_dictionary.append(permutation)
        else:
            populate_permutations(permutation, recursive_level + 1)


# Checks if the -1 term comes before the 1 term and filters out those permutations
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


# external entry point for optimal Schedule Calculation
def set_params_and_get_optimal_schedule(MAX_BOOKED_PARAM, show_up_prob_PARAM, PER_SLOT_PROCESSING_PARAM,
                                        NUMBER_OF_SLOTS_PARAM, over_time_power, wait_time_constant, over_time_constant,
                                        TAG="TAG", debug_logger_param=False,
                                        stop_at_optimal_N_for_level_by_level_calculation_param=False):
    global MAX_BOOKED, PER_SLOT_PROCESSING, NUMBER_OF_SLOTS, show_up_prob, N_CALCULATION_RANGE, stop_at_optimal_N_for_level_by_level_calculation, debug_logger, MINIMUM_BOOKED
    MAX_BOOKED = MAX_BOOKED_PARAM
    N_CALCULATION_RANGE = MAX_BOOKED_PARAM
    PER_SLOT_PROCESSING = PER_SLOT_PROCESSING_PARAM
    MINIMUM_BOOKED = PER_SLOT_PROCESSING_PARAM
    NUMBER_OF_SLOTS = NUMBER_OF_SLOTS_PARAM
    show_up_prob = show_up_prob_PARAM
    stop_at_optimal_N_for_level_by_level_calculation = stop_at_optimal_N_for_level_by_level_calculation_param
    debug_logger = debug_logger_param

    return get_optimal_schedule(over_time_constant, wait_time_constant, over_time_power, TAG)


# internal entry point for optimal Schedule Calculation
def get_optimal_schedule(over_time_constant=1.0, wait_time_constant=1.0, over_time_power=2, TAG="TAG"):
    start_time = print_parameters(TAG, over_time_constant, over_time_power, wait_time_constant, time.time())

    n_value_list, payoff_value_list, output_rows, highest_payoff_config, highest_payoff = execute(over_time_power,
                                                                                                  wait_time_constant,
                                                                                                  over_time_constant)
    print_parameters(TAG, over_time_constant, over_time_power, wait_time_constant, start_time)
    print "\tFinal Output for Optimal N configuration and payoff ", highest_payoff_config, highest_payoff, "\n\n"

    filename = TAG + "MAX_BOOKED_" + str(MAX_BOOKED) + "_" + "PER_SLOT_" + str(
        PER_SLOT_PROCESSING) + "_" + "NUMBER_OF_SLOTS_" + str(NUMBER_OF_SLOTS) + "_" + "prob_" + str(show_up_prob)
    output_file = open("Output-csv/" + filename + ".csv", 'w')
    csv_file = csv.writer(output_file)
    csv_file.writerows(output_rows)
    output_file.close()

    # plt.plot(n_value_list, payoff_value_list)
    # plt.savefig("Output-png/" + filename + ".png", bbox_inches='tight')

    return highest_payoff_config, highest_payoff


if __name__ == "__main__":
    get_optimal_schedule(over_time_constant=1, wait_time_constant=1)
