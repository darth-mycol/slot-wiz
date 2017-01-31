import csv

import scipy.stats as ss

MAX_BOOKED = 10
MINIMUM_BOOKED = 0

MINIMUM_SHOW = 0

SLOT_PREFERENCE = 2

show_up_prob = 0.9

output_file = open('output.csv', 'w')
csv_file = csv.writer(output_file)

print "x,\ty,\tTotal"

max_total = 0
max_x = 0
max_y = 0

slot_x = 0
slot_y = 0

for x in range(MINIMUM_BOOKED, MAX_BOOKED + 1):
    x_distribution = ss.binom(x, show_up_prob)
    for y in range(MINIMUM_BOOKED, MAX_BOOKED - x + 1):
        y_distribution = ss.binom(y, show_up_prob)
        for z in range(MINIMUM_BOOKED, MAX_BOOKED - x - y + 1):
            z_distribution = ss.binom(y, show_up_prob)
            xy_total = 0

            for x_value in range(MINIMUM_BOOKED, x + 1):
                x_prob = x_distribution.pmf(x_value)
                x_wait = x_value - SLOT_PREFERENCE if x_value - SLOT_PREFERENCE > 0 else 0

                for y_value in range(MINIMUM_BOOKED, y + 1):
                    y_prob = y_distribution.pmf(y_value)
                    y_wait = y_value + x_wait - SLOT_PREFERENCE if y_value + x_wait - SLOT_PREFERENCE > 0 else 0

                    for z_value in range(MINIMUM_BOOKED, z + 1):
                        z_prob = z_distribution.pmf(z_value)
                        z_wait = z_value + y_wait - SLOT_PREFERENCE if z_value + y_wait - SLOT_PREFERENCE > 0 else 0

                        z_over = z_wait * (z_wait + 1) / 2

                        benefit = (x_value + y_value + z_value) - (x_wait + y_wait + z_over)

                        if x_value + y_value > SLOT_PREFERENCE * 2:
                            benefit -= (x_value + y_value - SLOT_PREFERENCE * 2) * (x_value + y_value - SLOT_PREFERENCE * 2)

                        xy_total += benefit * x_prob * y_prob

            csv_file.writerow([x, y, xy_total])
            # print x,y,xy_total
            if xy_total > max_total:
                max_y = y
                max_x = x
                max_total = xy_total

print max_x, max_y, max_total
output_file.close()
