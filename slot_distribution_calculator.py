import csv
import itertools as itools
import sys
import time

from payoff_calculator import estimate_payoff

MAX_BOOKED = 375
PER_SLOT_PROCESSING = 67
NUMBER_OF_SLOTS = 3
show_up_prob = 0.5

N_CALCULATION_RANGE = MAX_BOOKED
MINIMUM_BOOKED = PER_SLOT_PROCESSING
stop_at_optimal_N_for_level_by_level_calculation = False
debug_logger = True

permutation_dictionary_list = []


def add_sample_to_permutation_dictionary(index, permutation_dictionary_list, total_possibilities, sample_size,
                                         single_sample_dictionary):
    if len(single_sample_dictionary) > sample_size or index == total_possibilities - 1:
        permutation_dictionary_list.append(single_sample_dictionary[:])
        single_sample_dictionary = []
    return single_sample_dictionary


def initialize_permutation_dictionary(sample_size, permutation_across_n=False):
    global permutation_dictionary_list
    permutation_dictionary_list = []
    if NUMBER_OF_SLOTS > 1:
        single_sample_dictionary = []
        if permutation_across_n:
            for index in range(NUMBER_OF_SLOTS):
                configuration = [0 for x in range(NUMBER_OF_SLOTS)]
                configuration[index] = -1
                single_sample_dictionary.append(configuration[:])
                configuration[index] = 1
                single_sample_dictionary.append(configuration[:])

                single_sample_dictionary = add_sample_to_permutation_dictionary(index, permutation_dictionary_list,
                                                                                NUMBER_OF_SLOTS, sample_size,
                                                                                single_sample_dictionary)
        else:
            position_permutations = set(list(itools.permutations(range(NUMBER_OF_SLOTS), 2)))
            for index, position_configuration in enumerate(position_permutations):
                configuration = [0 for x in range(NUMBER_OF_SLOTS)]
                configuration[position_configuration[0]] = -1
                configuration[position_configuration[1]] = 1
                single_sample_dictionary.append(configuration[:])
                single_sample_dictionary = add_sample_to_permutation_dictionary(index, permutation_dictionary_list,
                                                                                len(position_permutations), sample_size,
                                                                                single_sample_dictionary)


def print_parameters(TAG, over_time_constant, over_time_power, wait_time_constant, previous_time):
    #print "\n********Parameters : MAX_BOOKED, PER_SLOT_PROCESSING, NUMBER_OF_SLOTS, p, Over_Time_Power, over_time_constant, wait_time_constant, TAG, processing_time*******\n", \
    #    MAX_BOOKED, PER_SLOT_PROCESSING, NUMBER_OF_SLOTS, show_up_prob, over_time_power, over_time_constant, wait_time_constant, TAG, time.time() - previous_time, "\n"
    return time.time()


def get_initial_configuration(iterator):
    schedule = []
    for i in range(NUMBER_OF_SLOTS, 0, -1):
        schedule.append((MAX_BOOKED + (i - 1) - iterator) / NUMBER_OF_SLOTS)
    return schedule


def get_unique_permutation(present_configuration, variation):
    permutation = present_configuration[:]
    for index, term in enumerate(permutation):
        term += variation[index]
        permutation[index] = term
        if term < 0:
            return []
    return permutation


def get_perturbation_list(present_configuration, previous_neighbourhood, single_sample_dictionary):
    perturbation_list = []
    for variation in single_sample_dictionary:
        permutation = get_unique_permutation(present_configuration, variation)
        if len(permutation) == 0:
            continue

        permutation_tuple = tuple(permutation)
        if not previous_neighbourhood.has_key(permutation_tuple):
            perturbation_list.append(permutation)
            previous_neighbourhood[permutation_tuple] = 1

    if debug_logger:
        print "LOGGER perturbation_list : ", perturbation_list
    return perturbation_list


def optimize_from_given_start_config(present_configuration, present_payoff, over_time_power,
                                     over_time_constant, wait_time_constant, previous_neighbourhood):
    best_variation = []
    value_for_best_perturbation = -sys.maxint - 1
    for single_sample_dictionary in permutation_dictionary_list:
        perturbation_list = get_perturbation_list(present_configuration, previous_neighbourhood,
                                                  single_sample_dictionary)
        for variation in perturbation_list:
            perturbation_payoff = estimate_payoff(variation, show_up_prob, PER_SLOT_PROCESSING, wait_time_constant,
                                                  over_time_constant, over_time_power)
            if perturbation_payoff > value_for_best_perturbation:
                best_variation = variation[:]
                value_for_best_perturbation = perturbation_payoff

        if value_for_best_perturbation > present_payoff:
            if debug_logger:
                print "LOGGER best_variation, value_for_best_perturbation, present_configuration, time", best_variation, value_for_best_perturbation, present_configuration, time.time()
            return optimize_from_given_start_config(best_variation, value_for_best_perturbation, over_time_power,
                                                    over_time_constant, wait_time_constant,
                                                    previous_neighbourhood)
    return present_configuration, present_payoff


