import csv

import calculate_optimal_in_one_slot_model as range_calculator
import slot_distribution_calculator

PER_SLOT_PROCESSING = 66
NUMBER_OF_SLOTS = 3
TAG = "CAPACITY_198_SLOTS_3"

if __name__ == "__main__":
    # Get list of probability to run over
    probability_list = []
    for prob in range(40, 71, 5):
        probability_list.append(float(prob) / 100)
    for prob in range(80, 96, 5):
        probability_list.append(float(prob) / 100)
    probability_list.append(0.99)

    total_processing = PER_SLOT_PROCESSING * NUMBER_OF_SLOTS
    heading = ["Prob", "N", "PAYOFF"]
    for slot_number in range(NUMBER_OF_SLOTS): heading.append("Optimal Slot" + str(slot_number + 1))
    output_rows = [heading]

    for probability in probability_list:
        MAX_BOOKED = int(float(total_processing) / probability)
        boundary_cost, boundary = range_calculator.set_parameters_and_get_optimal_n(
            total_processing, MAX_BOOKED, probability)

        highest_payoff_config, highest_payoff = slot_distribution_calculator.set_parameters_and_get_optimal_distribution(
            boundary, probability, PER_SLOT_PROCESSING, NUMBER_OF_SLOTS, TAG,
            stop_at_optimal_N_for_level_by_level_calculation_param=True)
        row_value = [probability, sum(highest_payoff_config), highest_payoff]
        for slot in range(NUMBER_OF_SLOTS): row_value.append(highest_payoff_config[slot])
        output_rows.append(row_value)

    filename = TAG + "PER_SLOT_" + str(PER_SLOT_PROCESSING) + "_" + "NUMBER_OF_SLOTS_" + str(NUMBER_OF_SLOTS)
    output_file = open("Aggregated-csv/" + filename + ".csv", 'w')
    csv_file = csv.writer(output_file)
    csv_file.writerows(output_rows)
    output_file.close()
