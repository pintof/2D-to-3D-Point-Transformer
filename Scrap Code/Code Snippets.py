#Check if an element exists within a 2D array
from itertools import chain
from pydoc import doc
if time in chain(*contentsDepth): #Check if time from current line of Parsed Scan CSV file exists anywhere within 2D Depth Matrix
   print("Found!")





#search for an element within a 2D array, return 2D index if found
for count, iterator in enumerate(contentsDepth):
        if time in iterator:
            print(count, iterator.index(time))





#search for an element within a 2D array, return 2D index if found
import numpy.array_api
a = numpy.array(contentsDepth)
indexI, indexII = numpy.where(a == time)
print(indexI,indexII)



#find last iteration of a loop (only works on sliceable things like lists, and all elements of list must also be unique)
for iterator in list:
   if iterator == list[-1]:

#find last iteration of a loop
for count, iterator in enumerate(list):
   if count == len(list) - 1:
      do...


#Skip first line of iteration (like skipping the header line of a CSV in an iteration loop)
for x in list[1:]:
   do...


#Redirect standard output to a file instead
sys.stdout = open(FileLocation, 'w+') #redirect Standard Output datastream to a file 
sys.stdout.close() #close the file
sys.stdout = sys.__stdout__ #redirect Standard Output stream back to default (from file, back to console)


#Read and iterate through a CSV file (CSV library):
import csv
with open(inputFile) as csv_file:
   csv_reader = csv.reader(csv_file)
   for i in csv_reader:
      do...


#Read and iterate through a CSV file (Pandas library)
import pandas
data = pandas.read_csv(fileLocation)
for i in data:
   do... (can call columns by their header name)



#Read and iterate through a CSV file (no library), and save it into a 2D array that can be iterated through later (2D array is called contentsDepth in this case)
with open(newFileLocation, 'r+') as parsedDepthFile: #Open Parsed Depth CSV file
   contentsDepth = parsedDepthFile.readlines() #read each line of the file separately into a list
   #Load CSV into a 2D matrix
   for i in range(len(contentsDepth)): #Loop through each line of CSV
      contentsDepth[i] = contentsDepth[i].rstrip('\n') #remove \n from the end of every line (messes up formatting of the .split() function)
      contentsDepth[i] = contentsDepth[i].split(',') #split each line into a list, using ',' as the delimiter




#Embed an icon as a string into a tkinter GUI, first convert the .ico into a Base64 string at http://www.motobit.com/util/base64-decoder-encoder.asp
import base64
import os
from Tkinter import *
##The Base64 icon version as a string
icon = \
""" REPLACE THIS WITH YOUR BASE64 VERSION OF THE ICON
"""
icondata= base64.b64decode(icon)
## The temp file is icon.ico
tempFile= "icon.ico"
iconfile= open(tempFile,"wb")
## Extract the icon
iconfile.write(icondata)
iconfile.close()
root = Tk()
root.wm_iconbitmap(tempFile)
## Delete the tempfile
os.remove(tempFile)



#execute a string as Python code (can do multi line code, but cannot give a return value)
exec()



#execute a string as python code (can do single line code, but can return a value as well)
eval()



#Exception handling - try anything, if it doesnt work, print the error, and type of error
try:
   do...
except Exception as e:
   repr(e)




#Exception handling - try anything, if it doesnt work, print the error, type of error, and line of occurrence of error
import traceback
try:
   do...
except Exception:
   traceback.print_exc()





#Check how long which parts of a function take to process
import cProfile
import pstats
with cProfile.Profile() as pr:
   yourFunctionHere()
stats = pstats.Stats(pr)
stats.sort_stats(pstats.SortKey.TIME) #sort the stats by time
stats.print_stats() #print out the stats

#Or as opposed to printing the stats about how much time each part of a function call takes, you can save it to a file
#Then open the file with snakeviz (first do pip install snakeviz), then from CMD do snakeviz filename (filename of the outputted stats)
stats.dump_stats(filename='profiling_stats.prof') #instead of last print_stats() function, do this dump_stats() function instead to save the output to a file
#from CMD, run 'snakeviz profiling_stats.prof' to see a web based graphical analysis
#Instrucitons here https://www.youtube.com/watch?v=m_a0fN48Alw&ab_channel=mCoding
