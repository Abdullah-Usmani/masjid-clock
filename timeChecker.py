import pandas as pd
import time
from datetime import datetime, timedelta

def midnight(time_str1, time_str2, hours_to_add=12):
    # Define the input time format
    input_format = "%I:%M %p"
    
    # Function to convert a single time string to hh:mm format
    def convert_time(time_str):
        # Parse the time string into a datetime object
        time_obj = datetime.strptime(time_str, input_format)
        # Format the datetime object into the desired output format
        return time_obj.strftime("%I:%M").lstrip("0").replace(" 0", " ")
    
    # Function to convert a time object to HH:MM am/pm format
    def format_to_am_pm(time_obj):
        # Convert the datetime object to 12-hour format with AM/PM
        return time_obj.strftime("%I:%M %p").lstrip("0").replace(" 0", " ")

    # Convert both time strings
    pure_time1 = convert_time(time_str1)
    pure_time2 = convert_time(time_str2)
    
    # Convert pure_time1 back to a datetime object to add hours
    pure_time1_obj = datetime.strptime(pure_time1, "%I:%M")
    pure_time1_obj += timedelta(hours=hours_to_add)
    
    # Convert the second time string to a datetime object
    pure_time2_obj = datetime.strptime(pure_time2, "%I:%M")
    
    # Calculate the difference in minutes
    time_difference = (pure_time1_obj - pure_time2_obj).total_seconds() / 60
    
    # Halve the difference
    half_difference = time_difference / 2
    
    # Add the half difference to the second time
    adjusted_time2_obj = pure_time2_obj + timedelta(minutes=half_difference)
    
    # Add 12 hours to flip AM/PM
    adjusted_time2_obj += timedelta(hours=12)
    
    # Format the adjusted second time to HH:MM am/pm format
    adjusted_time2 = format_to_am_pm(adjusted_time2_obj)
    
    return adjusted_time2

def initializers():
    df = pd.read_csv(r'C:\Users\Abdullah Usmani\Documents\MasjidClock\athan-plus-iqamah-time-clock\prayerTimes.csv')

    # Select only the relevant columns
    relevant_columns = ['Date', 'Hijri', 'Day', 'Imsak', 'Fajr', 'Syuruk', 'Zohor', 'Asar', 'Maghrib', 'Isyak', 'Midnight']
    prayer_headers = ['Fajr', 'Syuruk', 'Zohor', 'Asar', 'Maghrib', 'Isyak', 'Midnight']
    prayer_headers_ar = ['فجر', 'شروق', 'ظهر', 'عصر', 'مغرب', 'عشاء', 'الليل نصف']
    iqama_headers = [25, 0, 15, 15, 10, 15, 0]

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

    # Apply the midnight function to each row
    df['Midnight'] = df.apply(lambda row: midnight(row['Fajr'], row['Maghrib']), axis=1)

    df = df[relevant_columns]
    return df, prayer_headers, prayer_headers_ar, iqama_headers


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
            selectedRow = i
            break

    if not found:
        print("XX:XX - UPDATE REQUIRED")
        
    return selectedRow, rowDate, Hijri, Day, prayer_headers, found

def timeComparer(selectedRow, df, prayer_headers, iqama_headers, offset):
    currentUTC = time.gmtime()  # Get current time in UTC
    currentMYT = time.localtime(time.mktime(currentUTC) + offset * 3600)  # Add 8 hours for GMT+8
    
    # Create a datetime object for the current time
    currentTime = datetime(currentMYT.tm_year, currentMYT.tm_mon, currentMYT.tm_mday, currentMYT.tm_hour, currentMYT.tm_min, currentMYT.tm_sec).time()
    
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
        act_time[i] = datetime.strptime(df.loc[selectedRow, f'{i}'], '%I:%M %p').time()
        iqama_time[i] = (datetime.combine(datetime.min, act_time[i]) + timedelta(minutes=iqama_headers[j])).time()
        display_act_time[i] = f"{int(act_time[i].strftime('%I'))}:{act_time[i].strftime('%M %p')}"
        display_iqama_time[i] = f"{int(iqama_time[i].strftime('%I'))}:{iqama_time[i].strftime('%M %p')}"


    for i in range(len(prayer_headers)):  # Iterate over the prayer headers
        next = prayer_headers[i]
        curr = prayer_headers[i-1]
        if currentTime < act_time[next]:  # Compare current time with the actual time
            break
        elif currentTime > act_time['Isyak']:
            break
    return currentTime, displayCurrentTime, act_time, iqama_time, display_act_time, display_iqama_time, curr, next

# # Run initializers and dateComparer as needed
# df, prayer_headers, prayer_headers_ar, iqama_headers = initializers()
# selectedRow, date, hijri, day, headers, foundFlag = dateComparer(df, prayer_headers, 8)
# currentTime, displayCurrentTime, act_times, iqama_times, display_act_times, display_iqama_times, current_prayer, next_prayer = timeComparer(selectedRow, df, prayer_headers, iqama_headers, 8)
