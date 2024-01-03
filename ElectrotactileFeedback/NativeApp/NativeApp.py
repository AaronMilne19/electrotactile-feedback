﻿from datetime import datetime
import itertools
from tkinter import *
from tkinter import ttk
import uuid
import tkdial as tkd
import random
from FESService import FESService

class NativeApp:

    dev = FESService()
    def __init__(self, user_id:str, descriptor:str=None, title="Electrotactile Feedback", geometry="600x400", result_dir="results"):
        self.dev.reset_settings()
        self.user_id = user_id
        self.descriptor = descriptor
        self.r = -1
        self.window = Tk()
        self.window.geometry(geometry)
        self.window.title(title)
        self.result_dir = result_dir

    #Title
    def add_title(self, title:str):
        self.r += 1
        ttk.Label(master=self.window, text=title, font=("Arial", 25)).grid(columnspan=2, row=self.r, padx=10, pady=20, sticky="n")

    #Button
    def add_button_widget(self):
        self.r += 1
        ttk.Label(master=self.window, text="Try clicking this button:").grid(column=0, row=self.r, padx=10, sticky="e")
        button = Button(master=self.window, text="Click me!", width=25, command=self.dev.send_pulse)
        button.bind("<Button-1>", lambda e: self.dev.send_pulse())
        button.grid(column=1, row=self.r, sticky="w", padx=10)

    #Text input
    def add_text_widget(self):
        self.r += 1
        ttk.Label(master=self.window, text="Enter some text:").grid(column=0, row=self.r, padx=10, sticky="e")
        text = ttk.Entry(master=self.window, width=25)
        text.bind("<Key>", lambda e: self.dev.send_pulse())
        text.grid(column=1, row=self.r, sticky="w", padx=10)

    #Multi select checkboxes
    #Needs to return the list of v otherwise black box is shown by default on the window
    def add_multi_selection_widget(self):
        self.r += 1
        Label(text="Select multiple options:").grid(column=0, row=self.r, padx=10, sticky="e")
        multi_select_frame = Frame(self.window)
        multi_select_frame.grid(column=1, row=self.r, sticky="w", padx=10)
        v = []
        for i in range(1,6):
            v.append(BooleanVar(value=False))
            button = ttk.Checkbutton(text=i, master=multi_select_frame, variable=v[i-1], command=self.dev.send_pulse)
            button.bind("<Button-1>", lambda e: self.dev.send_pulse())
            button.grid(row=0, column=i-1, sticky="w")
        return v

    #Radio buttons
    def add_radio_widget(self):
        self.r += 1
        Label(text="Select a radio button:").grid(column=0, row=self.r, padx=10, sticky="e")
        radio_select_frame = Frame(self.window)
        radio_select_frame.grid(column=1, row=self.r, sticky="w", padx=10)
        radio_var = IntVar()
        for i in range(1,6):
            button = ttk.Radiobutton(text=i, value=i, master=radio_select_frame, variable=radio_var, command=self.dev.send_pulse)
            button.bind("<Button-1>", lambda e: self.dev.send_pulse())
            button.grid(row=0, column=i-1, sticky="w")

    #Device parameter dials
    def add_parameter_dials(self, pw_val=0, fq_val=0, amp_val=0):
        self.r += 1
        dial_frame = Frame(self.window)
        dial_frame.grid(columnspan=2, row=self.r, padx=10, pady=20)
        self.pulsewidth_dial = tkd.Dial(master=dial_frame, text="Pulsewidth (μs):\n ", radius=35, scroll_steps=10, integer=True,
                        color_gradient=("gray", "gray"), unit_length=7, unit_width=7, height=150, width=100, end=200,
                        command=lambda: self.dev.set_pulsewidth(self.pulsewidth_dial.get()))
        self.frequency_dial = tkd.Dial(master=dial_frame, text="Frequency (PPS):\n ", radius=35, scroll_steps=5, integer=True,
                        color_gradient=("gray", "gray"), unit_length=7, unit_width=7, height=150, width=100, end=99,
                        command=lambda: self.dev.set_frequency(self.frequency_dial.get()))
        self.amplitude_dial = tkd.Dial(master=dial_frame, text="Amplitude (mA):\n ", radius=35, scroll_steps=1, integer=True,
                        color_gradient=("gray", "gray"), unit_length=7, unit_width=7, height=150, width=100, end=20,
                        command=lambda: self.dev.set_amplitude(self.amplitude_dial.get()))
        self.pulsewidth_dial.set(pw_val)
        self.frequency_dial.set(fq_val)
        self.amplitude_dial.set(amp_val)
        self.pulsewidth_dial.grid(row=0, column=0, padx=10)
        self.frequency_dial.grid(row=0, column=1, padx=10)
        self.amplitude_dial.grid(row=0, column=2, padx=10)

    #for phase 2, have pre-defined presets and let users choose the most comforatble one
    def add_preset_buttons(self, presets):
        self.r += 1
        preset_frame = Frame(self.window)
        preset_frame.grid(columnspan=2, row=self.r, padx=10, pady=20)
        preset_var = StringVar()
        preset_var.set(f"{presets[0][0]} {presets[0][1]} {presets[0][2]}")
        self.set_preset(preset_var)
        for i, preset in enumerate(presets):
            ttk.Radiobutton(text=f"Preset {i+1}", value=preset, master=preset_frame, variable=preset_var, command=lambda:self.set_preset(preset_var)).grid(row=0, column=i, sticky="w")
    
    def set_preset(self, preset_var:StringVar):
        pw, fq, amp = preset_var.get().split()
        self.dev.set_pulsewidth(int(pw))
        self.dev.set_frequency(int(fq))
        self.dev.set_amplitude(int(amp))

    #continue button which will save the results to a text file.
    def add_save_button(self):
        self.r +=1
        Button(master=self.window, text="Save results", command=self.save_results_exit).grid(columnspan=2, row=self.r, sticky="s", pady=20)

    #Save params to output csv file (pulsewidth,frequency,amplitude)
    def save_results_exit(self):
        if self.user_id != None:
            with open(f"{self.result_dir}/{self.user_id}_{self.descriptor}.csv", "a") as f:
                f.write(f"{self.dev.get_pulsewidth()},{self.dev.get_frequency()},{self.dev.get_amplitude()}\n")
        self.window.destroy()

    #Configure window scaling and run the app
    def run(self):
        self.window.rowconfigure(list(range(self.r+1)), weight=0, minsize=50)
        self.window.columnconfigure(list(range(2)), weight=1, minsize=50)
        self.window.mainloop()


