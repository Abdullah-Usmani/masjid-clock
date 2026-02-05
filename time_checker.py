import pandas as pd
import time
from datetime import datetime, timedelta, timezone
import os

def process_prayer_data(file_path='./prayerTimes.csv'):
    """
    Processes the entire CSV once at startup. 
    Calculates Midnight, Hijri formatting, and translations for all 365 days.
    """
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return {}

    df = pd.read_csv(file_path)

    # Standardize column names from the Malay source
    prayer_mapping = {
        'Syuruk': 'Sunrise', 
        'Zohor': 'Dhuhr', 
        'Asar': 'Asr', 
        'Isyak': 'Isha'
    }
    df.rename(columns=prayer_mapping, inplace=True, errors='ignore')

    # Localization Mappings
    day_en = {
        'Isnin': 'Monday', 'Selasa': 'Tuesday', 'Rabu': 'Wednesday', 
        'Khamis': 'Thursday', 'Jumaat': 'Friday', 'Sabtu': 'Saturday', 'Ahad': 'Sunday'
    }
    day_ar = {
        'Isnin': 'الإثنين', 'Selasa': 'الثلاثاء', 'Rabu': 'الأربعاء', 
        'Khamis': 'الخميس', 'Jumaat': 'الجمعة', 'Sabtu': 'السبت', 'Ahad': 'الأحد'
    }
    month_ar = {
        'Muh': 'محرم', 'Saf': 'صفر', 'Raw': 'الأول ربيع', 'Rak': 'الآخر ربيع', 
        'Jaw': 'الأولى جمادى', 'Jak': 'الآخرة جمادى', 'Rej': 'رجب', 'Syb': 'شعبان', 
        'Ram': 'رمضان', 'Syw': 'شوال', 'Zkh': 'القعدة ذي', 'Zhj': 'الحجة ذي'
    }
    
    # Windows-friendly zero-padding remover
    # Use '#' for Windows, '-' for Linux (Raspberry Pi)
    fmt_prefix = '#' if os.name == 'nt' else '-'

    arabic_num_map = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
    headers = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
    iqama_delays = {'Fajr': 25, 'Sunrise': 0, 'Dhuhr': 15, 'Asr': 15, 'Maghrib': 10, 'Isha': 15}

    processed_data = {}

    for _, row in df.iterrows():
        date_key = row['Date']
        
        # 1. Parse Times & Calculate Midnight
        fajr_dt = datetime.strptime(row['Fajr'], "%I:%M %p")
        maghrib_dt = datetime.strptime(row['Maghrib'], "%I:%M %p")
        
        # Duration between Maghrib and Fajr (Fajr is effectively next day)
        diff_seconds = (fajr_dt + timedelta(hours=12) - maghrib_dt).total_seconds()
        midnight_dt = maghrib_dt + timedelta(seconds=diff_seconds / 2)
        midnight_time_obj = midnight_dt.time()

        # 2. Format Hijri String
        h_parts = row['Hijri'].split('-')
        if len(h_parts) == 3:
            h_day = h_parts[0].lstrip("0").translate(arabic_num_map)
            h_month = month_ar.get(h_parts[1], h_parts[1])
            h_year = h_parts[2].translate(arabic_num_map)
            formatted_hijri = f"{h_day}  {h_month}  {h_year}"
        else:
            formatted_hijri = row['Hijri']

        # 3. Build Prayer Time Objects & Display Strings
        day_times = {}
        day_display = {}
        for h in headers:
            actual_dt = datetime.strptime(row[h], "%I:%M %p")
            
            # Isha Ramadan Override
            if "Ram" in row['Hijri'] and h == 'Isha':
                iqama_dt = datetime.strptime("9:15 PM", "%I:%M %p")
            else:
                iqama_dt = actual_dt + timedelta(minutes=iqama_delays.get(h, 0))

            day_times[h] = actual_dt.time()
            day_times[f"{h}_iqama"] = iqama_dt.time()
            
            # Use dynamic prefix based on OS
            day_display[h] = actual_dt.strftime(f"%{fmt_prefix}I:%M %p")
            day_display[f"{h}_iqama"] = iqama_dt.strftime(f"%{fmt_prefix}I:%M %p")

        # 4. Save to dictionary
        processed_data[date_key] = {
            'Display_Date': datetime.strptime(date_key, "%d-%b-%Y").strftime("%d %B %Y"),
            'Hijri': formatted_hijri,
            'Day_En': day_en.get(row['Day'], row['Day']),
            'Day_Ar': day_ar.get(row['Day'], row['Day']),
            'Midnight': midnight_time_obj,
            'Midnight_Disp': midnight_dt.strftime(f"%{fmt_prefix}I:%M %p"),
            'Times': day_times,
            'Display': day_display
        }

    return processed_data

def time_comparer(offset):
    now_utc = datetime.now(timezone.utc)
    now_myt = now_utc + timedelta(hours=offset)
    
    # Prefix check for the clock display as well
    fmt_prefix = '#' if os.name == 'nt' else '-'
    
    return (
        now_myt.time(),
        now_myt.strftime(f"%{fmt_prefix}I:%M"),
        now_myt.strftime("%S"),
        now_myt.strftime("%p")
    )