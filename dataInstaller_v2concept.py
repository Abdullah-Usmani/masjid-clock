import requests
import csv
from datetime import datetime

# URL for the e-solat API (Zone SGR01 - Gombak/Hulu Langat/etc)
url = "https://www.e-solat.gov.my/index.php?r=esolatApi/takwimsolat&period=year&zone=SGR01"

def format_time(time_str):
    """Converts '05:56:00' to '5:56 am'"""
    dt = datetime.strptime(time_str, "%H:%M:%S")
    formatted = dt.strftime("%I:%M %p").lower()
    # Remove leading zero for the hour
    if formatted.startswith('0'):
        formatted = formatted[1:]
    return formatted

def format_hijri(hijri_str):
    """Converts '1447-07-11' to '11-Rej-1447'"""
    month_mapping = {
        '01': 'Muh', '02': 'Saf', '03': 'Raw', '04': 'Rak',
        '05': 'Jaw', '06': 'Jak', '07': 'Rej', '08': 'Syb',
        '09': 'Ram', '10': 'Syw', '11': 'Zkh', '12': 'Zhj'
    }
    y, m, d = hijri_str.split('-')
    return f"{d}-{month_mapping[m]}-{y}"

response = requests.get(url)

if response.status_code == 200:
    raw_data = response.json()["prayerTime"]
    processed_data = []

    for row in raw_data:
        processed_row = {
            'Date': row['date'],
            'Hijri': format_hijri(row['hijri']),
            'Day': row['day'],
            'Imsak': format_time(row['imsak']),
            'Fajr': format_time(row['fajr']),
            'Syuruk': format_time(row['syuruk']),
            'Zohor': format_time(row['dhuhr']),
            'Asar': format_time(row['asr']),
            'Maghrib': format_time(row['maghrib']),
            'Isyak': format_time(row['isha'])
        }
        processed_data.append(processed_row)

    # Save to prayerTimes.csv using original headers
    fieldnames = ['Date', 'Hijri', 'Day', 'Imsak', 'Fajr', 'Syuruk', 'Zohor', 'Asar', 'Maghrib', 'Isyak']
    
    with open("prayerTimes.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(processed_data)

    print("Success: prayerTimes.csv generated with the correct format.")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")