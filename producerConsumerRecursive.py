import scipy.stats as ss
import time

MAX_BOOKED = 376
MINIMUM_BOOKED = 100
PER_SLOT_PROCESSING = 100
MINIMUM_SHOW = 0
NUMBER_OF_SLOTS = 2
show_up_prob = 0.5
permutation_dictionary_list = []


def calculate_benefit(gain, wait, loss):
    if wait == 0:
        return gain - loss
    else:
        overbooked_cost = wait * wait
        wait_copy = wait - PER_SLOT_PROCESSING
        overbooked_wait_cascading_cost = 0
        while (wait_copy > 0) :
            overbooked_wait_cascading_cost += wait_copy
            wait_copy -= PER_SLOT_PROCESSING

        return gain + wait - (overbooked_wait_cascading_cost + loss + overbooked_cost)


def get_recursive_benefit(slot_booked_list):
    slot_distribution_list = []
    for term in slot_booked_list:
        slot_distribution_list.append(ss.binom(term, show_up_prob))
    return recursive_benefit_calculation(1, 0, 0, 0, slot_distribution_list, slot_booked_list, 0)


def recursive_benefit_calculation(prob, gain, wait, loss, slot_distribution_list, slot_booked_list, recursive_level):
    # eliminate the recursive_level later. - buggy
    slot_booked = slot_booked_list[recursive_level]
    slot_distribution = slot_distribution_list[recursive_level]

    present_level_benefit = 0
    for slot_show_up in range(slot_booked + 1):
        slot_probability = slot_distribution.pmf(slot_show_up)
        attendance = slot_show_up + wait
        slot_gain = min(attendance, PER_SLOT_PROCESSING)
        slot_over_load = attendance - slot_gain

        if recursive_level == NUMBER_OF_SLOTS - 1:
            present_level_benefit += prob * slot_probability * calculate_benefit(slot_gain + gain, slot_over_load,
                                                                                 loss + slot_over_load)
        else:
            present_level_benefit += recursive_benefit_calculation(prob * slot_probability, slot_gain + gain,
                                                                   slot_over_load,
                                                                   loss + slot_over_load, slot_distribution_list,
                                                                   slot_booked_list,
                                                                   recursive_level + 1)
    return present_level_benefit


def get_perturbations(present_configuration, earlier_configuration):
    perturbation_list = []
    for variation in permutation_dictionary_list:
        left = present_configuration[:]
        non_zero = True
        for index, term in enumerate(left):
            term += variation[index]
            left[index] = term
            if term < 0:
                non_zero = False
                break
        if non_zero:
            add_unique_perturbation(left, perturbation_list, earlier_configuration)

    return perturbation_list


def add_unique_perturbation(left, perturbations, previous):
    if previous is not None and len(previous) > 0 and previous == left:
        pass
    else:
        perturbations.append(left)


def optimize_from_given_vector(present_configuration, present_benefit, previous_configuration):
    perturbations = get_perturbations(present_configuration, previous_configuration)
    best_variation = []
    value_for_best_perturbation = -1
    improvement_possible = False
    for variation in perturbations:
        perturbation_benefit = get_recursive_benefit(variation)
        if perturbation_benefit > present_benefit:
            best_variation = variation[:]
            value_for_best_perturbation = perturbation_benefit
            improvement_possible = True

    if improvement_possible:
        print best_variation, value_for_best_perturbation, present_configuration, time.time()
        return optimize_from_given_vector(best_variation, value_for_best_perturbation, present_configuration)
    else:
        return present_configuration, present_benefit


def produce():
    initial_configuration = [MAX_BOOKED/NUMBER_OF_SLOTS for x in range(NUMBER_OF_SLOTS)]
    initial_benefit = get_recursive_benefit(initial_configuration)

    return optimize_from_given_vector(initial_configuration, initial_benefit, [])


def populate_permutations(incomplete_list, recursive_level):
    for term in range(-1, 1+1, 1):
        permutation = incomplete_list[:]
        permutation.append(term)
        if recursive_level == NUMBER_OF_SLOTS - 1:
            permutation_dictionary_list.append(permutation)
        else:
            populate_permutations(permutation, recursive_level + 1)


def brute_producer():
    populate_permutations([], 0)
    # variation = []
    # value_with_best_permutation = -1
    # for permutation in permutation_dictionary.keys():
    #     permutation_benefit = get_recursive_benefit(permutation)
    #     if permutation_benefit > value_with_best_permutation:
    #         value_with_best_permutation = permutation_benefit
    #         variation = permutation_benefit
    #
    # return variation, value_with_best_permutation


brute_producer()
optimal_configuration, optimal_benefit = produce()
print optimal_configuration, optimal_benefit




# def populate_permutations(total, incomplete_list, recursive_level):
#     max_range = MAX_BOOKED - total - (NUMBER_OF_SLOTS * MINIMUM_BOOKED) + 1
#     for term in range(-1, 1, 1):
#         permutation = incomplete_list[:]
#         permutation.append(term)
#         if recursive_level == NUMBER_OF_SLOTS - 1:
#             permutation_dictionary[permutation] = 1
#         else:
#             populate_permutations(total + term, incomplete_list, recursive_level + 1)
#
#
# def brute_producer():
#     populate_permutations(0, [], 0)
#     variation = []
#     value_with_best_permutation = -1
#     for permutation in permutation_dictionary.keys():
#         permutation_benefit = get_recursive_benefit(permutation)
#         if permutation_benefit > value_with_best_permutation:
#             value_with_best_permutation = permutation_benefit
#             variation = permutation_benefit
#
#     return variation, value_with_best_permutation
