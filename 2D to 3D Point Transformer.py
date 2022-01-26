import sys, math, csv, os
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename
#Designed for Python 3.10 in January 2022 by Floyd Pinto - floyd.pinto@gmail.com



################
#Create the GUI#
################
#Function to be called when the Select Sonar Scan File button is clicked
def openFileDialogScan():
    inputFile = askopenfilename(title='Select Sonar Scan CSV', filetypes=(('CSV Files','*.csv'),('All Files','*.*'))) #Opens a file select dialog box for the user, allows them to select a .csv files, then stores this path in the variable inputFile 
    scanEntry.configure(textvariable=StringVar(value=inputFile), state=DISABLED) #Populates the scan Entry box with the path of the user selected sonar scan .csv file, also disable the Entry box making it gray and uneditable, letting the user know the required action has been completed for this UI component
#Function to be called when the Select ROV Depth File button is clicked
def openFileDialogDepth():
    fileLocation = askopenfilename(title='Select ROVs depth log file') #Opens a file select dialog box for the user, allows them to select a file, then stores this path in the variable fileLocation 
    depthEntry.configure(textvariable=StringVar(value=fileLocation), state=DISABLED) #Populates the depth Entry box with the path of the user selected ROV depth log file, also disable the Entry box making it gray and uneditable, letting the user know the required action has been completed for this UI component
#Function to be called when the Read Instructions button is clicked
def instructionButton():
   messagebox.showinfo("Instructions", "Explanation:\n\nSonar heads increase reflectance values as range increases, in order to create a uniformly illuminated image. These effects can be reversed however using custom scaling equations. The hope would be that the most illuminated target, would be the intended one, and echoes would be faded to a lesser illumination.\n\nUsable Variables:\n\n\t'i[x]' - Reflectance value of current sonar scan point\n\n\t'currentRange' - Range of current sonar scan point\n\n\t'gain' - Gain\n\nExamples:\n\n\ti[x] = i[x] * (1 / range)\n\nMultiply the current sonar scan point's reflectance value by the reciprocal of it's current range. This will make the reflectance weaker as range increases. Hopefully cancelling out the increased reflectance the sonar adds in, thus giving a more normalized result.\n\n\tif gain > 40:\n\t\ti[x] = i[x] * (1 / range)\n\telif gain <= 40:\n\t\ti[x] = i[x] * (2 / range)\n\nIf gain is strong, so larger than 40 for example, then weaken the reflectance by multiplying it with the standard reciprocal of the range, otherwise though if the gain is weak, so less than 40 for example, then the resolution will be lower, and noise may be lesser, so the reflectance value can be scaled down using a less agressive reciprocal of the range as there will be less noise to fade out.\nDisclaimer: The values of 40 & reciprocal of the range were completely randomn & arbitrary values that were picked to demonstrate a point. The exact values for best results will need to be determined via experimentation.")
win= Tk() #Create an instance of Tkinter frame
win.geometry("750x250") #Set the geometry of Tkinter frame
win.title('2D to 3D Point Transformer') #Set the title of Tkinter frame
#If the icon file exists in the same directory of the current python file, then set that as the icon of the Tkinter frame. Use exception handling to prevent the possible file not found error from halting program execution
try:
    win.iconbitmap(os.path.abspath(os.getcwd())+r'\favicon.ico')
except:
    pass
