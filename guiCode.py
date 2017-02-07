#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import Tkinter

import data_interaction_module
import payoff_calculator

ALLOWED_OVER_TIME_POWER = [1.0, 1.5, 2.0]

ALLOWED_OVER_TIME_VALUES = [1.0, 1.5]

ALLOWED_WAIT_TIME_VALUES = [0.0, 0.5, 1.0, 1.5]

SET_DEFAULT_PROB = 0.55
NUMBER_OF_SLOTS = 3

LABEL_BKGRND = "mediumseagreen"


class mycolapp_tk(Tkinter.Tk):
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.row_number = -1
        self.initialize()

    def increment_row_number(self):
        self.row_number += 1
        return self.row_number

    def initialize(self):
        self.grid()

        self.add_major_label(u"AIIMS Scheduler")
        self.add_major_label(u"Universal Variables")

        ##################

        self.increment_row_and_add_field_label(u"Probability of patient show : ")
        self.pEntryVariable = Tkinter.StringVar()
        self.pEntry = Tkinter.Entry(self, textvariable=self.pEntryVariable)
        self.pEntry.grid(column=1, row=self.row_number, sticky='EW', padx=5, pady=8)
        self.pEntryVariable.set(SET_DEFAULT_PROB)

        ###################

        self.increment_row_and_add_field_label(u"Wait Time Cost : ")

        self.wait_time_constant_variable = Tkinter.StringVar()
        self.wait_time_constant_entry = Tkinter.Entry(self, textvariable=self.wait_time_constant_variable)
        self.wait_time_constant_entry.grid(column=1, row=self.row_number, sticky='EW', padx=5, pady=8)
        self.wait_time_constant_variable.set(1)

        ####################
        self.increment_row_and_add_field_label(u"Over Time Cost : ")
        self.over_time_constant_variable = Tkinter.StringVar()
        self.over_time_constant_entry = Tkinter.Entry(self, textvariable=self.over_time_constant_variable)
        self.over_time_constant_entry.grid(column=1, row=self.row_number, sticky='EW', padx=5, pady=8)
        self.over_time_constant_variable.set(1)

        ###################
        self.increment_row_and_add_field_label(u"Impact of Over Time : ")
        self.over_time_power_variable = Tkinter.StringVar()
        self.over_time_power_entry = Tkinter.Entry(self, textvariable=self.over_time_power_variable)
        self.over_time_power_entry.grid(column=1, row=self.row_number, sticky='EW', padx=5, pady=8)
        self.over_time_power_variable.set(2)

        ###################

        self.increment_row_and_add_field_label(u"Number of Slots : ", 1)

        self.radioVariable = Tkinter.IntVar()
        self.radioVariable.set(3)
        MODES = [
            ("One", 1),
            ("Two", 2),
            ("Three", 3)
        ]
        for txt, num in MODES:
            if num != 1: self.increment_row_number()
            b = Tkinter.Radiobutton(self, text=txt, variable=self.radioVariable, value=num, foreground="white",
                                    bg=LABEL_BKGRND, indicatoron=False)
            b.grid(column=1, row=self.row_number, sticky='EW', padx=5, pady=1)

        ###################

        self.add_major_label(u"User Generated Solution Variables")

        self.increment_row_number()
        self.add_column_label("Hour1", column=1)
        self.add_column_label("Hour2", column=2)
        self.add_column_label("Hour3", column=3)

        self.increment_row_and_add_field_label(u"Capacity Per Hour Per Slot : ")

        self.capacityFirstEntryVariable = Tkinter.StringVar()
        self.capacityFirstEntry = Tkinter.Entry(self, textvariable=self.capacityFirstEntryVariable)
        self.capacityFirstEntry.grid(column=1, row=self.row_number, sticky='E', padx=5, pady=8)
        self.capacityFirstEntryVariable.set(67)

        self.capacitySecondEntryVariable = Tkinter.StringVar()
        self.capacitySecondEntry = Tkinter.Entry(self, textvariable=self.capacitySecondEntryVariable)
        self.capacitySecondEntry.grid(column=2, row=self.row_number)
        self.capacitySecondEntryVariable.set(67)

        self.capacityThirdEntryVariable = Tkinter.StringVar()
        self.capacityThirdEntry = Tkinter.Entry(self, textvariable=self.capacityThirdEntryVariable)
        self.capacityThirdEntry.grid(column=3, row=self.row_number, sticky='W', padx=5, pady=8)
        self.capacityThirdEntryVariable.set(66)

        ###################

        self.increment_row_and_add_field_label(u"Patient Booking per hour : ")

        self.scheduleEntryVariable = Tkinter.StringVar()
        self.scheduleEntry = Tkinter.Entry(self, textvariable=self.scheduleEntryVariable)
        self.scheduleEntry.grid(column=1, row=self.row_number, sticky='E', padx=5, pady=8)
        self.scheduleEntryVariable.set(129)

        self.scheduleSecondEntryVariable = Tkinter.StringVar()
        self.scheduleSecondEntry = Tkinter.Entry(self, textvariable=self.scheduleSecondEntryVariable)
        self.scheduleSecondEntry.grid(column=2, row=self.row_number)
        self.scheduleSecondEntryVariable.set(125)

        self.scheduleThirdEntryVariable = Tkinter.StringVar()
        self.scheduleThirdEntry = Tkinter.Entry(self, textvariable=self.scheduleThirdEntryVariable)
        self.scheduleThirdEntry.grid(column=3, row=self.row_number, sticky='W', padx=5, pady=8)
        self.scheduleThirdEntryVariable.set(116)

        ###################

        button = Tkinter.Button(self, text=u"Calculate Payoff", command=self.OnComputePayoffClick)
        button.grid(column=0, row=self.increment_row_number())

        self.payoffVariable = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=self.payoffVariable, anchor="w", fg="black", bg="white")
        label.grid(column=0, row=self.increment_row_number(), columnspan=4, sticky='EW', padx=5, pady=8)
        self.payoffVariable.set("Calculated Pay Off : ")

        ####################
        self.add_major_label(u"System Generated Solution Variables")

        self.increment_row_and_add_field_label(u"Total Capacity : ")

        self.total_capacity_entry_variable = Tkinter.StringVar()
        self.total_capacity_entry = Tkinter.Entry(self, textvariable=self.total_capacity_entry_variable)
        self.total_capacity_entry.grid(column=1, row=self.row_number, sticky='W', padx=5, pady=8)
        self.total_capacity_entry_variable.set(200)

        lookup_button = Tkinter.Button(self, text=u"Optimal Solution", command=self.OnPressOptimalSolution)
        lookup_button.grid(column=0, row=self.increment_row_number())

        self.optimalVariable = Tkinter.StringVar()
        lookup_label = Tkinter.Label(self, textvariable=self.optimalVariable,
                                     anchor="w", fg="black", bg="white")

        lookup_label.grid(column=0, row=self.increment_row_number(), columnspan=4, sticky='EW', padx=5, pady=8)
        self.optimalVariable.set("Calculated Pay Off : ")

        self.grid_columnconfigure(0, weight=1)
        self.resizable(True, False)
        self.update()
        self.geometry(self.geometry())
        self.configure(background="lavender")
        self.pEntry.focus_set()
        self.pEntry.selection_range(0, Tkinter.END)

    def increment_row_and_add_field_label(self, text, pady=8):
        label = Tkinter.Label(self, text=text, anchor="w", fg="white", bg=LABEL_BKGRND)
        label.grid(column=0, row=self.increment_row_number(), columnspan=1, sticky='EW', padx=5, pady=pady)

    def add_major_label(self, txt):
        headinglabel = Tkinter.Label(self, text=txt, anchor="center", fg="white", bg="lightseagreen")
        headinglabel.grid(column=0, row=self.increment_row_number(), sticky='EW', columnspan=4, padx=4, pady=16)

    def add_column_label(self, txt, column):
        headinglabel = Tkinter.Label(self, text=txt, anchor="w", fg="grey", bg="lavender")
        headinglabel.grid(column=column, row=self.row_number, sticky='EW', columnspan=4, padx=4, pady=0)

    def get_schedule_capacity(self):
        if self.radioVariable.get() == 3:
            schedule = [int(self.scheduleEntryVariable.get()), int(self.scheduleSecondEntryVariable.get()),
                        int(self.scheduleThirdEntryVariable.get())]
            per_slot_processing_list = [int(self.capacityFirstEntryVariable.get()),
                                        int(self.capacitySecondEntryVariable.get()),
                                        int(self.capacityThirdEntryVariable.get())]
        elif self.radioVariable.get() == 2:
            schedule = [int(self.scheduleEntryVariable.get()), int(self.scheduleSecondEntryVariable.get())]
            per_slot_processing_list = [int(self.capacityFirstEntryVariable.get()),
                                        int(self.capacitySecondEntryVariable.get())]
        elif self.radioVariable.get() == 1:
            schedule = [int(self.scheduleEntryVariable.get())]
            per_slot_processing_list = [int(self.capacityFirstEntryVariable.get())]
        else:
            raise Exception("Radio Button Option Not Supported")
        for capacity in per_slot_processing_list:
            if capacity < 1:
                raise Exception("Capacity per slot should be greater than 0")
        return per_slot_processing_list, schedule

    def OnComputePayoffClick(self):
        try:
            probability = float(self.pEntryVariable.get())
            if probability > 1 or probability < 0:
                self.payoffVariable.set("Could Not Compute Optimal Payoff. Probability should between 0 and 1")
                self.pEntry.focus_set()
                self.pEntry.selection_range(0, Tkinter.END)
                return

            wait_time_constant = float(self.wait_time_constant_variable.get())
            over_time_constant = float(self.over_time_constant_variable.get())
            over_time_power = float(self.over_time_power_variable.get())
            per_slot_processing_list, schedule = self.get_schedule_capacity()
            payoff = payoff_calculator.estimate_payoff(schedule, probability,
                                                       per_slot_processing_list, wait_time_constant,
                                                       over_time_constant, over_time_power)
            self.payoffVariable.set("Calculated Pay Off : " + str(payoff))
        except Exception:
            self.payoffVariable.set("Could Not Compute Payoff. Please check parameter values.")
        self.pEntry.focus_set()
        self.pEntry.selection_range(0, Tkinter.END)

    def OnPressOptimalSolution(self):
        try:
            wait_time_constant = float(self.wait_time_constant_variable.get())
            over_time_constant = float(self.over_time_constant_variable.get())
            over_time_power = float(self.over_time_power_variable.get())
            probability = float(self.pEntryVariable.get())
        except Exception:
            self.optimalVariable.set("Could Not Compute Optimal Payoff. Please check parameter values.")
            return

        if wait_time_constant not in ALLOWED_WAIT_TIME_VALUES:
            self.optimalVariable.set(
                "Could Not Compute Optimal Payoff. Wait Time cost can only be " + str(ALLOWED_WAIT_TIME_VALUES))
            self.wait_time_constant_entry.focus_set()
            self.wait_time_constant_entry.selection_range(0, Tkinter.END)
            return

        if over_time_constant not in ALLOWED_OVER_TIME_VALUES:
            self.optimalVariable.set(
                "Could Not Compute Optimal Payoff. Over Time cost can only be " + str(ALLOWED_OVER_TIME_VALUES))
            self.over_time_constant_entry.focus_set()
            self.over_time_constant_entry.selection_range(0, Tkinter.END)
            return

        if over_time_power not in ALLOWED_OVER_TIME_POWER:
            self.optimalVariable.set(
                "Could Not Compute Optimal Payoff. Over Time Impact can only be " + str(ALLOWED_OVER_TIME_POWER))
            self.over_time_constant_entry.focus_set()
            self.over_time_constant_entry.selection_range(0, Tkinter.END)
            return

        if probability > 1 or probability < 0:
            self.optimalVariable.set("Could Not Compute Optimal Payoff. Probability should between 0 and 1")
            self.pEntry.focus_set()
            self.pEntry.selection_range(0, Tkinter.END)
            return

        try:
            schedule, payoff = data_interaction_module.look_up_dictionary(probability,
                                                                          self.radioVariable.get(),
                                                                          int(self.total_capacity_entry_variable.get()),
                                                                          over_time_constant, wait_time_constant,
                                                                          over_time_power)
            self.optimalVariable.set("Calculated Pay Off : " + str(payoff) + " and optimal schedule : " + str(schedule))
        except Exception:
            self.optimalVariable.set("Could Not Compute Optimal Payoff. Please check parameter values.")
        self.total_capacity_entry.focus_set()
        self.total_capacity_entry.selection_range(0, Tkinter.END)


if __name__ == "__main__":
    app = mycolapp_tk(None)
    app.title("myCOL Scheduler")
    app.mainloop()
