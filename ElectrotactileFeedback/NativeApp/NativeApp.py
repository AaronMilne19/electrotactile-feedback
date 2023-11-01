from doctest import master
from tkinter import *
from tkinter import ttk
import tkdial as tkd
from FESService import FESService

class NativeApp:
    
    window = Tk()
    dev = FESService()
    r = -1

    def __init__(self, title="Electrotactile Feedback", geometry="700x500"):
        self.window.geometry(geometry)
        self.window.title(title)

    #Title
    def add_title(self):
        self.r += 1
        ttk.Label(master=self.window, text="Electrotactile Feedback!", font=("Arial", 25)).grid(columnspan=2, row=self.r, padx=10, pady=20, sticky="n")

    #Button
    def add_button_widget(self):
        self.r += 1
        ttk.Label(master=self.window, text="Try clicking this button:").grid(column=0, row=self.r, padx=10, sticky="e")
        Button(master=self.window, text="Click me!", width=25, command=self.dev.send_pulse).grid(column=1, row=1, sticky="w", padx=10)

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
            ttk.Checkbutton(text=i, master=multi_select_frame, variable=v[i-1], command=self.dev.send_pulse).grid(row=0, column=i-1, sticky="w")
        return v

    #Radio buttons
    def add_radio_widget(self):
        self.r += 1
        Label(text="Select a radio button:").grid(column=0, row=self.r, padx=10, sticky="e")
        radio_select_frame = Frame(self.window)
        radio_select_frame.grid(column=1, row=self.r, sticky="w", padx=10)
        radio_var = IntVar()
        for i in range(1,6):
            ttk.Radiobutton(text=i, value=i, master=radio_select_frame, variable=radio_var, command=self.dev.send_pulse).grid(row=0, column=i-1, sticky="w")

    #Device parameter dials
    def add_parameter_dials(self, pw_val=0, fq_val=0, amp_val=0):
        self.r += 1
        dial_frame = Frame(self.window)
        dial_frame.grid(columnspan=2, row=self.r, padx=10, pady=20)
        pulsewidth_dial = tkd.Dial(master=dial_frame, text="Pulsewidth (μs):\n ", radius=35, scroll_steps=10, integer=True,
                        color_gradient=("green", "red"), unit_length=7, unit_width=7, height=150, width=100, end=200,
                        command=lambda: self.dev.set_pulsewidth(pulsewidth_dial.get()))
        frequency_dial = tkd.Dial(master=dial_frame, text="Frequency (PPS):\n ", radius=35, scroll_steps=5, integer=True,
                        color_gradient=("green", "red"), unit_length=7, unit_width=7, height=150, width=100, end=99,
                        command=lambda: self.dev.set_frequency(frequency_dial.get()))
        amplitude_dial = tkd.Dial(master=dial_frame, text="Amplitude (mA):\n ", radius=35, scroll_steps=1, integer=True,
                        color_gradient=("green", "red"), unit_length=7, unit_width=7, height=150, width=100, end=20,
                        command=lambda: self.dev.set_amplitude(amplitude_dial.get()))
        pulsewidth_dial.set(pw_val)
        frequency_dial.set(fq_val)
        amplitude_dial.set(amp_val)
        pulsewidth_dial.grid(row=0, column=0, padx=10)
        frequency_dial.grid(row=0, column=1, padx=10)
        amplitude_dial.grid(row=0, column=2, padx=10)

    #Configure window scaling and run the app
    def run(self):
        self.window.rowconfigure(list(range(self.r+1)), weight=0, minsize=50)
        self.window.columnconfigure(list(range(2)), weight=1, minsize=50)
        self.window.mainloop()


####################
app = NativeApp()
app.add_title()
app.add_button_widget()
app.add_text_widget()
v = app.add_multi_selection_widget()
app.add_radio_widget()
app.add_parameter_dials()
app.run()