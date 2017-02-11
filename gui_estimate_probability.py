#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import Tkinter

import data_interaction_module_aiims

SET_DEFAULT_PROB = 0.5
LABEL_BACKGROUND = "mediumseagreen"


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

        self.increment_row_and_add_field_label(u"Probability of patient show : ")
        self.pEntryVariable = Tkinter.StringVar()
        self.pEntry = Tkinter.Entry(self, textvariable=self.pEntryVariable)
        self.pEntry.grid(column=1, row=self.row_number, sticky='EW', padx=5, pady=8)
        self.pEntry.bind("<Return>", self.OnPressEnter)
        self.pEntryVariable.set(SET_DEFAULT_PROB)

        self.increment_row_and_add_field_label(u"Total Capacity : ")
        self.total_capacity_entry_variable = Tkinter.StringVar()
        self.total_capacity_entry = Tkinter.Entry(self, textvariable=self.total_capacity_entry_variable)
        self.total_capacity_entry.grid(column=1, row=self.row_number, sticky='W', padx=5, pady=8)
        self.total_capacity_entry.bind("<Return>", self.OnPressEnter)
        self.total_capacity_entry_variable.set(200)

        button = Tkinter.Button(self, text=u"Estimate Optimal Number of Bookings", command=self.OnCalculateEstimate)
        button.grid(column=0, row=self.increment_row_number())

        self.payoffVariable = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=self.payoffVariable, anchor="w", fg="black", bg="white")
        label.grid(column=0, row=self.increment_row_number(), columnspan=4, sticky='EW', padx=5, pady=8)
        self.payoffVariable.set("Calculated Pay Off : ")

        self.grid_columnconfigure(0, weight=1)
        self.resizable(True, False)
        self.update()
        self.geometry(self.geometry())
        self.configure(background="lavender")

        self.pEntry.focus_set()
        self.pEntry.selection_range(0, Tkinter.END)

    def increment_row_and_add_field_label(self, text, pady=8):
        label = Tkinter.Label(self, text=text, anchor="w", fg="white", bg=LABEL_BACKGROUND)
        label.grid(column=0, row=self.increment_row_number(), columnspan=1, sticky='EW', padx=5, pady=pady)

    def add_major_label(self, txt):
        headinglabel = Tkinter.Label(self, text=txt, anchor="center", fg="white", bg="lightseagreen")
        headinglabel.grid(column=0, row=self.increment_row_number(), sticky='EW', columnspan=4, padx=4, pady=16)

    def OnCalculateEstimate(self):
        try:
            probability = float(self.pEntryVariable.get())
            if probability > 1 or probability < 0:
                self.payoffVariable.set("Could Not Compute Optimal Payoff. Probability should between 0 and 1")
                self.pEntry.focus_set()
                self.pEntry.selection_range(0, Tkinter.END)
                return

            capacity = int(self.total_capacity_entry_variable.get())
            optimal_n, probability_range = data_interaction_module_aiims.retrieve_values(probability, capacity)
            if optimal_n is None:
                self.payoffVariable.set("Number of Bookings not previously calculated for given parameters")
            else:
                self.payoffVariable.set(
                    "Number of Bookings: " + str(optimal_n) + " with a Probability Range : " + str(probability_range))
        except Exception:
            self.payoffVariable.set("Could Not Compute Payoff. Please check parameter values.")
        self.pEntry.focus_set()
        self.pEntry.selection_range(0, Tkinter.END)

    def OnPressEnter(self, event):
        self.OnCalculateEstimate()

if __name__ == "__main__":
    app = mycolapp_tk(None)
    app.title("myCOL Scheduler")
    app.mainloop()
