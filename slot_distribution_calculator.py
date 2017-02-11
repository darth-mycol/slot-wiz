import csv
import itertools as itools
import sys
import time

from slot_schedule_payoff_calculator import estimate_payoff

debug_logger = True
permutation_dictionary_list = []


def add_sample_to_permutation_dictionary(index, permutation_dictionary_list, total_possibilities, sample_size,
                                         single_sample_dictionary):
    if len(single_sample_dictionary) > sample_size or index == total_possibilities - 1:
        permutation_dictionary_list.append(single_sample_dictionary[:])
        single_sample_dictionary = []
    return single_sample_dictionary


def initialize_permutation_dictionary(sample_size, total_number_of_slots, permutation_across_n=False):
    global permutation_dictionary_list
    permutation_dictionary_list = []
    if total_number_of_slots > 1:
        single_sample_dictionary = []
        if permutation_across_n:
            for index in range(total_number_of_slots):
                configuration = [0 for x in range(total_number_of_slots)]
                configuration[index] = -1
                single_sample_dictionary.append(configuration[:])
                configuration[index] = 1
                single_sample_dictionary.append(configuration[:])

                single_sample_dictionary = add_sample_to_permutation_dictionary(index, permutation_dictionary_list,
                                                                                total_number_of_slots, sample_size,
                                                                                single_sample_dictionary)
        else:
            position_permutations = set(list(itools.permutations(range(total_number_of_slots), 2)))
            for index, position_configuration in enumerate(position_permutations):
                configuration = [0 for x in range(total_number_of_slots)]
                configuration[position_configuration[0]] = -1
                configuration[position_configuration[1]] = 1
                single_sample_dictionary.append(configuration[:])
                single_sample_dictionary = add_sample_to_permutation_dictionary(index, permutation_dictionary_list,
                                                                                len(position_permutations), sample_size,
                                                                                single_sample_dictionary)


def print_parameters(TAG, over_time_constant, over_time_power, wait_time_constant, previous_time, max_booked,
                     total_number_of_slots, show_up_prob):
    print "\n********Parameters : max_booked, total_number_of_slots, p, Over_Time_Power, over_time_constant, wait_time_constant, TAG, processing_time*******\n", \
        max_booked, total_number_of_slots, show_up_prob, over_time_power, over_time_constant, wait_time_constant, TAG, time.time() - previous_time, "\n"
    return time.time()


def get_initial_configuration(number_of_slots, booked_to_be_distributed, iterator=0):
    schedule = []
    for i in range(number_of_slots, 0, -1):
        schedule.append((booked_to_be_distributed + (i - 1) - iterator) / number_of_slots)
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


def optimize_from_given_start_config(present_configuration, present_payoff, over_time_power, over_time_constant,
                                     wait_time_constant, previous_neighbourhood, per_slot_processing_list,
                                     show_up_prob):
    best_variation = []
    value_for_best_perturbation = -sys.maxint - 1
    for single_sample_dictionary in permutation_dictionary_list:
        perturbation_list = get_perturbation_list(present_configuration, previous_neighbourhood,
                                                  single_sample_dictionary)
        for variation in perturbation_list:
            perturbation_payoff = estimate_payoff(variation, show_up_prob, per_slot_processing_list, wait_time_constant,
                                                  over_time_constant, over_time_power)
            if perturbation_payoff > value_for_best_perturbation:
                best_variation = variation[:]
                value_for_best_perturbation = perturbation_payoff

        if value_for_best_perturbation > present_payoff:
            if debug_logger:
                print "LOGGER best_variation, value_for_best_perturbation, present_configuration, time", best_variation, value_for_best_perturbation, present_configuration, time.time()
            return optimize_from_given_start_config(best_variation, value_for_best_perturbation, over_time_power,
                                                    over_time_constant, wait_time_constant, previous_neighbourhood,
                                                    per_slot_processing_list, show_up_prob)
    return present_configuration, present_payoff


def execute(over_time_power, wait_time_constant, over_time_constant, start_time, per_slot_processing_list,
            stop_at_optimal_N_for_level_by_level_calculation, total_number_of_slots, max_booked, show_up_prob):
    # Initialize list of perturbations
    initialize_permutation_dictionary(20, total_number_of_slots)

    heading = ["N", "PAYOFF"]
    for slot_number in range(total_number_of_slots): heading.append("Optimal Slot" + str(slot_number + 1))
    output_rows = [heading]

    # Initialize Execution Parameters
    n_value_list = []
    payoff_value_list = []

    highest_payoff = -sys.maxint - 1
    highest_payoff_config = []
    max_per_slot_processing = max(per_slot_processing_list)
    for total_number_of_bookings in range(0, min(max_booked - total_number_of_slots * max_per_slot_processing + 1,
                                                 max_booked)):
        initial_configuration = get_initial_configuration(total_number_of_slots, max_booked, total_number_of_bookings)
        initial_payoff = estimate_payoff(initial_configuration, show_up_prob, per_slot_processing_list,
                                         wait_time_constant, over_time_constant, over_time_power)
        optimal_config, optimal_payoff = optimize_from_given_start_config(initial_configuration, initial_payoff,
                                                                          over_time_power, over_time_constant,
                                                                          wait_time_constant,
                                                                          {tuple(initial_configuration): 1},
                                                                          per_slot_processing_list, show_up_prob)

        n_value_list.append(max_booked - total_number_of_bookings)
        payoff_value_list.append(optimal_payoff)
        row_value = [max_booked - total_number_of_bookings, optimal_payoff]
        for slot in range(total_number_of_slots): row_value.append(optimal_config[slot])
        output_rows.append(row_value)

        print "\nFinal, Most Optimal Output for N ", max_booked - total_number_of_bookings, "configuration and payoff ", \
            optimal_config, optimal_payoff, time.time() - start_time
        if optimal_payoff > highest_payoff:
            highest_payoff = optimal_payoff
            highest_payoff_config = optimal_config
        elif stop_at_optimal_N_for_level_by_level_calculation:
            break

    return n_value_list, payoff_value_list, output_rows, highest_payoff_config, highest_payoff


