# 2D-to-3D-Point-Transformer
Project for ASI Group - to convert 2D sonar survey data to 3D by combining the sonar scan data with positional ROV data

## CONTENTS

**2D to 3D Point Transformer.exe** - Main application, standalone program. Takes in a 2D Sonar Scan File, and a temporally matching ROV Depth File, and outputs a 3D point cloud CSV, which can be viewed using https://leica-geosystems.com/products/laser-scanners/software/leica-cyclone/leica-cyclone-3dr/leica-cyclone-3dr-download. Compiled using command 'pyinstaller -w -F --icon=favicon.ico 2D to 3D Point Transformer.py' -w flag is for an application with no additional console log window, -F flag is to compile into 1 single standalone executable instead of an executable with multiple dependant files. The executable has been compiled from a customized version of the source code that has been edited to implement it's icon from a string, instead of a .ico file (This customized code can be found in Scrap Code\Code Snippets.py). The flag --icon=favicon.ico may not even be necessary, or possibly just necessary for some minor system representations of the icon.

*Application Screenshot:*

![Application Screenshot](https://i.imgur.com/K9SkfpC.jpg)

**2D to 3D Point Transformer.py** - Python source code of main application

**favicon.ico** - An icon to go along with the source code for compilation 

**Scrap Code** - Code snippets detailing useful utilizations like how to implement an icon using a string as it's source instead of a .ico file. None of these code snippets are necessary for main application.

**Sonar Scan Files** - The input sonar scan files for the application. There are 2 of them, each match up with a respective ROV Depth File. There is a also a 3rd sonar scan file named randomn, which has no matching ROV depth file, so it cannot be run through the main program. A manual is also included which details what all the values in a raw sonar scan file represent. 2D Sonar Scan Files can be viewed using https://www.tritech.co.uk/support-software/seanet-pro-v2-25

*2D Sonar Scan File Screenshot:*

![2D Sonar Scan](https://i.imgur.com/FSPwljY.jpg)

**ROV Depth File** - The input ROV depth files for the application. There are 2 of them, each coincide with a temporally matching Sonar Scan File. A manual is included which explains what the values in a raw ROV Depth File represent.
