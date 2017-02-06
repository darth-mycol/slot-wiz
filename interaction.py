import cmd
import time

import data_interaction_module
import entry_optimal_schedule_calculator
import payoff_calculator

# noinspection PyUnusedLocal
class Interface(cmd.Cmd):
    intro = "Welcome to the Scheduling shell. Type help or ? to list commands.\n"
    prompt = "myCOLScheduler>>> "
    time_counter = 0

    def __init__(self):
        cmd.Cmd.__init__(self, completekey='\t')
        self.initialize_default_parameters()

    def initialize_default_parameters(self):
        self.schedule = [10, 10, 10]
        self.p = 0.5
        self.capacity = 5
        self.wait_time_constant = 1
        self.over_time_constant = 1
        self.over_time_power = 2
        self.total_capacity = 201
        self.number_of_slots = 3

    def do_reset(self, arg):
        self.initialize_default_parameters()
        self.do_print_parameters(self)

    def print_time_taken(self):
        print "\nTime Taken :", time.time() - self.time_counter, "seconds\n"

    def do_reinitialize_data(self, arg):
        data_interaction_module.initialize()

    def do_print_parameters(self, arg):
        print "\nPresent Parameters : \n"
        print "Universal : "
        print "p : ", self.p
        print "capacity : ", self.capacity
        print "wait_time_constant : ", self.wait_time_constant
        print "over_time_constant : ", self.over_time_constant
        print "over_time_power : ", self.over_time_power
        print "number_of_slots : ", self.number_of_slots

        print "\nPayOff Calculation : "
        print "schedule : ", self.schedule

        print "\nLookup Parameters : "
        print "total_capacity : ", self.total_capacity

    def do_lookup(self, arg):
        schedule, payoff = data_interaction_module.look_up_dictionary(self.p, self.number_of_slots, self.total_capacity,
                                                                      self.over_time_constant, self.wait_time_constant,
                                                                      self.over_time_power)
        if schedule is not None:
            print "Optimal Number of Bookings : ", sum(schedule)
            print "Optimal Distribution : ", schedule
            print "Calculated Pay Off : ", payoff
            self.print_time_taken()

    def do_calculate_payoff(self, arg):
        'Calculate Payoff using present Parameter Configuration'
        payoff = payoff_calculator.estimate_payoff(self.schedule, self.p, [self.capacity, self.capacity, self.capacity],
                                                   self.wait_time_constant,
                                                   self.over_time_constant, self.over_time_power)
        print "Calculated Pay Off : ", payoff
        self.print_time_taken()

    def do_calculate_optimal_schedule(self, arg):
        entry_optimal_schedule_calculator.compute_optimal_schedule([(self.wait_time_constant, self.over_time_constant)],
                                                                   self.number_of_slots, [self.over_time_power],
                                                                   [self.capacity, self.capacity, self.capacity], [self.p])
        self.do_reinitialize_data(self)
        self.print_time_taken()

    def do_bye(self, arg):
        print('Thanks for using Slot_Scheduler. See you next time!')
        return True

    # Set Parameters
    def do_number_of_slots(self, arg):
        try:
            self.number_of_slots = int(arg)
        except:
            print "ERR: Value for number_of_slots should be of type int"

    def do_wait_time_constant(self, arg):
        try:
            self.wait_time_constant = float(arg)
        except:
            print "ERR: Value for wait_time_constant should be of type float"

    def do_over_time_constant(self, arg):
        try:
            self.over_time_constant = float(arg)
        except:
            print "ERR: Value for over_time_constant should be of type float"

    def do_over_time_power(self, arg):
        try:
            self.over_time_power = float(arg)
        except:
            print "ERR: Value for over_time_power should be of type float"

    def do_capacity(self, arg):
        try:
            self.capacity = int(arg)
        except:
            print "ERR: Value for capacity should be of type int"

    def do_p(self, arg):
        try:
            self.p = float(arg)
        except:
            print "ERR: Value for p should be of type float"

    def do_schedule(self, arg):
        try:
            schedule = []
            for term in arg.split(","):
                schedule.append(int(term.strip()))
            self.schedule = schedule
        except:
            print "ERR: Value for schedule should be a comma separated integer values"

    def do_total_capacity(self, arg):
        try:
            self.total_capacity = int(arg)
        except:
            print "ERR: Value for total_capacity should be of type int"

    # Set Parameters Interactively
    def do_set_parameters(self, arg):
        self.do_number_of_slots(raw_input("Enter Value for number_of_slots : "))
        self.do_wait_time_constant(raw_input("Enter Value for wait_time_constant : "))
        self.do_over_time_constant(raw_input("Enter Value for over_time_constant : "))
        self.do_over_time_power(raw_input("Enter Value for over_time_power : "))
        self.do_capacity(raw_input("Enter Value for capacity : "))
        self.do_p(raw_input("Enter Value for p : "))
        self.do_schedule(raw_input("Enter Value for schedule : "))

        self.do_print_parameters(self)

    # Book Keeping Tasks
    def precmd(self, line):
        self.time_counter = time.time()
        return line


if __name__ == "__main__":
    Interface().cmdloop()
