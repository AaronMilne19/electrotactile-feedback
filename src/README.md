# ReadMe

Source code for the application presented to users during electrotactile feedback evaluations. This includes three different modes, depending on which evaluation is being run.

- **Evaluation One:** App presents users with four different widget types (button, radio, multi-select and text) three times each, in a random order. Interaction with these sends an electrotactile signal to the user. Dials control parameters of the signal. Chosen values are saved to `../data/raw/results`.
- **Evaluation Two:** Same as before, except instead of dials, there are 5 discrete parameter presets - determined through analysis of responses to evaluation one. Preferred presets are saved to `../data/raw/results2`.
- **Evaluation Three:** First shows 10 number entry tasks to users with no feedback, then 10 number entry tasks with feedback. 10 Phrase entry tasks are then shown with no feedback, then 10 with. Times and keystrokes are saved to `../data/raw/results3`.
 
### Code Structure

- `./FESDriver/` Directory contains Visual Studio project for driver code required to communicate with connected electrotactile device. This is a modification of existing code used by [Yousef *et al*](https://doi.org/10.1109/HAPTICS45997.2020.ras.HAP20.13.8ee5dc37).
- `./NativeApp/` Directory contains Visual Studio project for all custom app logic. **Note:** This is the startup project so runtime directory is inside here.
	- `main.py` Main runner code for the app. Instantiates NativeApp objects shows as windows to the user.
	- `NativeApp.py` Class representing the GUI windows shown to users. Contains functionality appropriate for evaluations one and two.
	- `Phase3NativeApp.py` An extension of `NativeApp`. Overriding some functionality which was different for the final evaluation, such as contents of results being saved.
	- `./NativeApp/admin/` Id maps will be saved to this directory after each user. Allowing local copy of map between participant IDs and names to be preserved. Contents are ignored from source control to maintain subject anonymity.

### Switching Between Modes

To switch between application modes, alter the argument value in the `run(mode)` function call at `line 150` of `./NativeApp/main.py`

Mode argument can equal either 1, 2 or 3, depending on the evaluation you would like to run.


## Build instructions

No official release/executable is available/deployed for this code, however follow the instructions below to run the application locally.

### Requirements

The following components were used to develop and run the code:

- Visual Strudio Community 2022 (Should work on 2019 version)
	- Python development workload installed. 
- Python 3.9 (64 bit) runtime environment.
- Packages: listed in `./NativeApp/requirements.txt`.
- Tested on Windows 10.
- If you want to experience the electrotactile feedback while interacting with the app, you will need the MOTIONSTIM 8 FES device connected before launching the app. (Note: app will run without this).

### Build and Run steps

1. Clone the repo into a directory of your choice.
2. Open Visual Studio 2022 Community IDE
3. Use the 'Open a project or solution' option to open the `./src/ElectrotactileFeedback.sln` file.
4. In the Solution Explorer, right click the `NativeApp` project and choose the option for 'Set as Startup Project'.
5. Expand the NativeApp project and 'Python Environments' tab.
6. Right click Python 3.9 (64-bit) and click install from requirements.txt.
7. This should install the required libraries and you should be able to run the code by hitting F5.
8. Change application modes as described above.

### Test steps

The application is working correctly if you are able to complete all windows and result files are saved to `data/raw/...`.