####################

def add_required_widgets(app:NativeApp, widget:str):
    if widget == "button":
        app.add_button_widget()
    elif widget == "text":
        app.add_text_widget()
    elif widget == "radio":
        app.add_radio_widget()
    elif widget == "multi":
        v = app.add_multi_selection_widget()
        return v
    else:
        app.add_button_widget()
        app.add_text_widget()
        app.add_radio_widget()
        v = app.add_multi_selection_widget()
        return v

def run(phase=1):
    user_id = uuid.uuid4()
    print(user_id)
    widgets = ["button", "text", "radio", "multi"]
    presets = None

    #Create one version of the app which does not save any response - use this as a demonstation
    test_app = NativeApp(None)
    test_app.add_title("Demonstation Window")
    test_app.add_button_widget()
    if phase == 1:
        presets = [(150,70,8),(50,50,15),(100,20,20)] #Phase 1 presets (for seeding the dials)
        test_app.add_parameter_dials()
    elif phase == 2:
        #Phase 2 presets based on analysis of phase 1 responses. These are fixed presets
        presets = [(150,70,8),(50,50,15),(100,50,13)] 
        test_app.add_preset_buttons(presets)
    test_app.add_save_button()
    test_app.run()

    if phase == 1:
        combinations = list(itertools.product(widgets, presets))
        random.shuffle(combinations)
        for widget, params in combinations:
            app = NativeApp(user_id, widget)
            app.add_title("Electrotactile Feedback!")
            v = add_required_widgets(app, widget)
            app.add_parameter_dials(*params)
            app.add_save_button()
            app.run()

        #Save the user id to the file to map to user
        with open("admin/Id_map.csv", "a") as f:
            f.write(f"{datetime.now()},{str(user_id)}\n")

    elif phase == 2:
        for widget in widgets:
            random.shuffle(presets)
            app = NativeApp(user_id, widget, result_dir="results2")
            app.add_title("Electrotactile Feedback!")
            v = add_required_widgets(app, widget)
            app.add_preset_buttons(presets)
            app.add_save_button()
            app.run()

        with open("admin/Id_map_phase2.csv", "a") as f:
            f.write(f"{datetime.now()},{str(user_id)}\n")

###########################

run(2) #change the argument here for diffent phase of experiment.