# ApsimNG data extraction and vizualization
Basic data extraction and vizualization of data using the ApsimNG simulator.

Uses the ApsimNG source code GitHub repository: <https://github.com/APSIMInitiative/ApsimX>

## Using the program:
1. Git Clone the APSIM repository
2. Git Clone this repository

    Obs: Keep in mind where the repositories are being stored.

3. Install all the dependecies and libraries needed to execute the program.

    All needed libraries are in the pyproject.toml file

4. Update the directories

    Update the directories in the file constants.py.

        - APSIM_DIR: Point where the ApsimNG source code is stored;
        - SIMULATION_DIR: Point where the simulation .apsimx is stored;
        - FIELDS_FILE: Point and update the report fields that you wish to extract and visualize (OPTIONAL).

    Obs: When running the program, keep in mind that you may have to change the directory of where the .met file is located using your [Weather] manager when using your ApsimNG simulations, as the simulator doesn't change that automatically.

5. Run the program

    Run the program executing the main.py file

All the results are in the output archive