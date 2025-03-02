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
    df = pd.read_csv('./prayerTimes.csv')

    # Select only the relevant columns
    relevant_columns = ['Date', 'Hijri', 'Day', 'Day_Arabic', 'Imsak', 'Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha', 'Midnight']
    prayer_headers_old = ['Fajr', 'Syuruk', 'Zohor', 'Asar', 'Maghrib', 'Isyak', 'Midnight']
    prayer_headers = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha', 'Midnight']
    prayer_headers_ar = ['فجر', 'شروق', 'ظهر', 'عصر', 'مغرب', 'عشاء', 'الليل منتصف']
    iqama_headers = [25, 0, 15, 15, 10, 15, 0]

    # Day mapping from Malay to English
    day_mapping = {
        'Isnin': 'Monday',
        'Selasa': 'Tuesday',
        'Rabu': 'Wednesday',
        'Khamis': 'Thursday',
        'Jumaat': 'Friday',
        'Sabtu': 'Saturday',
        'Ahad': 'Sunday'
    }

    # Day mapping from Malay to Arabic
    day_mapping_ar = {
        'Isnin': 'الإثنين',
        'Selasa': 'الثلاثاء',
        'Rabu': 'الأربعاء',
        'Khamis': 'الخميس',
        'Jumaat': 'الجمعة',
        'Sabtu': 'السبت',
        'Ahad': 'الأحد'
    }

    # Create a new column for Arabic day names
    df['Day_Arabic'] = df['Day'].replace(day_mapping_ar)

    # Replace values in 'Day' column with English day names
    df['Day'] = df['Day'].replace(day_mapping)


    # Create a mapping dictionary
    prayer_mapping = dict(zip(prayer_headers_old, prayer_headers))

    # Rename the columns in the DataFrame
    df.rename(columns=prayer_mapping, inplace=True)

    # Apply the midnight function to each row
    df['Midnight'] = df.apply(lambda row: midnight(row['Fajr'], row['Maghrib']), axis=1)

    df = df[relevant_columns]

    # print(df.describe())

    return df, prayer_headers, prayer_headers_ar, iqama_headers


def dateComparer(df, prayer_headers, iqama_headers, offset):

    # hijri_mapping_en = {
    #     'Muh': 'Muharram',
    #     'Saf': 'Safar',
    #     'Raw': 'Rabiul Awal',
    #     'Rak': 'Rabiul Akhir',
    #     'Jaw': 'Jumadil Ula',
    #     'Jak': 'Jumadil Akhira',
    #     'Rej': 'Rajab',
    #     'Syb': 'Shaban',
    #     'Ram': 'Ramadhan',
    #     'Syw': 'Shawwal',
    #     'Zkh': 'Dhul Qadah',
    #     'Zhj': 'Dhul Hijjah'
    # }

    hijri_mapping_ar = {
        'Muh': 'محرم',
        'Saf': 'صفر',
        'Raw': 'الأول ربيع',
        'Rak': 'الآخر ربيع',
        'Jaw': 'الأولى جمادى',
        'Jak': 'الآخرة جمادى',
        'Rej': 'رجب',
        'Syb': 'شعبان',
        'Ram': 'رمضان',
        'Syw': 'شوال',
        'Zkh': 'القعدة ذي',
        'Zhj': 'الحجة ذي'
    }

    arabic_numerals = {
        '0': '٠', '1': '١', '2': '٢', '3': '٣', '4': '٤',
        '5': '٥', '6': '٦', '7': '٧', '8': '٨', '9': '٩'
    }

    # Function to convert digits in a string to Arabic numerals
    def convert_to_arabic_numerals(date_str):
        return ''.join(arabic_numerals.get(char, char) for char in date_str)

    # Define a function to replace the month abbreviation and format the Hijri date
    def replace_hijri_month(hijri_date):
        parts = hijri_date.split('-')
        if len(parts) == 3:
            # Replace the second part (the month) with its full Arabic name
            parts[1] = hijri_mapping_ar.get(parts[1], parts[1])
            # Reorder to have day on the right and year on the left
            dayX = convert_to_arabic_numerals(parts[0].lstrip("0"))
            monthX = parts[1]
            yearX = convert_to_arabic_numerals(parts[2])

            formatted_hijri = f"{dayX}-{monthX}-{yearX}"

            return formatted_hijri
        return hijri_date

    currentUTC = time.gmtime()  # Get current time in UTC
    currentMYT = time.localtime(time.mktime(currentUTC) + offset * 3600)  # Add 8 hours for GMT+8
    currentDate = time.strftime('%d-%b-%Y', currentMYT)
    found = False
    selectedRow = None
    for i in range (365): # got potential for error if not leap year
        rowDate = df.loc[i, 'Date']
        Hijri = df.loc[i, 'Hijri']
        Day = df.loc[i, 'Day']
        Day_ar = df.loc[i, 'Day_Arabic']
        if rowDate == currentDate:
            found = True
            selectedRow = i
            break
    currentDate_dt = datetime.strptime(currentDate, "%d-%b-%Y")  # Convert back to datetime
    f_currentDate = currentDate_dt.strftime("%d-%B-%Y").lstrip("0")

    Hijri = replace_hijri_month(Hijri).replace('-', '  ')
    f_currentDate = f_currentDate.replace('-', ' ')


    if not found:
        print("XX:XX - UPDATE REQUIRED")
        return None, None, None, None, None, None, None, None, None, None, None
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

    # Special handling for Isha fixed delay in Ramadan
    iqama_time['Isha'] = datetime.strptime("9:15 PM", "%I:%M %p").time()
    display_iqama_time['Isha'] = f"{int(iqama_time['Isha'].strftime('%I'))}:{iqama_time['Isha'].strftime('%M %p')}"
        
    return selectedRow, f_currentDate, Hijri, Day, Day_ar, prayer_headers, found, act_time, iqama_time, display_act_time, display_iqama_time 

def timeComparer(offset):
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

    displayCurrentTime = f"{hour}:{currentMYT.tm_min:02}"
    displayCurrentTime_s = f"{currentMYT.tm_sec:02}"
    displayCurrentTime_meridian = f"{'AM' if currentMYT.tm_hour < 12 else 'PM'}"

    return currentTime, displayCurrentTime, displayCurrentTime_s, displayCurrentTime_meridian