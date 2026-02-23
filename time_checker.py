import pandas as pd
from datetime import datetime, timedelta, timezone
import os

def midnight_original(time_str1, time_str2, hours_to_add=12):
    """Your original logic for calculating the midnight midpoint."""
    input_format = "%I:%M %p"
    
    def convert_time(time_str):
        time_obj = datetime.strptime(time_str, input_format)
        return time_obj.strftime("%I:%M").lstrip("0").replace(" 0", " ")
    
    def format_to_am_pm(time_obj):
        return time_obj.strftime("%I:%M %p").lstrip("0").replace(" 0", " ")

    pure_time1 = convert_time(time_str1)
    pure_time2 = convert_time(time_str2)
    
    pure_time1_obj = datetime.strptime(pure_time1, "%I:%M")
    pure_time1_obj += timedelta(hours=hours_to_add)
    
    pure_time2_obj = datetime.strptime(pure_time2, "%I:%M")
    time_difference = (pure_time1_obj - pure_time2_obj).total_seconds() / 60
    half_difference = time_difference / 2
    
    adjusted_time2_obj = pure_time2_obj + timedelta(minutes=half_difference)
    adjusted_time2_obj += timedelta(hours=12)
    
    return format_to_am_pm(adjusted_time2_obj)

def process_prayer_data(file_path='./prayerTimes.csv'):
    if not os.path.exists(file_path):
        return {}

    df = pd.read_csv(file_path)
    prayer_mapping = {'Syuruk': 'Sunrise', 'Zohor': 'Dhuhr', 'Asar': 'Asr', 'Isyak': 'Isha'}
    df.rename(columns=prayer_mapping, inplace=True, errors='ignore')

    day_en = {'Isnin': 'Monday', 'Selasa': 'Tuesday', 'Rabu': 'Wednesday', 'Khamis': 'Thursday', 'Jumaat': 'Friday', 'Sabtu': 'Saturday', 'Ahad': 'Sunday'}
    month_ar = {'Muh': 'محرم', 'Saf': 'صفر', 'Raw': 'الأول ربيع', 'Rak': 'الآخر ربيع', 'Jaw': 'الأولى جمادى', 'Jak': 'الآخرة جمادى', 'Rej': 'رجب', 'Syb': 'شعبان', 'Ram': 'رمضان', 'Syw': 'شوال', 'Zkh': 'القعدة ذي', 'Zhj': 'الحجة ذي'}
    arabic_num_map = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
    
    fmt_prefix = '#' if os.name == 'nt' else '-'
    headers = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
    iqama_delays = {'Fajr': 25, 'Sunrise': 0, 'Dhuhr': 15, 'Asr': 15, 'Maghrib': 10, 'Isha': 15}

    processed_data = {}

    for _, row in df.iterrows():
        date_key = row['Date']
        
        # Calculate Midnight using original logic
        m_disp = midnight_original(row['Fajr'], row['Maghrib'])
        m_obj = datetime.strptime(m_disp, "%I:%M %p").time()
        
        # Format Hijri
        h_parts = row['Hijri'].split('-')
        formatted_hijri = f"{h_parts[0].lstrip('0').translate(arabic_num_map)}  {month_ar.get(h_parts[1], h_parts[1])}  {h_parts[2].translate(arabic_num_map)}" if len(h_parts) == 3 else row['Hijri']

        day_times, day_display = {}, {}
        for h in headers:
            actual_dt = datetime.strptime(row[h], "%I:%M %p")
            iqama_dt = datetime.strptime("9:15 PM", "%I:%M %p") if ("Ram" in row['Hijri'] and h == 'Isha') else (actual_dt + timedelta(minutes=iqama_delays.get(h, 0)))
            
            day_times[h] = actual_dt.time()
            day_times[f"{h}_iqama"] = iqama_dt.time()
            day_display[h] = actual_dt.strftime(f"%{fmt_prefix}I:%M %p").lstrip("0")
            day_display[f"{h}_iqama"] = iqama_dt.strftime(f"%{fmt_prefix}I:%M %p").lstrip("0")

        processed_data[date_key] = {
            'Display_Date': datetime.strptime(date_key, "%d-%b-%Y").strftime("%d %B %Y"),
            'Hijri': formatted_hijri,
            'Day_En': day_en.get(row['Day'], row['Day']),
            'Midnight': m_obj,
            'Midnight_Disp': m_disp,
            'Times': day_times,
            'Display': day_display
        }
    return processed_data

def time_comparer(offset):
    now_myt = datetime.now(timezone.utc) + timedelta(hours=offset)
    fmt_prefix = '#' if os.name == 'nt' else '-'
    return now_myt.time(), now_myt.strftime(f"%{fmt_prefix}I:%M").lstrip("0"), now_myt.strftime("%S"), now_myt.strftime("%p")