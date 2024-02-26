# for loop that checks every 1 min? for what prayer is next? 
# Constantly running clock that displays stuff
# extract prayer_data (individual date), according to date.
# extract which prayer is next, according to time
# set Iqamah timer - according to time
# if date not found, display XX:XX - UPDATE REQUIRED

import pandas
import time
import datetime

dataFrame = pandas.read_csv(r'C:\Users\Abdullah Usmani\Documents\MasjidClock\athan-plus-iqamah-time-clock\prayerTimes.csv')

# Select only the relevant columns
relevant_columns = ['Date', 'Hijri', 'Day', 'Imsak', 'Fajr', 'Syuruk', 'Zohor', 'Asar', 'Maghrib', 'Isyak']
dataFrame = dataFrame[relevant_columns]

selectedRow = 0

currentTimeUTC = time.gmtime()  # Get current time in UTC
currentTimeMYT = time.localtime(time.mktime(currentTimeUTC) + 8 * 3600)  # Add 8 hours for GMT+8

def dateComparer():
    currentDate = time.strftime('%d-%b-%y', currentTimeMYT)
    for i in range (366):
        rowDate = dataFrame.loc[i, 'Date']
        i += 1
        if rowDate == currentDate:
            print(f"VOILA!\n - MATCH!, this is at row # {i}, the row's date is {rowDate}")
            selectedRow == i
            break

dateComparer()

def timeComparer():
    currentTime = time.strftime('%d-%b-%y', currentTimeMYT)
    if currentTime < columnTime:
        print("FAJR RIGHT NOW!")


        # parsedRowDate = time.strptime(f'{rowDate}', '%d-%b-%y')
# def constantClock():
#     while True:
#       currentTimeUTC = time.gmtime()  # Get current time in UTC
#       currentTimeMYT = time.localtime(time.mktime(currentTimeUTC) + 8 * 3600)  # Add 8 hours for GMT+8
#       time.sleep(5)
# constantClock()
    # print(currentRowData.to_dict()) <--- this line would make all the rows appear as a dict if we were to include all columns, more readable
    # if rowDate == CurrentDate:
    #     selectedRow = i
    #     break

# if currentTime == (before)row.Date.Syuruk, print("FAJR + RIGHT NOW")
# else if currentTime == (before)row.Date.Dhuhr, print("NOTHING + RIGHT NOW")
# else if currentTime == (before)row.Date.Asr, print("DHUHR + RIGHT NOW")
# else if currentTime == (before)row.Date.Maghrib, print("ASR + RIGHT NOW")
# else if currentTime == (before)row.Date.Isyak, print("MAGHRIB + RIGHT NOW")
# else if currentTime == (before)row.Date.Fajr, print("ISYAK + RIGHT NOW")

# for every 5 seconds, print("Current Time - XX:XX Z") # CLOCK CONSTANTLY RUNNING