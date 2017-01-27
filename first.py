import scipy.stats as ss
from matplotlib import pyplot as plt

AVAILABLE_SLOTS = 2

MAX_BOOKED = 4
MINIMUM_BOOKED = 1

MINIMUM_SHOW = 0



p = 0.5

def calculate_cost(probability, show_up, booked):
	#print booked, show_up, probability
	if (show_up < AVAILABLE_SLOTS):
		return show_up * probability
	cost = (show_up - (show_up - AVAILABLE_SLOTS) * (show_up - AVAILABLE_SLOTS))
	return cost * probability 
		
	
expected_cost = 0
optimal_N = 0
print "booked,\tshow_up,probability,cost"


for booked in range(MINIMUM_BOOKED, MAX_BOOKED + 1): 
	distribution = ss.binom(booked, p)
	booked_cost = 0
	for show_up in range(MINIMUM_SHOW, booked + 1):
		#print booked, show_up
		prob = distribution.pmf(show_up)
		cost = calculate_cost(prob, show_up, booked)
		#print booked, "\t", show_up, "\t", prob, "\t", cost
		booked_cost += cost
		#print booked_cost
	
	#print "booked, booked_cost" , booked, booked_cost, "\n"
	
	if booked_cost > expected_cost:
		expected_cost = booked_cost
		optimal_N = booked


print "\nmax_cost", expected_cost, "\n"
print "\nOptimal", optimal_N, "\n"

    	
