import calculate_optimal_in_one_slot_model as range_calculator
import slot_distribution_calculator

PER_SLOT_PROCESSING = 3
NUMBER_OF_SLOTS = 3

if __name__ == "__main__":
    # Get list of probability to run over
    probability_list = []
    for prob in range(40, 71, 5):
        probability_list.append(float(prob) / 100)
    for prob in range(80, 96, 5):
        probability_list.append(float(prob) / 100)
    probability_list.append(0.99)

    total_processing = PER_SLOT_PROCESSING * NUMBER_OF_SLOTS
    for probability in probability_list:
        MAX_BOOKED = int(float(total_processing) / probability)
        boundary_cost, boundary = range_calculator.set_parameters_and_get_optimal_n(
            total_processing, MAX_BOOKED, probability)

        slot_distribution_calculator.set_parameters_and_get_optimal_distribution(boundary, probability,
                                                                                 PER_SLOT_PROCESSING,
                                                                                 NUMBER_OF_SLOTS,
                                                                                 "TRIAL_RUN_3_DIMENSION")
