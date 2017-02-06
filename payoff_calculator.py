import math

from scipy import stats as ss


def get_previous_waiting(earlier_slot_waiting, slot_number, probability_dict):
    if not probability_dict.has_key((slot_number, earlier_slot_waiting)):
        # Should not Happen
        raise Exception(
            "Earlier Probability not found. Key: (earlier_slot_waiting, slot_number), and past_probabilities_dict",
            earlier_slot_waiting, slot_number, probability_dict)

    return probability_dict.get((slot_number, earlier_slot_waiting))


# all values from 0 to per_slot for previous slot
def get_theta_summation(probability_dict, slot_number):
    return 1 if slot_number == -1 else get_previous_waiting(0, slot_number - 1, probability_dict)


def get_present_waiting(number_show_up, appointments_booked_in_slot, slot_show_up_distribution):
    if appointments_booked_in_slot < number_show_up:
        # Should not Happen
        raise Exception(
            "Number Show Up somehow greater than total booking",
            number_show_up, appointments_booked_in_slot, slot_show_up_distribution)
    else:
        return slot_show_up_distribution.pmf(number_show_up)


def estimate_loss(number_of_slots, per_slot_processing, show_up_prob, schedule, probability_dict,
                  over_time_power):
    if len(schedule) != number_of_slots or number_of_slots < 1: raise Exception("len(schedule) != NUMBER_OF_SLOTS")
    max_possible_carry_over = 0
    total_wait_loss = 0

    all_theta_prob_dictionary_for_schedule = {}
    for slot_number in range(number_of_slots):
        booked_appointments = schedule[slot_number]
        if max_possible_carry_over + booked_appointments <= per_slot_processing:
            probability_dict[(slot_number, 0)] = 1
            max_possible_carry_over = 0
            continue

        prob_of_at_least_one_over_load = 0
        patient_show_up_distribution = ss.binom(booked_appointments, show_up_prob)
        for over_load in range(0, max_possible_carry_over + booked_appointments + 1):
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

            all_theta_prob_dictionary_for_schedule[(slot_number, over_load)] = prob
            if over_load > per_slot_processing:
                total_waiting_at_slot_end = over_load - per_slot_processing
                probability_dict[(slot_number, total_waiting_at_slot_end)] = prob
                total_wait_loss += total_waiting_at_slot_end * prob
                prob_of_at_least_one_over_load += prob

        max_possible_carry_over = max(max_possible_carry_over + booked_appointments - per_slot_processing, 0)

        probability_dict[(slot_number, 0)] = 1 - prob_of_at_least_one_over_load

    over_time_loss = 0
    for over_book in range(1, max_possible_carry_over + 1):
        theta = get_previous_waiting(over_book, number_of_slots - 1, probability_dict)
        over_time_loss += theta * math.pow(over_book, over_time_power)

        overbooked_wait_cascading_cost = 0
        over_book_wait_loss = over_book - per_slot_processing
        while over_book_wait_loss > 0:
            overbooked_wait_cascading_cost += over_book_wait_loss
            over_book_wait_loss -= per_slot_processing

        total_wait_loss += overbooked_wait_cascading_cost * theta

    return total_wait_loss, over_time_loss


# external entry point
def estimate_payoff(schedule, show_up_prob, per_slot_processing, wait_time_constant=1, over_time_constant=1,
                    over_time_power=2):
    gain = sum(schedule) * show_up_prob
    wait_loss, over_time_loss = estimate_loss(len(schedule), per_slot_processing, show_up_prob,
                                              schedule, {(-1, 0): 1}, over_time_power)

    return gain - wait_time_constant * wait_loss - over_time_constant * over_time_loss


# external entry point for payoff calculation
def set_parameters_and_estimate_payoff(show_up_prob_PARAM, per_slot_processing, NUMBER_OF_SLOTS_PARAM, total_booking,
                                       wait_time_constant, over_time_constant):
    configuration = []
    for i in range(NUMBER_OF_SLOTS_PARAM, 0, -1):
        configuration.append((total_booking + (i - 1)) / NUMBER_OF_SLOTS_PARAM)

    return configuration[:], estimate_payoff(configuration, show_up_prob_PARAM, per_slot_processing, wait_time_constant,
                                             over_time_constant)


def test_estimate_payoff(configuration):
    return configuration[:], estimate_payoff(configuration, 0.5, 67, 1, 1)


if __name__ == "__main__":
    test_estimate_payoff([400,0,0])