def execute(over_time_power, wait_time_constant, over_time_constant, start_time):
    # Initialize list of perturbations
    initialize_permutation_dictionary(20)

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
                                                                          wait_time_constant,
                                                                          {tuple(initial_configuration): 1})

        n_value_list.append(MAX_BOOKED - total_number_of_bookings)
        payoff_value_list.append(optimal_payoff)
        row_value = [MAX_BOOKED - total_number_of_bookings, optimal_payoff]
        for slot in range(NUMBER_OF_SLOTS): row_value.append(optimal_config[slot])
        output_rows.append(row_value)

        print "\nFinal, Most Optimal Output for N ", MAX_BOOKED - total_number_of_bookings, "configuration and payoff ", \
            optimal_config, optimal_payoff, time.time() - start_time
        if optimal_payoff > highest_payoff:
            highest_payoff = optimal_payoff
            highest_payoff_config = optimal_config
        elif stop_at_optimal_N_for_level_by_level_calculation:
            break

    return n_value_list, payoff_value_list, output_rows, highest_payoff_config, highest_payoff


def execute_across_n(over_time_power, wait_time_constant, over_time_constant):
    initialize_permutation_dictionary(20, True)

    initial_configuration = get_initial_configuration(0)
    initial_payoff = estimate_payoff(initial_configuration, show_up_prob, PER_SLOT_PROCESSING, wait_time_constant,
                                     over_time_constant, over_time_power)

    previous_neighbourhood = {tuple(initial_configuration): 1}

    return optimize_from_given_start_config(initial_configuration, initial_payoff, over_time_power,
                                            over_time_constant, wait_time_constant, previous_neighbourhood)


# external entry point for optimal Schedule Calculation
def set_params_and_get_optimal_schedule(MAX_BOOKED_PARAM, show_up_prob_PARAM, PER_SLOT_PROCESSING_PARAM,
                                        NUMBER_OF_SLOTS_PARAM, over_time_power, wait_time_constant, over_time_constant,
                                        TAG="TAG", debug_logger_param=False,
                                        stop_at_optimal_N_for_level_by_level_calculation_param=False,
                                        search_across_N=False):
    global MAX_BOOKED, PER_SLOT_PROCESSING, NUMBER_OF_SLOTS, show_up_prob, N_CALCULATION_RANGE, stop_at_optimal_N_for_level_by_level_calculation, debug_logger, MINIMUM_BOOKED
    MAX_BOOKED = MAX_BOOKED_PARAM
    N_CALCULATION_RANGE = MAX_BOOKED_PARAM
    PER_SLOT_PROCESSING = PER_SLOT_PROCESSING_PARAM
    MINIMUM_BOOKED = PER_SLOT_PROCESSING_PARAM
    NUMBER_OF_SLOTS = NUMBER_OF_SLOTS_PARAM
    show_up_prob = show_up_prob_PARAM
    stop_at_optimal_N_for_level_by_level_calculation = stop_at_optimal_N_for_level_by_level_calculation_param
    debug_logger = debug_logger_param

    if search_across_N:
        return get_optimal_schedule_across_n(over_time_constant, wait_time_constant, over_time_power, TAG)
    else:
        return get_optimal_schedule(over_time_constant, wait_time_constant, over_time_power, TAG)


# internal entry point for optimal Schedule Calculation Across N
def get_optimal_schedule_across_n(over_time_constant=1.0, wait_time_constant=1.0, over_time_power=2, TAG="TAG"):
    start_time = print_parameters(TAG, over_time_constant, over_time_power, wait_time_constant, time.time())

    highest_payoff_config, highest_payoff = execute_across_n(over_time_power, wait_time_constant, over_time_constant)

    print_parameters(TAG, over_time_constant, over_time_power, wait_time_constant, start_time)
    #print "\tFinal Output for Optimal N configuration and payoff ", highest_payoff_config, highest_payoff, "\n\n"

    return highest_payoff_config, highest_payoff


# internal entry point for optimal Schedule Calculation
def get_optimal_schedule(over_time_constant=1.0, wait_time_constant=1.0, over_time_power=2, TAG="TAG"):
    start_time = print_parameters(TAG, over_time_constant, over_time_power, wait_time_constant, time.time())

    n_value_list, payoff_value_list, output_rows, highest_payoff_config, highest_payoff = \
        execute(over_time_power, wait_time_constant, over_time_constant, start_time)

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
    get_optimal_schedule_across_n()
