# %%
# for loop that checks every 1 min? for what prayer is next? 
# Constantly running clock that displays stuff
# extract prayer_data (individual date), according to date.
# extract which prayer is next, according to time
# set Iqamah timer - according to time
# if date not found, display XX:XX - UPDATE REQUIRED


# %%
import pandas as pd
import time
import datetime


# %%
def initializers(offset):
    currentUTC = time.gmtime()  # Get current time in UTC
    currentMYT = time.localtime(time.mktime(currentUTC) + offset * 3600)  # Add 8 hours for GMT+8

    df = pd.read_csv(r'C:\Users\Abdullah Usmani\Documents\MasjidClock\athan-plus-iqamah-time-clock\prayerTimes.csv')

    # Select only the relevant columns
    relevant_columns = ['Date', 'Hijri', 'Day', 'Imsak', 'Fajr', 'Syuruk', 'Zohor', 'Asar', 'Maghrib', 'Isyak']
    prayer_headers = ['Fajr', 'Syuruk', 'Zohor', 'Asar', 'Maghrib', 'Isyak']
    df = df[relevant_columns]

    return df, prayer_headers, currentMYT


# %%
def dateComparer(df, prayer_headers, currentMYT):
    currentDate = time.strftime('%d-%b-%Y', currentMYT)
    found = False
    for i in range (366): # got potential for error if not leap year
        rowDate = df.loc[i, 'Date']
        Hijri = df.loc[i, 'Hijri']
        Day = df.loc[i, 'Day']
        i += 1
        if rowDate == currentDate:
            found = True
            print(f"{rowDate} | {Hijri}")
            print(f"{Day}")
            for j in prayer_headers:
                print(f"{j} - {df.loc[i, f'{j}']}")
            selectedRow = i
            break

    if found == False:
        print("XX:XX - UPDATE REQUIRED")
        
    return selectedRow, rowDate, Hijri, Day, prayer_headers, found


# %%
def timeComparer(selectedRow, df, prayer_headers, currentMYT):
    currentTime = datetime.time(currentMYT.tm_hour, currentMYT.tm_min, currentMYT.tm_sec)
    displayCurrentTime = currentTime.strftime('%I:%M %p')  # Format current time as HH:MM:SS AM/PM
    
    # Create dictionaries to hold your times and display times
    act_time = {}
    display = {}

    for i in prayer_headers:
        # Store the values in dictionaries
        act_time[i] = datetime.datetime.strptime(df.loc[selectedRow, f'{i}'], '%I:%M %p').time()
        display[i] = datetime.datetime.strptime(df.loc[selectedRow, f'{i}'], '%I:%M %p').strftime('%I:%M %p')

    for i in range(len(prayer_headers)):  # Iterate over the prayer headers
        next = prayer_headers[i]
        curr = prayer_headers[i-1]
        if currentTime < act_time[next]:  # Compare current time with the actual time
            print(f"\nCurrent: {displayCurrentTime}")
            print(f"Next: {display[next]}")
            print(f"{curr} is now!")
            print(f"{next} is next!")
            break
        elif currentTime > act_time['Isyak']:
            print(f"\nCurrent: {displayCurrentTime}")
            print(f"{curr} is now!")
            print(f"Next: {display[next]}")
            print(f"Fajr is next!")
            break
    return currentTime, displayCurrentTime, act_time, display, curr, next

# %%
df, prayer_headers, currentMYT = initializers(8)
selectedRow, date, hijri, day, headers, foundFlag = dateComparer(df, prayer_headers, currentMYT)
currentTime, displayCurrentTime, act_times, display_times, current_prayer, next_prayer= timeComparer(selectedRow, df, prayer_headers, currentMYT)

print(selectedRow)
print(date)
print(hijri)
print(day)
print(headers)

print(currentTime)
print(displayCurrentTime)

# %%

    # fajrTime = datetime.datetime.strptime(df.loc[selectedRow, 'Fajr'], '%I:%M %p').time()
    # displayFajrTime = datetime.datetime.strptime(df.loc[selectedRow, 'Fajr'], '%I:%M %p').strftime('%I:%M %p')
    
    # syurukTime = datetime.datetime.strptime(df.loc[selectedRow, 'Syuruk'], '%I:%M %p').time()
    # displaySyurukTime = datetime.datetime.strptime(df.loc[selectedRow, 'Syuruk'], '%I:%M %p').strftime('%I:%M %p')
    
    # zohorTime = datetime.datetime.strptime(df.loc[selectedRow, 'Zohor'], '%I:%M %p').time()
    # displayZohorTime = datetime.datetime.strptime(df.loc[selectedRow, 'Zohor'], '%I:%M %p').strftime('%I:%M %p')
    
    # asarTime = datetime.datetime.strptime(df.loc[selectedRow, 'Asar'], '%I:%M %p').time()
    # displayAsarTime = datetime.datetime.strptime(df.loc[selectedRow, 'Asar'], '%I:%M %p').strftime('%I:%M %p')
    
    # maghribTime = datetime.datetime.strptime(df.loc[selectedRow, 'Maghrib'], '%I:%M %p').time()
    # displayMaghribTime = datetime.datetime.strptime(df.loc[selectedRow, 'Maghrib'], '%I:%M %p').strftime('%I:%M %p')
    
    # isyakTime = datetime.datetime.strptime(df.loc[selectedRow, 'Isyak'], '%I:%M %p').time()
    # displayIsyakTime = datetime.datetime.strptime(df.loc[selectedRow, 'Isyak'], '%I:%M %p').strftime('%I:%M %p')
    # if currentTime < syurukTime:
    #     print(f"{displayCurrentTime} vs {displaySyurukTime}")
    #     print("FAJR RIGHT NOW!")
    # elif currentTime < zohorTime:
    #     print(f"{displayCurrentTime} vs {displayZohorTime}")
    #     print("NOTHING RIGHT NOW")

    # elif currentTime < asarTime:
    #     print(f"{displayCurrentTime} vs {displayAsarTime}")
    #     print("ZOHOR RIGHT NOW")

    # elif currentTime < maghribTime:
    #     print(f"{displayCurrentTime} vs {displayMaghribTime}")
    #     print("ASAR RIGHT NOW")

    # elif currentTime < isyakTime:
    #     print(f"{displayCurrentTime} vs {displayIsyakTime}")
    #     print("MAGHRIB RIGHT NOW")

    # elif currentTime < fajrTime:
    #     print(f"{displayCurrentTime} vs {displayFajrTime}")
    #     print("ISYAK RIGHT NOW")
        

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


