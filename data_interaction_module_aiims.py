import csv
import inspect
import os
import time
from os import walk

estimate_dictionary = {}
date_wise_estimate_dictionary = {}


class Estimate_values:
    def __init__(self, n, prange):
        self.optimal_n = n
        self.prob_range = prange


date_time_format = "%a_%b_%d_%H_%M_%S"

ESTIMATE_DICTIONARY = "/estimate_dictionary/"
DATE_DICTIONARY = "/date_dictionary/"
PREVIOUS_DICTIONARY = "/previous_dictionary/previous_days_data.csv"


def write_one_optimal_by_date_file(output_rows, capacity="All", department="All"):
    filename = time.strftime(date_time_format) + "_CAPACITY_" + str(capacity) + "_department_" + str(department) + "_optimal_no_by_date"
    path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + DATE_DICTIONARY
    output_file = open(path + filename + ".csv", 'w')
    csv_file = csv.writer(output_file)
    csv_file.writerows(output_rows)
    output_file.close()


def initialize_estimate_dictionary_by_date():
    start_time = time.time()

    path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + DATE_DICTIONARY
    print path
    file_name_list = []
    for (d_path, d_names, f_names) in walk(path):
        file_name_list.extend(f_names)
        break

    for file_name in file_name_list:
        if ".py" in file_name or ".DS_STORE" in file_name:
            continue
        for index, line in enumerate(open(path + file_name, "r").readlines()):
            terms = line.split(",")
            # Skip the header line and any lines without all the fields (and blank lines)
            if index == 0 or len(terms) < 4:
                continue

            date = terms[2]
            department = int(terms[3])
            capacity = int(terms[4])

            estimate = Estimate_values(terms[0], terms[1])

            date_wise_estimate_dictionary[(date, department, capacity)] = estimate

    return time.time() - start_time


def initialize_estimate_dictionary():
    start_time = time.time()

    path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + ESTIMATE_DICTIONARY
    file_name_list = []
    for (d_path, d_names, f_names) in walk(path):
        file_name_list.extend(f_names)
        break

    for file_name in file_name_list:
        if ".py" in file_name or ".DS_STORE" in file_name:
            continue
        for index, line in enumerate(open(path + file_name, "r").readlines()):
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
        return None, None
    return estimate.optimal_n, estimate.prob_range


def retrieve_values_by_date(date, department, capacity):
    estimate = date_wise_estimate_dictionary.get((date, department, capacity))
    if estimate is None:
        return None, None
    return estimate.optimal_n, estimate.prob_range


def save_values_by_date(date, department, booked, actual_show_up):
    start_time = time.time()

    path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + PREVIOUS_DICTIONARY
    try:
        os.open(path, os.O_CREAT | os.O_EXCL)
        with open(path, "a") as dictionary:
            dictionary.write("Date,Department,Booked,Actual_show_up")
    except Exception:
        pass  # ignored

    with open(path, "a") as dictionary:
        dictionary.write("\n" + str(date) + "," + str(department) + "," + str(booked) + "," + str(actual_show_up))

    return time.time() - start_time

initialize_estimate_dictionary_by_date()
initialize_estimate_dictionary()

if __name__ == "__main__":
    initialize_estimate_dictionary_by_date()
    retrieve_values_by_date("1/1/2017", 1, 100)
