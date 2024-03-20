## Build instructions

No official release/executable is available/deployed for this code, however, follow the instructions below to run the application locally.

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

