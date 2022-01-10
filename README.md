# CERC Python code repository

Please contact Daniel Hutama if you have any questions or suggestions. 

README.md last edited on 16-Nov-2021.

-----------------------------------------------------------------
INSTRUCTIONS

Within the Core folder, there are five folders:
    1) Dependencies
    2) Documentation
    3) Drivers
    4) GUIs
    5) Methods

Please refer below for information regarding organization within these folders.

1) Dependencies
    
This folder contains code necessary to run most of the files in the "Drivers" folder. There are only 2 cases in which you would need to open this folder: you encounter an error in one of the dependency files, or you are adding a new base functionality that will be used in multiple drivers.

2) Documentation
    
This folder is for manuals, programming instructions, etc.

3) Drivers
    
This folder contains the code needed to control instruments via computer input.

4) GUIs
    
This folder contains graphical user interfaces that execute useful functions. For example, the BandwidthCalc.py file opens a GUI to aid in converting between wavelength and frequency bandwidth.

5) Methods
    
This folder contains custom functions that can have multiple use cases. For instance, a custom function that converts a single wavelength value to its corresponding frequency value should go here. 

This README file will be updated whenever there are new functionalities.


-----------------------------------------------------------------
CHANGELOG for this README file.

16-Nov-2021 | Daniel Hutama | Added instructions for repository usage. 

17-Nov-2021 | Daniel Hutama | Added linebreaks for improved readability.

10-Jan-2022 | Daniel Hutama | Separated Python and Matlab repositories. Changed READMEs accordingly.