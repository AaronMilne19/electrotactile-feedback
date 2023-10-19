from tkinter import *
from tkinter import ttk
from EventHandlers import EventHandlers

############
window = Tk()
event_handlers = EventHandlers()
window.geometry("700x500")
window.title("Electrotactile Feedback")
############

#Title
r = 0
title = ttk.Label(text="Electrotactile Feedback!", font=("Arial", 25)).grid(columnspan=2, row=r, padx=10, pady=20, sticky="n")

#Button
r+=1
button_label = ttk.Label(text="Try clicking this button:").grid(column=0, row=r, padx=10, sticky="e")
button = Button(text="Click me!", width=25, command=event_handlers.handle_button).grid(column=1, row=1, sticky="w", padx=10)

#Text input
r+=1
text_label = ttk.Label(text="Enter some text:").grid(column=0, row=r, padx=10, sticky="e")
text = ttk.Entry(width=25)
text.bind("<Key>", event_handlers.handle_keypress)
text.grid(column=1, row=2, sticky="w", padx=10)

#Multi select checkboxes
r+=1
multi_select_label = Label(text="Select multiple options:").grid(column=0, row=r, padx=10, sticky="e")
multi_select_frame = Frame(window)
multi_select_frame.grid(column=1, row=r, sticky="w", padx=10)
v = []
for i in range(1,6):
    v.append(BooleanVar(value=False))
    multi_select_i = ttk.Checkbutton(text=i, master=multi_select_frame, variable=v[i-1], command=event_handlers.handle_checkbox).grid(row=0, column=i-1, sticky="w")

#Radio buttons
r+=1
radio_select_label = Label(text="Select a radio button:").grid(column=0, row=r, padx=10, sticky="e")
radio_select_frame = Frame(window)
radio_select_frame.grid(column=1, row=r, sticky="w", padx=10)
radio_var = IntVar()
for i in range(1,6):
    radio_select_i = ttk.Radiobutton(text=i, value=i, master=radio_select_frame, variable=radio_var, command=event_handlers.handle_radio).grid(row=0, column=i-1, sticky="w")


########
window.rowconfigure(list(range(r+1)), weight=0, minsize=50)
window.columnconfigure(list(range(2)), weight=1, minsize=50)
window.mainloop()