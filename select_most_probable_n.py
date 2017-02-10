import sys

from scipy import stats as ss


def compute_best_n(prob, max_value, min_value, n_start_point):
    n_associated_with_best_likelihood = -1
    best_likelihood = -sys.maxint - 1
    while (True):
        distribution = ss.binom(n_start_point, prob)
        likely_hood = 0
        for patient_number in range(min_value + 1, max_value + 1):
            likely_hood += distribution.pmf(patient_number)

        if likely_hood > best_likelihood:
            best_likelihood = likely_hood
            n_associated_with_best_likelihood = n_start_point
        else:
            break

        n_start_point += 1

    if n_associated_with_best_likelihood == -1:
        raise StandardError("Best n_associated_with_best_likelihood not found")

    return int(n_associated_with_best_likelihood), best_likelihood
