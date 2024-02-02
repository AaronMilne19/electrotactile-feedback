import random
from tkinter import *
from tkinter import ttk
from typing_extensions import override
from NativeApp import NativeApp

class Phase3NativeApp(NativeApp):

    def __init__(self, user_id:str, descriptor:str=None, title="Electrotactile Feedback", geometry="600x400", result_dir="results3"):
        super().__init__(user_id=user_id, descriptor=descriptor, title=title, geometry=geometry, result_dir=result_dir, phase=3)
        self.text = None

    def set_preset(self, preset:tuple):
        pw, fq, amp = preset
        self.dev.set_pulsewidth(pw)
        self.dev.set_frequency(fq)
        self.dev.set_amplitude(amp)

    #Adds a keypad to the screen such that users can click the buttons to enter a number
    def add_numpad(self):
        self.r += 1
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
            ('0', 4, 0), ('.', 4, 1), ('<-', 4, 2)
        ]
        frame = Frame(self.window)
        frame.grid(row=self.r, padx=10, columnspan=2)
        for (text, row, col) in buttons:
            if text == '<-':
                button = Button(frame, text=text, width=5, height=2, font=('Arial', 14), command=self.backspace)
            else:
                button = Button(frame, text=text, width=5, height=2, font=('Arial', 14),
                                command=lambda t=text: self.numpad_click(t))
            button.grid(row=row, column=col)

    #This function adds text to the screen with the given font size
    def add_message(self, message, font_size=10):
        self.r += 1
        message_display = ttk.Label(self.window, text=message, font=("Arial", font_size))
        message_display.grid(columnspan=2, row=self.r, padx=10, pady=20, sticky="n")

    #Handles what happens when keypad button is pressed
    def numpad_click(self, number):
        self.dev.send_pulse()
        self.text.config(state='normal')
        current = self.text.get()
        self.text.delete(0, END)
        new_str = str(current) + str(number)
        self.text.insert(0, new_str)
        self.verify_input()
        self.text.config(state='disabled')

    #backspace one character from the text box
    def backspace(self):
        self.dev.send_pulse()
        self.text.config(state='normal')
        current = self.text.get()
        self.text.delete(len(current) - 1)
        self.verify_input()
        self.text.config(state='disabled')

    #Verifies the input of the text box
    def verify_input(self,char=""):
        try:
            if char == '\x08':
                self.save_button.config(state='normal') if int(self.text.get()[:-1]) == self.num else self.save_button.config(state='disabled')
            else:
                self.save_button.config(state='normal') if int(self.text.get() + char) == self.num else self.save_button.config(state='disabled')
        except ValueError:
            pass
    
    #Event handler
    def handle_keypress(self, e):
        self.dev.send_pulse()
        self.verify_input(e.char)

    #Overrides existing text input widget to incorporate phase 3 functionality
    @override
    def add_text_widget(self, disabled=True):
        self.r += 1
        if disabled: 
            self.text = ttk.Entry(master=self.window, width=25, state="disabled")
        else:
            self.text = ttk.Entry(master=self.window, width=25)
            self.text.bind("<Key>", lambda e: self.handle_keypress(e))
        self.text.grid(columnspan=2, row=self.r, padx=10, pady=20, sticky="n")

    @override
    #Save results to csv file
    def save_results_exit(self):
        print("override works", self.user_id)
        #if self.user_id != None:
        #    with open(f"{self.result_dir}/{self.user_id}_{self.descriptor}.csv", "a") as f:
        #        f.write(f"{self.dev.get_pulsewidth()},{self.dev.get_frequency()},{self.dev.get_amplitude()}\n")
        self.window.destroy()

    #Generates random number and gets users to type this number into the box
    def add_random_number_input(self, numpad:bool):
        self.num = random.randint(100000, 999999)
        self.add_message(f"Please enter the number {self.num}", 12)
        self.add_text_widget(numpad)
        if numpad:
            self.window.geometry("600x600")
            self.add_numpad()        
