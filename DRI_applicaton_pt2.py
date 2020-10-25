#############################################################################################################################
#Filename: DRI_application_p2.py
#Author:   Shawn Ray
#Description: This file is the application for the internship for The Desert Research Institute (DRI), satisfies the requirements
#                and the bonus objectives for part 2.
##############################################################################################################################
import sys                                  # system handler 
import csv
import json
from math import floor

stationCSV  = sys.argv[1]
stateAbbrev = sys.argv[2]

def main(stationCSV, stateAbbrev):          # Pass by value to enforce modularity
                                            # Dictionary of all the state codes, names included for printing and ease of access
    stateDict = {    'AL':'Alabama'       , 'AK':'Alaska'     ,'AZ':'Arizona'        ,'AR':'Arkansas'       ,'CA':'California'    ,'CO':'Colorado'      ,'CT':'Connecticut'      ,'DE':'Delaware'  ,
                     'FL':'Florida'       , 'GA':'Georgia'    ,'HI':'Hawaii'         ,'ID':'Idaho'          ,'IL':'Illinois'      ,'IN':'Indiana'       ,'IA':'Iowa'             ,'KS':'Kansas'    ,'KY':'Kentucky'  ,
                     'LA':'Louisiana'     , 'ME':'Maine'      ,'MD':'Maryland'       ,'MA':'Massachusetts'  ,'MI':'Michigan'      ,'MN':'Minnesota'     ,'MS':'Mississippi'      ,'MO':'Missouri'  ,'MT':'Montana'   ,
                     'NE':'Nebraska'      , 'NV':'Nevada'     ,'NH':'New Hampshire'  ,'NJ':'New Jersey'     ,'NM':'New Mexico'    ,'NY':'New York'      ,'NC':'North Carolina'   ,
                     'ND':'North Dakota'  , 'OH':'Ohio'       ,'OK':'Oklahoma'       ,'OR':'Oregon'         ,'PA':'Pennsylvania'  ,'RI':'Rhode Island'  ,'SC':'South Carolina'   ,
                     'SD':'South Dakota'  , 'TN':'Tennessee'  ,'TX':'Texas'          ,'UT':'Utah'           ,'VT':'Vermont'       ,'VA':'Virginia'      ,'WA':'Washington'       ,
                     'WV':'West Virginia' , 'WI':'Wisconsin'  ,'WY':'Wyoming'        
                }

    try:
                                            # If either inputs is none, don't run
        if stationCSV is None or stateAbbrev is None:
            raise TypeError("Error: A csv file and an abbreviation for a state is required.")
                                            # All states have 2 character codes
        if len(stateAbbrev) != 2:
            raise TypeError("Error: Improper state code designated, Please use the two character system in place for the Country.")
                                            # Was the code typed wrong?
        if not stateAbbrev in stateDict.keys():
            raise TypeError("Error: The two digit code specified in not found within the Country. Please try again.")
                                            # Was the extension missing?
        if stationCSV.find('.csv') == -1:
            raise TypeError("Error: The file specified is not a csv. Please try again.")
        
                                            # Open the file for reading 
        with open(stationCSV, 'r') as file:

            maxLocation    = 0
            minLocation    = 0 
            median1        = 0 
            median2        = 0 
            average        = 0
            count          = 0
            aboveSea       = 0
            above2000      = 0
            above4000      = 0
            above6000      = 0
            stateData      = []

            reader = csv.reader(file)      

            for row in reader:              # O(n) time complexity 
               
                if row[1] == stateAbbrev:   # Only operate when the state code matches 
                                            # add the elevation to average
                    stateData.append(
                                        row
                                    )       # store only the relevant state data in a list so locations can be found without
                                            # the need to parse the whole file. Inefficient for large datasets.
                                            # TODO: Locate more effective method for acquiring the information from the CSV

                    if row[3] == '':        # if the line is empty (no elevation data found) add a zero to the average
                        average      = average + 0
                    else:                   # Compute the average
                        average      = average + int(float(row[3]))
                                            # If the current row is bigger than max, it is the new max
                        if int(float(row[3])) > maxLocation:
                            maxLocation = count

                                            # If the current row is smaller than min, it is the new min(if min is 0 then anything is a minimum)
                        if int(float(row[3])) < minLocation or minLocation == 0:
                            minLocation = count
                                            # If the elevation is higher than sea level, keep track
                        if int(float(row[3])) > 0:
                            aboveSea  = aboveSea  + 1
                                            # 2000 feet is above sea level
                        if int(float(row[3])) > 2000:
                            above2000    = above2000    + 1
                                            # 4000 feet is also above 2000 fett
                        if int(float(row[3])) > 4000: 
                            above4000    = above4000    + 1
                                            # lastly 6000 feet is indeed above 4000 feet 
                        if int(float(row[3])) > 6000:
                            above6000    = above6000    + 1
                    count = count + 1       # Keep track of how many iterations are run for the average and location

            jData               = {}
            jData[stateDict[stateAbbrev]]  = []
            average = average / count
            if count % 2 == 0:              # Even amount of data set
                median1 = floor(count/2)
                median2 = floor(count/2)+1
                                            # Construct the JSON object                
                jData[stateDict[stateAbbrev]].append({
                'The maximum station' : stateData[int(maxLocation)],
                'The minimum station' : stateData[int(minLocation)],
                'The average height of the station' : average, 
                'The lower median station' : stateData[int(median1)],
                'The higher median station' : stateData[int(median2)],
                'Stations above sea level' : aboveSea ,
                'Stations above 2000 feet' : above2000,
                'Stations above 4000 feet' : above4000,
                'Stations above 6000 feet' : above6000
                })
            else:                           # Odd amount of data set
                median1 = count/2 
                                            # Construct the JSON object
                jData[stateDict[stateAbbrev]].append({
                'The maximum station' : stateData[int(maxLocation)],
                'The minimum station' : stateData[int(minLocation)],
                'The average height of the station' : average, 
                'The median station' : stateData[int(median1)],
                'Stations above sea level' : aboveSea ,
                'Stations above 2000 feet' : above2000,
                'Stations above 4000 feet' : above4000,
                'Stations above 6000 feet' : above6000
                })                    

                                            # output file
            with open('elevation_report_'+stateAbbrev+'.json', 'w') as write:
                json.dump(jData, write)
    except TypeError as e:
        print(e)

if __name__ == "__main__":
    main(stationCSV , stateAbbrev)