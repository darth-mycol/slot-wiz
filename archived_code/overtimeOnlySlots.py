import csv

import scipy.stats as ss

####DELETE this if unused

MAX_BOOKED = 218
MINIMUM_BOOKED = 100

MINIMUM_SHOW = 0

SLOT_PREFERENCE = 100

show_up_prob = 0.9

output_file = open('output_slots.csv', 'w')
csv_file = csv.writer(output_file)

print "x,\ty,\tTotal"

max_total = 0
max_x = 0
max_y = 0

slot_x = 0
slot_y = 0

previous_best_xy = 0


def generate_variations(x, y):
    if x == 1 or y ==1:
        return None
    else:
        return [[x-1,y], [x+1,y], [x,y-1], [x,y+1]]


while (True):
    x = 900
    y = 900

    list1 = generate_variations(x, y)
    if list1 == None:
        break
    for pair in list1:
        x = pair[0]
        y = pair[2]


        x_distribution = ss.binom(x, show_up_prob)
        y_distribution = ss.binom(y, show_up_prob)
        xy_total = 0

        for x_value in range(MINIMUM_SHOW, x + 1):
            x_prob = x_distribution.pmf(x_value)

            x_wait = x_value - SLOT_PREFERENCE if x_value - SLOT_PREFERENCE > 0 else 0
            # x_gain = SLOT_PREFERENCE if x_value >= SLOT_PREFERENCE else x_value

            for y_value in range(MINIMUM_SHOW, y + 1):
                y_prob = y_distribution.pmf(y_value)
                # y_gain = 1 if y_value + x_wait !=0 else 0

                # y_wait = y_value + x_wait - SLOT_PREFERENCE if y_value + x_wait - SLOT_PREFERENCE > 0 else 0
                # y_over = y_wait * (y_wait + 1) / 2

                benefit = (x_value + y_value)

                if x_wait + y_value > SLOT_PREFERENCE:
                    benefit -= (x_wait + y_value - SLOT_PREFERENCE) * (x_wait + y_value - SLOT_PREFERENCE)

                xy_total += benefit * x_prob * y_prob

        csv_file.writerow([x, y, xy_total])
        # print x,y,xy_total
        if xy_total > max_total:
            max_y = y
            max_x = x
            max_total = xy_total

        if xy_total < 0: #HEURISTIC, leave all further y's
            break

    if previous_best_xy > max_total and max_total != 0:
        break
    else:
        previous_best_xy = max_total

print max_x, max_y, max_total
output_file.close()
