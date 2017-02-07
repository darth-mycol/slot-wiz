import csv
import time

import one_slot_model_calculate_optimal as range_calculator
import slot_distribution_calculator


def get_over_time_power_list():
    over_time_power_list = []
    for over_time_power in range(10, 21, 5):
        over_time_power_list.append(float(over_time_power) / 10)
    return over_time_power_list


def get_prob_list():
    probability_list = []
    for prob in range(50, 71, 5):
        probability_list.append(float(prob) / 100)
    for prob in range(80, 96, 5):
        probability_list.append(float(prob) / 100)
    probability_list.append(0.99)
    return probability_list


def get_boundary_dict(probability_list, total_processing):
    boundary_dict = {}
    for probability in probability_list:
        max_booked_range = int(float(total_processing) / probability)
        boundary_cost, boundary = range_calculator.set_parameters_and_get_optimal_n(
            total_processing, max_booked_range, probability)
        boundary_dict[probability] = boundary
    return boundary_dict


def get_loss_constant_pairs():
    return [(0, 1), (0, 1.5)]
    # return [(0, 1), (1, 1), (0.5, 1.5), (1.5, 1.5), (0, 1.5)]


# External Entry Point
def compute_optimal_schedule(loss_constant_pair_list, number_of_slots, over_time_power_list, per_slot_processing_list,
                             probability_list, search_across_n=True, TAG=""):
    total_processing = sum(per_slot_processing_list)
    boundary_dict = get_boundary_dict(probability_list, total_processing)  # Initialize loss constants
    heading = ["Probability", "Optimal N", "Pay Off", "Over Time Power", "Wait Time Constant", "Over Time Constant",
               "Time Taken", "Number of Slots", "Total Capacity"]
    for slot_number in range(number_of_slots): heading.append("Slot" + str(slot_number + 1))
    output_rows = [heading]
    for loss_constant_tuple in loss_constant_pair_list:
        wait_time_constant = loss_constant_tuple[0]
        over_time_constant = loss_constant_tuple[1]

        for over_time_power in over_time_power_list:
            for probability in probability_list:
                optimal_schedule_calculation_start = time.time()
                highest_payoff_config, highest_payoff = slot_distribution_calculator.set_params_and_get_optimal_schedule(
                    boundary_dict[probability], probability, per_slot_processing_list, number_of_slots, over_time_power,
                    wait_time_constant, over_time_constant, TAG=TAG, debug_logger_param=False,
                    stop_at_optimal_N_for_level_by_level_calculation_param=True, search_across_N=search_across_n)

                row_value = [probability, sum(highest_payoff_config), highest_payoff, over_time_power,
                             wait_time_constant, over_time_constant,
                             time.time() - optimal_schedule_calculation_start, number_of_slots, total_processing]
                for slot in range(number_of_slots): row_value.append(highest_payoff_config[slot])
                output_rows.append(row_value)
    filename = TAG + "PER_SLOT_" + str(max(per_slot_processing_list)) + "_" + "NUMBER_OF_SLOTS_" + str(number_of_slots)
    output_file = open("processed_Results/" + filename + ".csv", 'w')
    csv_file = csv.writer(output_file)
    csv_file.writerows(output_rows)
    output_file.close()


if __name__ == "__main__":
    number_of_slots = 3
    total_capacity = 200

    start_time = time.time()
    loss_constant_pair_list = get_loss_constant_pairs()
    over_time_power_list = get_over_time_power_list()  # Get list of probability to run over
    probability_list = get_prob_list()
    per_slot_processing_list = slot_distribution_calculator.get_initial_configuration(number_of_slots, total_capacity)

    # noinspection PyArgumentList
    TAG = "CAPACITY_" + str(total_capacity) + \
          time.strftime("_%b_%d_%H_%M_", time.strptime(time.ctime()))

    compute_optimal_schedule(loss_constant_pair_list, number_of_slots, over_time_power_list, per_slot_processing_list,
                             probability_list, False, TAG)

    print time.time() - start_time
