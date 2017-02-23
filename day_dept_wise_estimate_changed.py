import pandas as pd

import data_interaction_module_aiims

PROBABILITY_XLS = "pickup_dictionary/predicted_probability.xls"

input_format = "%m/%d/%Y"
date_format = "%d/%m/%Y"


def get_capacity_list():
    return [100,135,150,200]


if __name__ == "__main__":
    output_rows = [
            ["optimalnumber", "probabilityrange", "date", "department", "capacity", "probability", "day", "month"]]
    department_wise_df_dict = {}
    for sn in pd.ExcelFile(PROBABILITY_XLS).sheet_names:
        department_wise_df_dict[sn] = pd.read_excel(PROBABILITY_XLS, sheetname=sn)

    department_number_dicionary = {"Medicine" : 1,  "Ortho" : 2, "Skin" : 3}
    capacity_list = get_capacity_list()
    for department_number in department_number_dicionary.items():

        department = department_number[1]
        df = department_wise_df_dict[department_number[0]]

        final_date_time_prob_dict = {}

        df.columns = ["A", "B"]
        date_list = df["A"]
        prob_list = df["B"]

        for date_entry_row, probability_for_date in zip(date_list, prob_list):
            if pd.isnull(probability_for_date):
                continue

            date = date_entry_row.to_datetime()
            probability = round(probability_for_date, 2)

            for capacity in capacity_list:
                if probability < 0.1 or probability > 0.99:
                    output_rows.append([-1, -1, date.strftime(date_format), department, capacity])
                else:
                    optimal_number, prob_range = data_interaction_module_aiims.retrieve_values(probability, capacity)
                    output_rows.append(
                        [optimal_number, prob_range, date.strftime(date_format), department, capacity, probability,
                         date.weekday() + 1, date.month])

    data_interaction_module_aiims.write_one_optimal_by_date_file(output_rows)