def execute_across_n(per_slot_processing_list, over_time_power, wait_time_constant, over_time_constant,
                     total_number_of_slots, max_booked, show_up_prob):
    initialize_permutation_dictionary(20, total_number_of_slots, True)

    initial_configuration = get_initial_configuration(total_number_of_slots, max_booked)
    initial_payoff = estimate_payoff(initial_configuration, show_up_prob, per_slot_processing_list, wait_time_constant,
                                     over_time_constant, over_time_power)

    previous_neighbourhood = {tuple(initial_configuration): 1}

    return optimize_from_given_start_config(initial_configuration, initial_payoff, over_time_power, over_time_constant,
                                            wait_time_constant, previous_neighbourhood, per_slot_processing_list,
                                            show_up_prob)


# external entry point for optimal Schedule Calculation
def set_params_and_get_optimal_schedule(max_booked, show_up_prob, per_slot_processing_list,
                                        total_number_of_slots, over_time_power, wait_time_constant, over_time_constant,
                                        TAG="TAG", debug_logger_param=False,
                                        stop_at_optimal_N_for_level_by_level_calculation=False,
                                        search_across_N=False):
    global debug_logger
    debug_logger = debug_logger_param

    if search_across_N:
        return get_optimal_schedule_across_n(per_slot_processing_list, max_booked, total_number_of_slots, show_up_prob,
                                             over_time_constant, wait_time_constant, over_time_power, TAG)
    else:
        return get_optimal_schedule(per_slot_processing_list, stop_at_optimal_N_for_level_by_level_calculation,
                                    max_booked, total_number_of_slots, show_up_prob,
                                    wait_time_constant, over_time_power, TAG, over_time_constant)


# internal entry point for optimal Schedule Calculation Across N
def get_optimal_schedule_across_n(per_slot_processing_list, max_booked, total_number_of_slots, show_up_prob,
                                  over_time_constant=1.0, wait_time_constant=1.0,
                                  over_time_power=2, TAG="TAG"):
    start_time = print_parameters(TAG, over_time_constant, over_time_power, wait_time_constant, time.time(), max_booked,
                                  total_number_of_slots, show_up_prob)

    highest_payoff_config, highest_payoff = execute_across_n(per_slot_processing_list, over_time_power,
                                                             wait_time_constant, over_time_constant,
                                                             total_number_of_slots, max_booked, show_up_prob)

    print_parameters(TAG, over_time_constant, over_time_power, wait_time_constant, start_time, max_booked,
                     total_number_of_slots, show_up_prob)

    return highest_payoff_config, highest_payoff


# internal entry point for optimal Schedule Calculation
def get_optimal_schedule(per_slot_processing_list, stop_at_optimal_N_for_level_by_level_calculation, max_booked,
                         total_number_of_slots, show_up_prob,
                         wait_time_constant=1.0, over_time_power=2, TAG="TAG", over_time_constant=1.0):
    start_time = print_parameters(TAG, over_time_constant, over_time_power, wait_time_constant, time.time(), max_booked,
                                  total_number_of_slots, show_up_prob)

    n_value_list, payoff_value_list, output_rows, highest_payoff_config, highest_payoff = \
        execute(over_time_power, wait_time_constant, over_time_constant, start_time, per_slot_processing_list,
                stop_at_optimal_N_for_level_by_level_calculation, total_number_of_slots, max_booked, show_up_prob)

    print_parameters(TAG, over_time_constant, over_time_power, wait_time_constant, start_time, max_booked,
                     total_number_of_slots, show_up_prob)
    print "\tFinal Output for Optimal N configuration and payoff ", highest_payoff_config, highest_payoff, "\n\n"

    filename = TAG + "max_booked_" + str(max_booked) + "_" + "total_number_of_slots_" + str(
        total_number_of_slots) + "_prob_" + str(show_up_prob)
    output_file = open("Output-csv/" + filename + ".csv", 'w')
    csv_file = csv.writer(output_file)
    csv_file.writerows(output_rows)
    output_file.close()

    # plt.plot(n_value_list, payoff_value_list)
    # plt.savefig("Output-png/" + filename + ".png", bbox_inches='tight')

    return highest_payoff_config, highest_payoff


if __name__ == "__main__":
    get_optimal_schedule([67, 67, 66], True, 375, 3, 0.5)
