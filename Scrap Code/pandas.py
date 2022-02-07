import pandas
import sys

fileLocation = sys.argv[1] #location of input CSV (entered by user via command line arguement)
newFileLocation = fileLocation[:fileLocation.rfind('.')] + '__PARSED__.csv' #location of output CSV to write

#Check if file's header has same number of columns as rest of file, if not, add commas to header to make blank header entries for rest of columns (If you dont do this, most CSV parsing libraries will work buggy) 
with open(fileLocation, 'r+') as f:
    contents = f.readlines() #read each line of the file separately into a list
    commaCount1 = contents[0].count(',') #count the number of commas in the first line
    commaCount2 = contents[1].count(',') #count the number of commas in the second line
    #if there as less commas in line 1 than 2, then add commas to line 1 to make it equal to the commas in line 2 
    if commaCount1 < commaCount2:
        contents[0] = contents[0].rstrip("Dbytes of DATA\n") + 'Dbyte1\n'
        commaDifference = commaCount2 - commaCount1
        for i in range(commaDifference):
            contents[0] = contents[0].rstrip('\n') + ',' + 'Dbyte' + str(i+2) + '\n'
        f.seek(0) #put the file cursor back to the beginning of the file
        f.truncate() #resize the file to the current cursor position (position is 0 so everything gets deleted)
        i = 0
        #write all the lines back into the file
        for ii in contents: 
            f.write(contents[i])
            i += 1

df = pandas.read_csv(fileLocation,low_memory=False) #open a dataframe which reads everything inside the CSV
sys.stdout = open(newFileLocation, 'w+') #redirect Standard Output datastream to a file (the CSV file which will be written)
print('DateTime,Bearing,DbyteMAX,DbyteMAXRange(meters)') #write the header for the CSV
#parse DateTime, Bearing, and DbyteMAX values out
for i in range(len(df['Dbytes'])): #Loop through all rows (done by getting the length of any column, Dbytes was used in this case)
    print(df['DateTime'][i],end=',') #Parse out DateTime to CSV
    print(df['Bearing'][i],end=',') #Parse out Bearing to CSV
    #Parse out DbytesMAX & DbytesMAXRange to CSV
    Dbytes = [] #reset the list back to blank for every fresh new parse of a row
    DbytesMAX = 0 #reset the value back to zero for every fresh new parse of a row
    DbytesMAXRange = 0 #reset the value back to zero for every fresh new parse of a row
    for ii in range(df['Dbytes'][0]): #Loop through all the Dbyte columns (this is done by using the value in the Dbytes cell which denotes the number of Dbytes, 635 in this case)
        Dbytes.append(df['Dbyte'+str(ii+1)][i]) #Create a list of all 635 dbyte values
        #If the current value in the Dbytes list is greater than the previous MAX, then this value becomes the MAX, and it's range is recorded as well
        if Dbytes[ii] > DbytesMAX:
            DbytesMAX = Dbytes[ii]
            DbytesMAXRange = df['Rangescale'][0] / 10 / df['Dbytes'][0] * (ii+1) #Get the current DbyteMAX's range in meters (Take the full range(Rangescale): 60 decimeters in this case, divide it by 10 to get it in meters, divide it by Dbytes(635 in this case) to get the range of a single Dbyte, then multiply the range of a single Dbyte by the number of dbytes that signify the current max (ii+1))
    print(DbytesMAX,end=',') #Parse out DbytesMAX to CSV
    print(DbytesMAXRange) #Parse out DbytesMAXRange to CSV
sys.stdout.close()