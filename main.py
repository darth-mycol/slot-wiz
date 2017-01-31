import csv
import time

import calculate_optimal_in_one_slot_model as range_calculator
import slot_distribution_calculator

PER_SLOT_PROCESSING = 67
NUMBER_OF_SLOTS = 3

# noinspection PyArgumentList
TAG = "CAPACITY_" + str(NUMBER_OF_SLOTS * PER_SLOT_PROCESSING) + time.strftime("_%b_%d_%H_%M_",
                                                                               time.strptime(time.ctime()))

if __name__ == "__main__":
    # Get list of over time powers to iterate over
    over_time_power_list = []
    for over_time_power in range(10, 21, 10):
        over_time_power_list.append(float(over_time_power) / 10)

    # Get list of probability to run over
    probability_list = []
    for prob in range(50, 91, 20):
        probability_list.append(float(prob) / 100)
    # for prob in range(80, 96, 10):
    #     probability_list.append(float(prob) / 100)
    #probability_list.append(0.99)

    # Initialize Output File Contents
    total_processing = PER_SLOT_PROCESSING * NUMBER_OF_SLOTS
    heading = ["Probability", "Optimal N", "Pay Off", "Over Time Power", "Wait Time Constant", "Over Time Constant"]
    for slot_number in range(NUMBER_OF_SLOTS): heading.append("Slot" + str(slot_number + 1))
    output_rows = [heading]

    # Initialize Boundary Ranges to search for optimal N
    boundary_dict = {}
    for probability in probability_list:
        max_booked_range = int(float(total_processing) / probability)
        boundary_cost, boundary = range_calculator.set_parameters_and_get_optimal_n(
            total_processing, max_booked_range, probability)
        boundary_dict[probability] = boundary

    # Initialize loss constants
    lost_constant_pair_list = [(0.5, 1.5), (1.5, 1.5)]

    for loss_constant_tuple in lost_constant_pair_list:
        wait_time_constant = loss_constant_tuple[0]
        over_time_constant = loss_constant_tuple[1]

        for over_time_power in over_time_power_list:
            for probability in probability_list:
                highest_payoff_config, highest_payoff = slot_distribution_calculator.set_params_and_get_optimal_schedule(
                    boundary_dict[probability], probability, PER_SLOT_PROCESSING, NUMBER_OF_SLOTS, over_time_power,
                    wait_time_constant, over_time_constant, TAG=TAG, debug_logger_param=False,
                    stop_at_optimal_N_for_level_by_level_calculation_param=True)

                row_value = [probability, sum(highest_payoff_config), highest_payoff, over_time_power,
                             wait_time_constant, over_time_constant]
                for slot in range(NUMBER_OF_SLOTS): row_value.append(highest_payoff_config[slot])
                output_rows.append(row_value)

    filename = TAG + "PER_SLOT_" + str(PER_SLOT_PROCESSING) + "_" + "NUMBER_OF_SLOTS_" + str(NUMBER_OF_SLOTS)
    output_file = open("Aggregated-csv/" + filename + ".csv", 'w')
    csv_file = csv.writer(output_file)
    csv_file.writerows(output_rows)
    output_file.close()
