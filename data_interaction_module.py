import time
from os import walk

import pandas as pd

# This is the Data Interaction for the system using the Pandas Library, reading from pre-prepared excel sheets.
# One needs to only substitute this module if the data interaction needs to change, to say a mongo set up

# Static
CSV_FORMAT = ".csv"
PAY_OFF = "pay_off"
SLOT_COLUMN_NAME = 'slot'
NUMBER_OF_SLOTS = 'number_of_slots'
ALLOWED_SLOT_TYPES = [24, 12, 3, 2, 1]
PROCESSED_RESULTS = "processed_Results/"

# Dynamic
data_frame_dictionary = {}


def add_to_dictionary(key, df_list):
    global data_frame_dictionary
    if key in data_frame_dictionary.keys():
        for df in df_list:
            data_frame_dictionary[key].append(df, ignore_index=True)
    else:
        initial = df_list[0]
        for index in range(1, len(df_list)):
            df = df_list[index]
            initial = initial.append(df, ignore_index=True)
            data_frame_dictionary[key] = initial


# a consumer module will them come looking with an N.
# it will check if the producer dictionary has such an entity. if yes then it will look it up, read the same and return.
# if not it will just give that the production has not completed.
# it will ask: do you want to reinitialize the reading if the database has been updated?
def look_up_dictionary(p, number_of_slots, N, over_time_constant=1, wait_time_constant=1, over_time_power=2):
    global data_frame_dictionary
    if number_of_slots not in data_frame_dictionary.keys():
        "The payoff is not previously calculated for given number of slots.\nDo you want to re-initialize?"
        return None, None

    df = data_frame_dictionary[number_of_slots]
    row = df[df.probability == p][df.over_time_constant == over_time_constant][
        df.wait_time_constant == wait_time_constant][
        df.over_time_power == over_time_power][df.total_capacity == N]

    if len(row) == 0:
        print "The payoff is not previously calculated.\nDo you want to re-initialize?"
        return None, None

    row = row[0:1]
    schedule = []
    for slot_number in range(number_of_slots):
        schedule.append(list(row[SLOT_COLUMN_NAME + str(slot_number + 1)])[0])
    return schedule, list(row[PAY_OFF])[0]


def initialize():
    start_time = time.time()

    path = PROCESSED_RESULTS
    file_name_list = []
    for (d_path, d_names, f_names) in walk(path):
        file_name_list.extend(f_names)
        break

    key_to_df_list = {}
    for file_name in file_name_list:
        df = pd.read_csv(path + file_name)
        df.columns = [c.replace(' ', '_').lower() for c in df.columns]

        if not CSV_FORMAT in file_name: continue

        number_of_slots = df[NUMBER_OF_SLOTS][0]
        if not number_of_slots in ALLOWED_SLOT_TYPES:
            print "Skipped File as number of slots not supported. FileName : ", file_name
            continue

        if number_of_slots in key_to_df_list.keys():
            key_to_df_list[number_of_slots].append(df)
        else:
            key_to_df_list[number_of_slots] = [df]

    for key in key_to_df_list.keys():
        add_to_dictionary(key, key_to_df_list[key])

    return time.time() - start_time


# Run when module is imported
initialize()

if __name__ == "__main__":
    print look_up_dictionary(0.5, 3, 202, 1, 1, 2)
