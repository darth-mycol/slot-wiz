import time
from os import walk

estimate_dictionary = {}


class Estimate_values:
    def __init__(self, n, prange):
        self.optimal_n = n
        self.prob_range = prange


ESTIMATE_DICTIONARY = "estimate_dictionary/"


def initialize():
    start_time = time.time()

    path = ESTIMATE_DICTIONARY
    file_name_list = []
    for (d_path, d_names, f_names) in walk(path):
        file_name_list.extend(f_names)
        break

    for file_name in file_name_list:
        if ".py" in file_name or ".DS_STORE" in file_name:
            continue
        for index, line in enumerate(open(ESTIMATE_DICTIONARY + file_name, "r").readlines()):
            terms = line.split(",")
            # Skip the header line and any lines without all the fields (and blank lines)
            if index == 0 or len(terms) < 4:
                continue

            prob = float(terms[2])
            capacity = int(terms[3])

            estimate = Estimate_values(terms[0], terms[1])

            estimate_dictionary[(prob, capacity)] = estimate

    return time.time() - start_time


def retrieve_values(prob, capacity):
    estimate = estimate_dictionary.get((prob, capacity))
    if estimate is None:
        return 0, 0
    return estimate.optimal_n, estimate.prob_range


initialize()