textBoxEquation = Text(height=5, width=95) #Create the textbox for the user to input their custom scaling equation
textBoxEquation.pack() #Place the textbox on the GUI
ttk.Label(text="Optional: Enter custom scaling equation").pack() #Display instructional text on the GUI
ttk.Button(text= "Read Instructions",width= 20, command= instructionButton).pack() #Create a Read Instructions button for the user to click, to read instructions about the scaling equation parameters
scanEntry= Entry(width= 40) #Create Entry box (to be populated with the path of the selected sonar scan file, so that the path is visible to the user)
scanEntry.pack(side=LEFT) #position the Entry box
ttk.Button(text= "Select Sonar Scan File",width= 20, command= openFileDialogScan).pack(side=LEFT) #Create a button, onclick a function executes that opens a select file dialog box for the user to select a sonar scan .csv file, and populates the path of this selected file into the adjacent entry box
depthEntry= Entry(width= 40) #Create Entry box (to be populated with the path of the selected ROV depth log file, so that the path is visible to the user)
depthEntry.pack(side=LEFT) #position the Entry box
ttk.Button(text= "Select ROV Depth File",width= 20, command= openFileDialogDepth).pack(side=LEFT) #Create a button, onclick a function executes that opens a select file dialog box for the user to select a ROV depth log file, and populates the path of this selected file into the adjacent entry box
#Function to be called when the Transform! button is clicked, this executes the bulk of the processing code, which takes in two 2D survey data files, and outputs a 3D survey data file
def transformButton():
    #######################################################
    #Open Scan CSV file, and output a Parsed Scan CSV file#
    #######################################################
    inputFile = scanEntry.get() #Get the path of the sonar scan .csv file from the text currently entered in the scan Entry box
    outputFile = inputFile[:-4] + '__PARSED__.CSV' #Location of the Parsed Scan CSV file to output
    with open(inputFile) as csv_file, open(outputFile,'w+', newline='', encoding='utf-8') as csv_output: #Change newline character from '\n' to '' to handle line breaks manually
        csv_reader = csv.reader(csv_file)
        csv_writer = csv.writer(csv_output, delimiter=' ', quotechar='"', quoting=csv.QUOTE_NONE, escapechar=' ', lineterminator='') #Change lineterminator character from '\n' to '' to handle line breaks manually, change delimiter from ',' to ' ' to eliminate the quotations this CSV parsing library puts around inputted values
        next(csv_reader) #Skip parsing the header (causes errors, as there aren't headers for every column, cannot manually put in the headers either, as the number of columns starts to change mid-file in some files, as the number of Dbytes can change mid file)
        csv_writer.writerow(['DateTime,Bearing,DbyteMAX,DbyteMAXRange(m)\r\n'])
        for i in csv_reader: #Loop through each row of the CSV
            csv_writer.writerow([i[1]+','])  #Output DateTime to new CSV
            csv_writer.writerow([i[13]+',']) #Output Bearing to new CSV
            DbyteMAX = 0 #Reset value back to zero for every new parse of a row
            DbyteMAXRange = 0 #Reset value back to zero for every new parse of a row
            for x in range(15,15+int(i[14])): #Loop through all the Dbyte values (this is done dynamically by getting the number of Dbyte values from the Dbyte column evertime a new row parses, so if the number of Dbytes changes mid file, this can be handled)
                i[x] = float(i[x]) #Convert the Dbyte values to integers for mathematical processing (this CSV parsing library reads the values in as strings)
                currentRange = float(int(i[5]) / 10 / int(i[14]) * (x-14)) #Get range of current Dbyte (Create as an easy to read variable for the user to use via the code injection equation)
                gain = float(i[6]) #Get gain (Create easy to understand variable name, for user to use with code injection equation)
                #If the custom scaling equation textbox is not blank, then execute it's user inputted text as code at this point in the program. 1.0 denotes the start range of the get() which gets the 1st line, at the [0] character. end-1c is the ending index range of the get(), it gets the end minus 1 character (the \n character which is automatically added by the system). The get() for tkinter Text boxes requires mandatory index ranges to be put in for the input parameters, unlike most other get() which can be left blank
                if textBoxEquation.get('1.0','end-1c') != '':
                    try:
                        exec(textBoxEquation.get('1.0','end-1c'))
                    #If the user inputted code injection equation throws an error, then display the error to the user, then restart the program
                    except Exception as errorMsg:
                        messagebox.showerror("Bad Code Injection equation used", repr(errorMsg) + '\n\nProgram will now restart')
                        os.execl(sys.executable, os.path.abspath(__file__))
                #If the current Dbyte value being iterated through, is bigger than the previous MAX, then this value becomes the new MAX, the range of this Dbyte is also recorded
                if i[x] > DbyteMAX:
                    DbyteMAX = i[x] #Assign the new MAX from the current Dbyte
                    DbyteMAXRange = int(i[5]) / 10 / int(i[14]) * (x-14) #Assign the range of the MAX, this is done dynamically by getting the RangeScale from the current row everytime a new row is parsed (so different RangeScales can be handled), this RangeScale is then divided by 10 to convert from decimeters to meters, then divided by the number of Dbytes (again acquired dynamically) to get the range of a single Dbyte, this value is then multiplied by the currnet DbyteMAX to get that MAX's range
            csv_writer.writerow([str(DbyteMAX)+',']) #Output DbyteMAX to new CSV
            csv_writer.writerow([str(DbyteMAXRange)+'\r\n']) #Output DbyteMAXRange to new CSV
    ##############################################
    #Open Depth CSV and output a parsed Depth CSV#
    ##############################################
    fileLocation = depthEntry.get() #Get the path of the ROV depth log file from the text currently entered in the depth Entry box
    newFileLocation = fileLocation[:fileLocation.rfind('.')] + '__PARSED__.csv' #location of output Parsed Depth CSV to write
    sys.stdout = open(newFileLocation, 'w+') #redirect Standard Output datastream to a file (the new Parsed Depth CSV file which will be written)
    print('Time,Heading,Depth(m)') #Print Header line to new CSV
    #Open Depth Log file for parsing, and output parsed data to new CSV
    with open(fileLocation, 'r+') as f:
        contents = f.readlines() #read each line of the file separately into a list
        for line in contents: #Loop through each line in the list of lines
            if len(line) == 120:
                print(line[11:24] + line[57:63] + ',' + str(float(line[90:97])*1.02)) #Output time + Heading + Pressure Depth*1.02 (convert from decibar to meters of head pressure) to CSV
    sys.stdout.close() #close the Parsed Depth CSV file
    sys.stdout = sys.__stdout__ #redirect Standard Output stream back to default (from file, back to console)

    #Load Parsed Depth CSV file into a 2D matrix
    with open(newFileLocation, 'r+') as parsedDepthFile: #Open Parsed Depth CSV file
        contentsDepth = parsedDepthFile.readlines() #read each line of the file separately into a list
        #Load CSV into a 2D matrix
        for i in range(len(contentsDepth)): #Loop through each line of CSV
            contentsDepth[i] = contentsDepth[i].rstrip('\n') #remove \n from the end of every line (messes up formatting of the .split() function)
            contentsDepth[i] = contentsDepth[i].split(',') #split each line into a list, using ',' as the delimiter
    ##########################################################################################
    #Open Parsed Scan CSV file, and parse it along with Depth Matrix into the final X,Y,Z CSV#
    ##########################################################################################
    XYZFileLocation = fileLocation[:fileLocation.rfind('/')+1] + 'XYZ.csv' #location of output CSV to write
    sys.stdout = open(XYZFileLocation, 'w+') #redirect Standard Output datastream to a file (the new XYZ CSV file which will be written)
    with open(outputFile, 'r+') as parsedScanFile: #Open Parsed Scan CSV file
        print('ScanTime,DepthTime,ScanTime&DepthTimeDelta,Bearing(1/16 Gradians),Heading(Degrees),Bearing+Heading(Degrees),Reflectance,Range,X(m),Y(m),Z(m)') #Output header line
        contentsScan = parsedScanFile.readlines() #read each line of the file separately into a list
        for line in contentsScan[1:]: #Loop through the list of lines, and skip the first line (the header)
            line = line.rstrip('\n') #Remove \n from end of line to ensure proper formatting with the split() function
            line = line.split(',') #Split the line on the delimiter ',' into a list
            scanTime = line[0][:line[0].rfind('.')] #Store time (omitting milliseconds) from current line in a variable
            scanMillisecondTime = line[0][line[0].rfind('.'):] #Store only the milliseconds of the time from the current line
            millisecondDifference = 1 #Reset this value everytime the loop iterates (this value is used as placeholder to compare the difference in milliseconds between the Scan CSV & Depth CSV, in order to find the smallest delta)
            scanSkipFlag = True #Reset this value everytime the loop iterates (this Flag is used to know when to skip over lines of the Scan CSV, if there are no matching timestamps between both files)
            depthIndex = 0 #Reset this value everytime the loop iterates (this value is used to record the index of the Depth Matrix which had the closest timestamp to the current line of the Scan CSV)
            hypotenuse = float(line[3])
            #Find the index of the Depth Matrix which closest matches the timestamp of the current line of the Scan CSV, if there is no match within the same second, then skip this line of Scan CSV
            for count, iterator in enumerate(contentsDepth): #Loop through Depth Matrix
                #if the Scan timestamp and Depth timestamp are the same (excluding milliseconds), then set the skip Flag to False
                if scanTime == iterator[0][:iterator[0].rfind('.')]:
                    scanSkipFlag = False
                    #Get the index of the Depth Matrix which has the smallest differential between the millliseconds of the Scan CSV's timestamp, and Depth Matrix's timestamp
                    if abs(float(scanMillisecondTime) - float(iterator[0][iterator[0].rfind('.'):])) < float(millisecondDifference):
                        millisecondDifference = abs(float(scanMillisecondTime) - float(iterator[0][iterator[0].rfind('.'):]))
                        depthIndex = count
            if scanSkipFlag == False: #Only output parsed data if skip Flag is set to False
                BearingHeading = float(line[1])*(1/16)*0.9 + float(contentsDepth[depthIndex][1]) #Add bearing & heading (in degrees, by first converting 1/16 Bearing Gradians to Degrees)
                if BearingHeading > 360: BearingHeading -= 360 #If Bearing + Heading is greater than 360, than restart the portion of the value greater than 360 back at zero (this maintains the value in degrees)
                if 0 <= BearingHeading < 90: angle = 90 - BearingHeading; y = math.sin(math.pi/180*angle) * hypotenuse; x = math.sqrt(hypotenuse**2 - y**2) #Solve X & Y if Bearing+Heading angle falls in Quadrant 1, Use Sin(angle) = opposite/hypotenuse to solve for y, then use Pythagorean Theorem to solve for x. Note sin() function uses radians, so degrees must be converted to radians by multiplying by pi/180
                if 90 <= BearingHeading < 180: angle = BearingHeading - 90; y = math.sin(math.pi/180*angle) * hypotenuse; x = math.sqrt(hypotenuse**2 - y**2); y = -y #Solve for X & Y if Bearing+Heading angle falls in Quadrant 4, adjust angle so that it's measured from the x-axis instead of 0, and change the y value to a negative
                if 180 <= BearingHeading < 270: angle = 270 - BearingHeading; y = math.sin(math.pi/180*angle) * hypotenuse; x = math.sqrt(hypotenuse**2 - y**2); y = -y; x = -x #Solve for X & Y if Bearing+Heading angle falls in Quadrant 3, adjust angle so that it's measured from the x-axis instead of 0, and change the x & y values to negative
                if 270 <= BearingHeading <= 360: angle = BearingHeading - 270; y = math.sin(math.pi/180*angle) * hypotenuse; x = math.sqrt(hypotenuse**2 - y**2); x = -x #Solve for X & Y if Bearing+Heading angle falls in Quadrant 2, adjust angle so that it's measured from the x-axis instead of 0, and change the x value to negative
                print(line[0],end=',') #Output Scan Timestamp
                print(contentsDepth[depthIndex][0],end=',') #Output closest matching Depth Timestamp
                print(millisecondDifference,end=',') #Output delta between Scan timestamp and closest matching Depth timestamp
                print(line[1],end=',') #Output Scan Bearing
                print(contentsDepth[depthIndex][1],end=',') #Output Depth Heading
                print(BearingHeading,end=',') #Ouput Bearing+Heading (in Degrees)
                print(line[2],end=',') #Output Reflectance of the Max
                print(hypotenuse,end=',') #Output Range of the Max
                print(x,end=',') #Output X 
                print(y,end=',') #Output Y
                print(contentsDepth[depthIndex][2],end='\n') #Output Z (depth)
    sys.stdout.close() #close the XYZ CSV file
    sys.stdout = sys.__stdout__ #redirect Standard Output stream back to default (from file, back to console)
    os.remove(outputFile) #Delete intermediary CSV (Parsed Scan CSV)
    os.remove(newFileLocation) #Delete intermediary CSV (Parsed Depth CSV)
    scanEntry.configure(state=NORMAL) #Set the Entry box for the sonar scan file path back to normal, thus re-enabling the box, indicating that the program has finished running successfully, and the box can be edited again (the box is disabled & uneditable whilst the main Transform function is running)
    depthEntry.configure(state=NORMAL) #Set the Entry box for the ROV depth log file path back to normal, thus re-enabling the box, indicating that the program has finished running successfully, and the box can be edited again (the box is disabled & uneditable whilst the main Transform function is running)
    messagebox.showinfo("Output File Location", "3D Points file successfully written to:\n"+XYZFileLocation) #Upon completion of creation of the XYZ.csv file (the final output), send a message box prompt to the user, notifying them of successful completion, and of location of newly created XYZ.csv file
ttk.Button(text= "Transform to 3D!",width= 20, command= transformButton).place(x=310,y=220) #Create the Transform button, onclick the processing part of the program executes, which takes in two 2D survey data files from the user specified paths in the 2 Entry boxes, and ouputs a 3D survey data .csv file
win.mainloop() #Create a continuous loop for the GUI, which continually listens for events like button clicks