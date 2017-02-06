#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter

import data_interaction_module
import payoff_calculator

SET_DEFAULT_PROB = 0.5

LABEL_BKGRND = "mediumseagreen"


class mycolapp_tk(Tkinter.Tk):
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.row_number = 0
        self.initialize()

    def increment_row_number(self):
        self.row_number += 1
        return self.row_number

    def initialize(self):
        self.grid()

        plabel = Tkinter.Label(self, text=u"Probability : ", anchor="w", fg="white", bg=LABEL_BKGRND)
        plabel.grid(column=0, row=self.row_number, columnspan=1, sticky='EW', padx=5, pady=8)
        self.pEntryVariable = Tkinter.StringVar()
        self.pEntry = Tkinter.Entry(self, textvariable=self.pEntryVariable)
        self.pEntry.grid(column=1, row=self.row_number, sticky='EW', padx=5, pady=8)
        self.pEntryVariable.set(SET_DEFAULT_PROB)

        ###################

        capacityLabel = Tkinter.Label(self, text=u"Capacity Per Slot : ", anchor="w", fg="white", bg=LABEL_BKGRND)
        capacityLabel.grid(column=0, row=self.increment_row_number(), columnspan=1, sticky='EW', padx=5, pady=8)
        self.capacityEntryVariable = Tkinter.StringVar()
        self.capacityEntry = Tkinter.Entry(self, textvariable=self.capacityEntryVariable)
        self.capacityEntry.grid(column=1, row=self.row_number, sticky='EW', padx=5, pady=8)
        self.capacityEntryVariable.set(5)

        ###################

        scheduleLabel = Tkinter.Label(self, text=u"Schedule : ", anchor="w", fg="white", bg=LABEL_BKGRND)
        scheduleLabel.grid(column=0, row=self.increment_row_number(), columnspan=1, sticky='EW', padx=5, pady=8)

        self.scheduleEntryVariable = Tkinter.StringVar()
        self.scheduleEntry = Tkinter.Entry(self, textvariable=self.scheduleEntryVariable)
        self.scheduleEntry.grid(column=1, row=self.row_number, sticky='E', padx=5, pady=8)
        self.scheduleEntryVariable.set(5)

        self.scheduleSecondEntryVariable = Tkinter.StringVar()
        self.scheduleSecondEntry = Tkinter.Entry(self, textvariable=self.scheduleSecondEntryVariable)
        self.scheduleSecondEntry.grid(column=2, row=self.row_number)
        self.scheduleSecondEntryVariable.set(5)

        self.scheduleThirdEntryVariable = Tkinter.StringVar()
        self.scheduleThirdEntry = Tkinter.Entry(self, textvariable=self.scheduleThirdEntryVariable)
        self.scheduleThirdEntry.grid(column=3, row=self.row_number, sticky='W', padx=5, pady=8)
        self.scheduleThirdEntryVariable.set(5)

        ###################

        button = Tkinter.Button(self, text=u"Compute Payoff", command=self.OnComputePayoffClick)
        button.grid(column=0, row=self.increment_row_number())

        self.payoffVariable = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=self.payoffVariable, anchor="w", fg="white", bg=LABEL_BKGRND)

        label.grid(column=0, row=self.increment_row_number(), columnspan=2, sticky='EW', padx=5, pady=8)

        total_capacity_label = Tkinter.Label(self, text=u"Total Capacity : ", anchor="w", fg="white", bg=LABEL_BKGRND)
        total_capacity_label.grid(column=0, row=self.increment_row_number(), columnspan=1, sticky='EW', padx=5, pady=8)

        self.total_capacity_entry_variable = Tkinter.StringVar()
        self.total_capacity_entry = Tkinter.Entry(self, textvariable=self.total_capacity_entry_variable)
        self.total_capacity_entry.grid(column=1, row=self.row_number, sticky='W', padx=5, pady=8)
        self.total_capacity_entry_variable.set(201)

        lookup_button = Tkinter.Button(self, text=u"Total Capacity Solution", command=self.OnPressEnter)
        lookup_button.grid(column=0, row=self.increment_row_number())

        self.optimalVariable = Tkinter.StringVar()
        lookup_label = Tkinter.Label(self, textvariable=self.optimalVariable,
                                     anchor="w", fg="white", bg=LABEL_BKGRND)

        lookup_label.grid(column=0, row=self.increment_row_number(), columnspan=4, sticky='EW', padx=5, pady=8)

        self.grid_columnconfigure(0, weight=1)
        self.resizable(True, False)
        self.update()
        self.geometry(self.geometry())
        self.configure(background="lavender")
        self.pEntry.focus_set()
        self.pEntry.selection_range(0, Tkinter.END)

    def OnComputePayoffClick(self):
        try:
            schedule = [int(self.scheduleEntryVariable.get()), int(self.scheduleSecondEntryVariable.get()),
                        int(self.scheduleThirdEntryVariable.get())]
            payoff = payoff_calculator.estimate_payoff(schedule, float(self.pEntryVariable.get()),
                                                       int(self.capacityEntryVariable.get()))
            self.payoffVariable.set("Calculated Pay Off : " + str(payoff))
            self.pEntry.focus_set()
            self.pEntry.selection_range(0, Tkinter.END)
        except Exception:
            self.payoffVariable.set("Could Not Compute Payoff. Please check parameter values.")

    def OnPressEnter(self):
        try:
            schedule, payoff = data_interaction_module.look_up_dictionary(float(self.pEntryVariable.get()), 3,
                                                                          int(self.total_capacity_entry_variable.get()))
            self.optimalVariable.set("Calculated Pay Off : " + str(payoff) + " and optimal schedule : " + str(schedule))
            self.pEntry.focus_set()
            self.pEntry.selection_range(0, Tkinter.END)
        except Exception:
            self.optimalVariable.set("Could Not Compute Optimal Payoff. Please check parameter values.")


if __name__ == "__main__":
    app = mycolapp_tk(None)
    app.title("myCOL Scheduler")
    app.mainloop()
