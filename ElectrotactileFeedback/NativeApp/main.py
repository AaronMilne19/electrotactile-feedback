from cmath import phase
import datetime
import itertools
import random
import uuid
from NativeApp import NativeApp
from Phase3NativeApp import Phase3NativeApp


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

def get_presets(phase, widget=None):
    if phase == 1 or widget == None:
        return [(150,70,8),(50,50,15),(100,20,20)]
    elif phase == 2:
        if widget == "button":
            return [(64, 29, 8), (78, 42, 10), (92, 56, 11), (116, 70, 12), (139, 85, 14)]
        elif widget == "text":
            return [(59, 20, 8), (78, 34, 9), (97, 49, 11), (118, 59, 12), (139, 70, 14)]
        elif widget == "multi":
            return [(50, 23, 8), (70, 36, 10), (89, 49, 11), (113, 59, 14), (137, 70, 16)]
        elif widget == "radio":
            return [(66, 20, 8), (81, 34, 9), (97, 47, 10), (115, 56, 12), (132, 66, 13)]

def run_test(phase):
    #Create one version of the app which does not save any response - use this as a demonstation
    test_app = NativeApp(None)
    test_app.add_title("Demonstation Window")
    test_app.add_button_widget()
    if phase == 1:
        presets = get_presets(phase) #Phase 1 presets (for seeding the dials)
        test_app.add_parameter_dials()
    elif phase == 2:
        #Phase 2 presets based on analysis of phase 1 responses. These are fixed presets. random for the demo window.
        test_app.phase = 2
        presets = get_presets(phase, "button") 
        test_app.add_preset_buttons(presets)
    test_app.add_save_button()
    test_app.run()

def run_phase1(widgets, user_id):
    presets = get_presets(1)
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

def run_phase2(widgets, user_id):
    wid_3 = widgets * 3
    random.shuffle(wid_3)
    for widget in wid_3:
        presets = get_presets(2, widget)
        random.shuffle(presets)
        app = NativeApp(user_id, widget, result_dir="results2", phase=2)
        app.add_title("Electrotactile Feedback!")
        v = add_required_widgets(app, widget)
        app.add_preset_buttons(presets)
        app.add_save_button()
        app.run()

    #TODO: Add another iteration where the user ranks their preference of presets.
    app = NativeApp(user_id=None, phase=2)
    app.edit_bg_colour('orange')
    app.add_title("Please Rank Your Favourite Presets.")
    app.add_button_widget()
    presets = get_presets(2, "button")
    app.add_preset_buttons(presets)
    app.add_save_button()
    app.run()

    with open("admin/Id_map_phase2.csv", "a") as f:
        f.write(f"{datetime.now()},{str(user_id)}\n")

def run_phase3(user_id):
    #Run with keypad, and typing 10x each, record the time taken and the number of keys pressed.
    iters = 10
    phase_3_app(user_id, iters, True)
    phase_3_app(user_id, iters, True, (100, 50, 10))
    phase_3_app(user_id, iters, False)
    phase_3_app(user_id, iters, False, (100, 50, 10))

def phase_3_app(user_id, iters, keypad:bool, preset=(0,0,0)):
    for i in range(iters):
        app = Phase3NativeApp(user_id)
        app.set_preset(preset) #TODO: Edit this to match presets from analysis
        app.add_title("Electrotactile Feedback!")
        app.add_random_number_input(keypad)
        app.add_save_button()
        app.run()

def run(phase=1):
    user_id = uuid.uuid4()
    print(user_id)
    widgets = ["button", "text", "radio", "multi"]
    if phase == 1:
        run_test(1)    
        run_phase1(widgets, user_id)
    elif phase == 2:
        run_test(2)
        run_phase2(widgets, user_id)
    elif phase == 3:
        run_phase3(user_id)


###########################

run(3) #change the argument here for diffent phase of experiment.