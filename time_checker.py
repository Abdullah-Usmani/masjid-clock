import pandas as pd
import time
from datetime import datetime, timedelta, timezone
import os

def process_prayer_data(file_path='./prayerTimes.csv'):
    if not os.path.exists(file_path):
        return {}

    df = pd.read_csv(file_path)
    prayer_mapping = {'Syuruk': 'Sunrise', 'Zohor': 'Dhuhr', 'Asar': 'Asr', 'Isyak': 'Isha'}
    df.rename(columns=prayer_mapping, inplace=True, errors='ignore')

    day_en = {'Isnin': 'Monday', 'Selasa': 'Tuesday', 'Rabu': 'Wednesday', 'Khamis': 'Thursday', 'Jumaat': 'Friday', 'Sabtu': 'Saturday', 'Ahad': 'Sunday'}
    day_ar = {'Isnin': 'الإثنين', 'Selasa': 'الثلاثاء', 'Rabu': 'الأربعاء', 'Khamis': 'الخميس', 'Jumaat': 'الجمعة', 'Sabtu': 'السبت', 'Ahad': 'الأحد'}
    month_ar = {'Muh': 'محرم', 'Saf': 'صفر', 'Raw': 'الأول ربيع', 'Rak': 'الآخر ربيع', 'Jaw': 'الأولى جمادى', 'Jak': 'الآخرة جمادى', 'Rej': 'رجب', 'Syb': 'شعبان', 'Ram': 'رمضان', 'Syw': 'شوال', 'Zkh': 'القعدة ذي', 'Zhj': 'الحجة ذي'}
    
    fmt_prefix = '#' if os.name == 'nt' else '-'
    arabic_num_map = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
    headers = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
    iqama_delays = {'Fajr': 25, 'Sunrise': 0, 'Dhuhr': 15, 'Asr': 15, 'Maghrib': 10, 'Isha': 15}

    processed_data = {}

    for _, row in df.iterrows():
        date_key = row['Date']
        
        # Parse Times
        fajr_dt = datetime.strptime(row['Fajr'], "%I:%M %p")
        maghrib_dt = datetime.strptime(row['Maghrib'], "%I:%M %p")
        
        # FIXED MIDNIGHT LOGIC:
        # Midnight is roughly half-way between Maghrib (PM) and Fajr (AM next day)
        # We treat Fajr as being 12 hours ahead for the calculation
        total_night_seconds = (fajr_dt + timedelta(hours=12) - maghrib_dt).total_seconds()
        midnight_dt = maghrib_dt + timedelta(seconds=total_night_seconds / 2)
        
        # Format Hijri
        h_parts = row['Hijri'].split('-')
        formatted_hijri = f"{h_parts[0].lstrip('0').translate(arabic_num_map)}  {month_ar.get(h_parts[1], h_parts[1])}  {h_parts[2].translate(arabic_num_map)}" if len(h_parts) == 3 else row['Hijri']

        day_times, day_display = {}, {}
        for h in headers:
            actual_dt = datetime.strptime(row[h], "%I:%M %p")
            iqama_dt = datetime.strptime("9:15 PM", "%I:%M %p") if ("Ram" in row['Hijri'] and h == 'Isha') else (actual_dt + timedelta(minutes=iqama_delays.get(h, 0)))
            
            day_times[h] = actual_dt.time()
            day_times[f"{h}_iqama"] = iqama_dt.time()
            day_display[h] = actual_dt.strftime(f"%{fmt_prefix}I:%M %p")
            day_display[f"{h}_iqama"] = iqama_dt.strftime(f"%{fmt_prefix}I:%M %p")

        processed_data[date_key] = {
            'Display_Date': datetime.strptime(date_key, "%d-%b-%Y").strftime("%d %B %Y"),
            'Hijri': formatted_hijri,
            'Day_En': day_en.get(row['Day'], row['Day']),
            'Day_Ar': day_ar.get(row['Day'], row['Day']),
            'Midnight': midnight_dt.time(),
            'Midnight_Disp': midnight_dt.strftime(f"%{fmt_prefix}I:%M %p"), # Correctly formats as AM
            'Times': day_times,
            'Display': day_display
        }
    return processed_data

def time_comparer(offset):
    now_myt = datetime.now(timezone.utc) + timedelta(hours=offset)
    fmt_prefix = '#' if os.name == 'nt' else '-'
    return now_myt.time(), now_myt.strftime(f"%{fmt_prefix}I:%M"), now_myt.strftime("%S"), now_myt.strftime("%p")