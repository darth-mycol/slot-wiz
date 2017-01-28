import scipy.stats as ss
import time
from matplotlib import pyplot as plt

PER_SLOT_PROCESSING = 200
MAX_BOOKED = 2000
MINIMUM_BOOKED = 1
MINIMUM_SHOW = 0

def calculate_cost(probability, show_up, booked):
	if (show_up < PER_SLOT_PROCESSING):
		return show_up * probability
	cost = (show_up - (show_up - PER_SLOT_PROCESSING) * (show_up - PER_SLOT_PROCESSING))
	return cost * probability
		

def get_optimal_cost(event_prob):
	expected_cost = 0
	optimal_N = 0
	

	for booked in range(MINIMUM_BOOKED, MAX_BOOKED + 1): 
		distribution = ss.binom(booked, event_prob)
		booked_cost = 0
		for show_up in range(MINIMUM_SHOW, booked + 1):
			prob = distribution.pmf(show_up)
			cost = calculate_cost(prob, show_up, booked)
			#print booked, "\t", show_up, "\t", prob, "\t", cost
			booked_cost += cost
		
		if booked_cost > expected_cost:
			expected_cost = booked_cost
			optimal_N = booked
	return expected_cost, optimal_N

print "\nprob, optimal_N, expected_cost, time"

p_unit  = 0.1
prob_range = []

for count in range(1,10):
	event_prob = count * p_unit
	
	event_calculation_start_time = time.time()
	expected_cost, optimal_N = get_optimal_cost(event_prob)
	print event_prob, "\t", optimal_N, "\t", expected_cost, time.time() - event_calculation_start_time, "\n"
