import pandas as pd
from matplotlib import pyplot as plt


def main_method():
    df = pd.read_csv("Aggregated-csv/ONE_SLOT_BOOKING_PER_SLOT_201_DISTRIBUTED_CYCLIC_FRONT_LOADING.csv")
    df_second_file = pd.read_csv("Aggregated-csv/CAPACITY_201_SLOTS_3PER_SLOT_67_NUMBER_OF_SLOTS_3.csv")

    first = list(df["Distributed Payoff"][:])
    second = list(df_second_file["PAYOFF"][:])

    diff = []
    for term, second_term in zip(first, second):
        diff.append(second_term - term)

    probability_list = []
    for prob in range(40, 71, 5):
        probability_list.append(float(prob) / 100)
    for prob in range(80, 96, 5):
        probability_list.append(float(prob) / 100)
    probability_list.append(0.99)

    plt.plot(probability_list, diff)
    plt.show()


if __name__ == "__main__":
    main_method()
