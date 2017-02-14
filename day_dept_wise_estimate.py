import math
from datetime import date, timedelta

import data_interaction_module_aiims

date_format = "%d/%m/%Y"


def generate_day_wise_data():
    zero_constant = -0.0015858
    alpha = 0.3232916
    beta = {1: 0, 2: -0.0778308, 3: -0.0699497, 4: -0.0807388, 5: 0.026566, 6: -0.1063554, 7: 0}
    gamma = {1: 0, 2: -0.070373, 3: -0.2453557, 4: -0.2433087, 5: -0.2703052, 6: -0.3415253, 7: -0.3818892,
             8: -0.3360227, 9: -0.408951, 10: -0.4120214, 11: -0.3554762, 12: -0.0406669}

    start_date = date(year=2016, month=12, day=15)
    end_date = date(year=2017, month=3, day=31)

    date_time_prob_dict = {start_date: -.11}

    date_loop_variable = start_date
    while date_loop_variable <= end_date:
        previous_date = date_loop_variable
        date_loop_variable += timedelta(days=1)

        # Account for the activity being zero on the Sunday
        day_of_week = date_loop_variable.weekday() + 1
        if day_of_week == 7:
            continue
        if day_of_week == 1:
            previous_date -= timedelta(days=1)

        previous_prob = date_time_prob_dict[previous_date]
        if previous_prob is None:
            raise Exception(
                "Flow Broken, probability for date not generated. Date : " + previous_date.strftime(date_format))

        probability = zero_constant + alpha * previous_prob + beta[day_of_week] * day_of_week + \
                      gamma[date_loop_variable.month] * date_loop_variable.month

        date_time_prob_dict[date_loop_variable] = probability

    return date_time_prob_dict


def get_capacity_list():
    return [100,135,150,200]


if __name__ == "__main__":
    department = 1
    final_date_time_prob_dict = generate_day_wise_data()
    capacity_list = get_capacity_list()
    for capacity in capacity_list:
        output_rows = [
            ["optimalnumber", "probabilityrange", "date", "department", "capacity", "probability", "day", "month"]]

        for item in final_date_time_prob_dict.items():
            date = item[0]
            probability_ratio = item[1]
            e_val = math.exp(float(probability_ratio))
            probability = round(e_val / (1 + e_val), 2)

            if probability < 0.1 or probability > 0.99:
                output_rows.append([-1, -1, date.strftime(date_format), department, capacity])
            else:
                optimal_number, prob_range = data_interaction_module_aiims.retrieve_values(probability, capacity)
                output_rows.append(
                    [optimal_number, prob_range, date.strftime(date_format), department, capacity, probability,
                     date.weekday() + 1, date.month])

        data_interaction_module_aiims.write_one_optimal_by_date_file(output_rows, capacity)
