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
def initializers():
    df = pd.read_csv(r'C:\Users\Abdullah Usmani\Documents\MasjidClock\athan-plus-iqamah-time-clock\prayerTimes.csv')

    # Select only the relevant columns
    relevant_columns = ['Date', 'Hijri', 'Day', 'Imsak', 'Fajr', 'Syuruk', 'Zohor', 'Asar', 'Maghrib', 'Isyak']
    prayer_headers = ['Fajr', 'Syuruk', 'Zohor', 'Asar', 'Maghrib', 'Isyak']
    iqama_headers = [25, 0, 15, 15, 10, 15]

    # Replace the values in the 'Day' column
    day_mapping = {
        'Isnin': 'Monday',
        'Selasa': 'Tuesday',
        'Rabu': 'Wednesday',
        'Khamis': 'Thursday',
        'Jumaat': 'Friday',
        'Sabtu': 'Saturday',
        'Ahad': 'Sunday'
    }
    df['Day'] = df['Day'].replace(day_mapping)

    df = df[relevant_columns]

    return df, prayer_headers, iqama_headers


# %%
def dateComparer(df, prayer_headers, offset):
    currentUTC = time.gmtime()  # Get current time in UTC
    currentMYT = time.localtime(time.mktime(currentUTC) + offset * 3600)  # Add 8 hours for GMT+8
    currentDate = time.strftime('%d-%b-%Y', currentMYT)
    found = False
    for i in range (366): # got potential for error if not leap year
        rowDate = df.loc[i, 'Date']
        Hijri = df.loc[i, 'Hijri']
        Day = df.loc[i, 'Day']
        i += 1
        if rowDate == currentDate:
            found = True
            # print(f"{rowDate} | {Hijri}")
            # print(f"{Day}")
            # for j in prayer_headers:
                # print(f"{j} - {df.loc[i, f'{j}']}")
            selectedRow = i
            break

    if found == False:
        print("XX:XX - UPDATE REQUIRED")
        
    return selectedRow, rowDate, Hijri, Day, prayer_headers, found


# %%
def timeComparer(selectedRow, df, prayer_headers, iqama_headers, offset):
    currentUTC = time.gmtime()  # Get current time in UTC
    currentMYT = time.localtime(time.mktime(currentUTC) + offset * 3600)  # Add 8 hours for GMT+8
    currentTime = datetime.time(currentMYT.tm_hour, currentMYT.tm_min, currentMYT.tm_sec)
    
    
    # Format current time manually to avoid platform-specific issues
    hour = currentMYT.tm_hour
    if hour > 12:
        hour -= 12  # Convert to 12-hour format
    elif hour == 0:
        hour = 12  # Handle midnight as 12 AM

    displayCurrentTime = f"{hour}:{currentMYT.tm_min:02}:{currentMYT.tm_sec:02} {'AM' if currentMYT.tm_hour < 12 else 'PM'}"
    
    # Create dictionaries to hold your times and display times
    act_time = {}
    iqama_time = {}
    display_act_time = {}
    display_iqama_time = {}

    for j, i in enumerate(prayer_headers):
        # Store the values in dictionaries
        act_time[i] = datetime.datetime.strptime(df.loc[selectedRow, f'{i}'], '%I:%M %p')
        iqama_time[i] = (act_time[i] + datetime.timedelta(minutes=iqama_headers[j])).time()
        act_time[i] = act_time[i].time()
        display_act_time[i] = f"{int(act_time[i].strftime('%I'))}:{act_time[i].strftime('%M %p')}"
        display_iqama_time[i] = f"{int(iqama_time[i].strftime('%I'))}:{iqama_time[i].strftime('%M %p')}"


    for i in range(len(prayer_headers)):  # Iterate over the prayer headers
        next = prayer_headers[i]
        curr = prayer_headers[i-1]
        if currentTime < act_time[next]:  # Compare current time with the actual time
            # print(f"\nCurrent: {displayCurrentTime}")
            # print(f"Next: {display[next]}")
            # print(f"{curr} is now!")
            # print(f"{next} is next!")
            break
        elif currentTime > act_time['Isyak']:
            # print(f"\nCurrent: {displayCurrentTime}")
            # print(f"{curr} is now!")
            # print(f"Next: {display[next]}")
            # print(f"Fajr is next!")
            break
    return currentTime, displayCurrentTime, act_time, iqama_time, display_act_time, display_iqama_time, curr, next

# %%
# df, prayer_headers, iqama_headers = initializers()
# selectedRow, date, hijri, day, headers, foundFlag = dateComparer(df, prayer_headers)
# currentTime, displayCurrentTime, act_times, iqama_times, display_act_times, display_iqama_times, current_prayer, next_prayer= timeComparer(selectedRow, df, prayer_headers, iqama_headers, 8)
