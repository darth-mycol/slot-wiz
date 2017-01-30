import csv
import time

import calculate_optimal_in_one_slot_model as range_calculator
import slot_distribution_calculator

PER_SLOT_PROCESSING = 1
NUMBER_OF_SLOTS = 24

# noinspection PyArgumentList
TAG = "CAPACITY_" + str(NUMBER_OF_SLOTS * PER_SLOT_PROCESSING) + time.strftime("_%b_%d_%H_%M_", time.strptime(time.ctime()))

if __name__ == "__main__":
    # Get list of over time powers to iterate over
    over_time_power_list = []
    for over_time_power in range(10, 31, 5):
        over_time_power_list.append(float(over_time_power) / 10)

    # Get list of probability to run over
    probability_list = []
    for prob in range(80, 96, 5):
        probability_list.append(float(prob) / 100)
    probability_list.append(0.99)
    for prob in range(40, 71, 5):
        probability_list.append(float(prob) / 100)

    # Initialize Output File Contents
    total_processing = PER_SLOT_PROCESSING * NUMBER_OF_SLOTS
    heading = ["Probability", "Optimal N", "Pay Off", "Over Time Power"]
    for slot_number in range(NUMBER_OF_SLOTS): heading.append("Slot" + str(slot_number + 1))
    output_rows = [heading]

    # Initialize Boundary Ranges to search for optimal N
    boundary_dict = {}
    for probability in probability_list:
        max_booked_range = int(float(total_processing) / probability)
        boundary_cost, boundary = range_calculator.set_parameters_and_get_optimal_n(
            total_processing, max_booked_range, probability)
        boundary_dict[probability] = boundary

    for over_time_power in over_time_power_list:
        for probability in probability_list:
            highest_payoff_config, highest_payoff = slot_distribution_calculator.set_params_and_get_optimal_schedule(
                boundary_dict[probability], probability, PER_SLOT_PROCESSING, NUMBER_OF_SLOTS, over_time_power,
                stop_at_optimal_N_for_level_by_level_calculation_param=True, TAG=TAG, debug_logger_param=True)

            row_value = [probability, sum(highest_payoff_config), highest_payoff, over_time_power]
            for slot in range(NUMBER_OF_SLOTS): row_value.append(highest_payoff_config[slot])
            output_rows.append(row_value)

    filename = TAG + "PER_SLOT_" + str(PER_SLOT_PROCESSING) + "_" + "NUMBER_OF_SLOTS_" + str(NUMBER_OF_SLOTS)
    output_file = open("Aggregated-csv/" + filename + ".csv", 'w')
    csv_file = csv.writer(output_file)
    csv_file.writerows(output_rows)
    output_file.close()
