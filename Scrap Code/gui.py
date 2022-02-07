#Import the required Libraries
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

#Create an instance of Tkinter frame
win= Tk()

#Set the geometry of Tkinter frame
win.geometry("750x250")
win.title('2D to 3D Point Transformer')
win.iconbitmap(r"C:\Users\Fraeya Pinto\Downloads\favicon.ico")


def openFileDialogScan():
    inputFile = askopenfilename(title='Select Sonar Scan CSV', filetypes=(('CSV Files','*.csv'),('All Files','*.*'))) #Location of the Scan CSV file to read
    scanEntry.configure(textvariable=StringVar(value=inputFile),state=DISABLED)

def openFileDialogDepth():
    inputFile2 = askopenfilename(title='Select ROVs depth log file') #Location of the Depth Log file to read
    depthEntry.configure(textvariable=StringVar(value=inputFile2),state=DISABLED)

def instructionButton():
   messagebox.showinfo("Instructions", "Explanation:\n\nSonar heads increase reflectance values as range increases, in order to create a uniformly illuminated image. These effects can be reversed however using custom scaling equations. The hope would be that the most illuminated target, would be the intended one, and echoes would be faded to a lesser illumination.\n\nUsable Variables:\n\n\t'i[x]' - Reflectance value of current sonar scan point\n\n\t'currentRange' - Range of current sonar scan point\n\n\t'gain' - Gain\n\nExamples:\n\n\ti[x] = i[x] * (1 / range)\n\nMultiply the current sonar scan point's reflectance value by the reciprocal of it's current range. This will make the reflectance weaker as range increases. Hopefully cancelling out the increased reflectance the sonar adds in, thus giving a more normalized result.\n\n\tif gain > 40:\n\t\ti[x] = i[x] * (1 / range)\n\telif gain <= 40:\n\t\ti[x] = i[x] * (2 / range)\n\nIf gain is strong, so larger than 40 for example, then weaken the reflectance by multiplying it with the standard reciprocal of the range, otherwise though if the gain is weak, so less than 40 for example, then the resolution will be lower, and noise may be lesser, so the reflectance value can be scaled down using a less agressive reciprocal of the range as there will be less noise to fade out.\nDisclaimer: The values of 40 & reciprocal of the range were completely randomn & arbitrary values that were picked to demonstrate a point. The exact values for best results will need to be determined via experimentation.")

def transformButton():
    messagebox.showinfo("success",textBoxEquation.get('1.0','end-1c'))
    

textBoxEquation = Text(height=5, width=95)
textBoxEquation.pack()


#Initialize a Label to display the User Input
ttk.Label(text="Optional: Enter custom scaling equation").pack()

ttk.Button(text= "Read Instructions",width= 20, command= instructionButton).pack()

#Create an Entry widget to accept User Input
scanEntry= Entry(width= 40)
scanEntry.pack(side=LEFT)

#Create a Button to validate Entry Widget
ttk.Button(text= "Select Sonar Scan File",width= 20, command= openFileDialogScan).pack(side=LEFT)

#Create an Entry widget to accept User Input
depthEntry= Entry(width= 40)
depthEntry.pack(side=LEFT)

#Create a Button to validate Entry Widget
test = ttk.Button(text= "Select ROV Depth File",width= 20, command= openFileDialogDepth).pack(side=LEFT)

ttk.Button(text= "Transform!",width= 20, command= transformButton).place(x=310,y=220)

win.mainloop()