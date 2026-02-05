import tkinter as tk
from PIL import Image
import customtkinter as ctk
from datetime import datetime, timedelta, timezone
import arabic_reshaper
from bidi.algorithm import get_display

# Import the optimized logic from your updated time_checker.py
from time_checker import process_prayer_data, time_comparer

# 1. INITIALIZATION (Happens once at startup)
# This processes the CSV into a dictionary for O(1) lookups throughout the year
PRAYER_DATABASE = process_prayer_data('./prayerTimes.csv')
CURRENT_DAY_DATA = None
OFFSET = 8  # GMT+8

# UI Constants
LIGHT = "#f2f4f5"
DARK = "#212121"
GOLD = "#946d2e"

# Caching for performance
previous_values = {}
previous_highlight = None

def get_ms_until_midnight():
    """Calculates time remaining until the next day starts in Malaysia."""
    now = datetime.now(timezone.utc) + timedelta(hours=OFFSET)
    tomorrow = datetime.combine(now.date() + timedelta(days=1), datetime.min.time(), tzinfo=now.tzinfo)
    return int((tomorrow - now).total_seconds() * 1000)

def refresh_daily_data():
    """Updates the CURRENT_DAY_DATA context. No loops required."""
    global CURRENT_DAY_DATA
    now = datetime.now(timezone.utc) + timedelta(hours=OFFSET)
    today_str = now.strftime('%d-%b-%Y')
    
    # Direct dictionary lookup instead of 365-row loop
    CURRENT_DAY_DATA = PRAYER_DATABASE.get(today_str)
    
    if not CURRENT_DAY_DATA:
        print(f"XX:XX - DATA MISSING FOR {today_str}")
    
    # Schedule next refresh for exactly midnight
    root.after(get_ms_until_midnight(), refresh_daily_data)

# 2. UI SETUP
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title("Prayer Times - ISOC 24/25")
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

main_frame = ctk.CTkFrame(master=root, fg_color=(LIGHT, DARK))
main_frame.pack(padx=10, pady=10, fill='both', expand=True)

# Layout Frames
info_frame = ctk.CTkFrame(master=main_frame, fg_color=(LIGHT, DARK))
info_frame.place(x=0, y=0, relwidth=1, relheight=0.45)

prayer_frame = ctk.CTkFrame(master=main_frame, fg_color=(LIGHT, DARK))
prayer_frame.place(x=0, rely=0.45, relwidth=1, relheight=.55)

rows_frame = ctk.CTkFrame(master=prayer_frame, fg_color=(LIGHT, DARK))
rows_frame.pack(fill='both', expand=True, ipady=30, ipadx=50)
rows_frame.columnconfigure((0, 2), weight=2, uniform='a')
rows_frame.columnconfigure(1, weight=1, uniform='a')

# State Variables
toggle_state = False
notice_text = "unmisoc.com"

# 3. HELPER FUNCTIONS
def update_label_cached(widget, key, new_value):
    """Only updates the widget if the text has actually changed."""
    if previous_values.get(key) != new_value:
        widget.configure(text=new_value)
        previous_values[key] = new_value

def status_toggle():
    global toggle_state
    toggle_state = not toggle_state
    root.after(5000, status_toggle)

def update_highlights(currentTime):
    global previous_highlight
    if not CURRENT_DAY_DATA: return

    times = CURRENT_DAY_DATA['Times']
    midnight_time = CURRENT_DAY_DATA['Midnight'] # Get Midnight from the top level
    # Sequence of prayer keys in order of the day
    prayer_keys = ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
    grid_map = {0: 0, 1: 2, 2: 3, 3: 4, 4: 5} # Map prayer list to row indices

    highlight_index = None

    if currentTime < midnight_time:
        highlight_index = 5 # Highlight Isha    elif currentTime > times['Isha']:
        highlight_index = 5
    elif currentTime < times['Fajr']:
        highlight_index = None
    else:
        # Loop through to find the active prayer slot
        for i, key in enumerate(prayer_keys):
            if currentTime < times[key]:
                highlight_index = grid_map.get(i-1)
                break
    
    if highlight_index == previous_highlight:
        return

    # Reset old highlight
    if previous_highlight is not None:
        prayer_labels[previous_highlight].configure(font=("Roboto", 50), fg_color="transparent", text_color=("black", "white"))
        act_time_labels[previous_highlight].configure(font=("Roboto", 80), fg_color="transparent", text_color=("black", "white"))
        iqama_time_labels[previous_highlight].configure(font=("Roboto", 80), fg_color="transparent", text_color=("black", "white"))

    # Apply new highlight
    if highlight_index is not None:
        prayer_labels[highlight_index].configure(font=("Roboto", 50, "bold"), fg_color=GOLD, text_color="white")
        act_time_labels[highlight_index].configure(font=("Roboto", 80, "bold"), fg_color=GOLD, text_color="white")
        iqama_time_labels[highlight_index].configure(font=("Roboto", 80, "bold"), fg_color=GOLD, text_color="white")

    previous_highlight = highlight_index

def update_display():
    if not CURRENT_DAY_DATA: 
        root.after(1000, update_display)
        return

    # 1. Get current time values (O(1) from helper)
    currentTime, dispTime, dispSec, dispMeridian = time_comparer(OFFSET)
    
    # 2. Update Notice
    update_label_cached(notice, "notice", notice_text)

    # 3. Handle Language Toggle Logic
    if toggle_state:
        date_display = CURRENT_DAY_DATA['Display_Date']
        day_display = CURRENT_DAY_DATA['Day_En']
        headers = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
        adhan_txt, iqama_txt = "Adhan", "Iqamah"
    else:
        # Arabic bidi/reshaper logic
        date_display = get_display(arabic_reshaper.reshape(CURRENT_DAY_DATA['Hijri']))
        day_display = CURRENT_DAY_DATA['Day_Ar']
        headers = ['فجر', 'شروق', 'ظهر', 'عصر', 'مغرب', 'عشاء']
        adhan_txt, iqama_txt = "أذان", "إقامة"

    # 4. Update Header Labels
    update_label_cached(date_label, "date", date_display)
    update_label_cached(day_label, "day", day_display)
    update_label_cached(adhan_label, "adhan_hdr", adhan_txt)
    update_label_cached(iqamah_label, "iqama_hdr", iqama_txt)

    # 5. Update Clock
    update_label_cached(currenttime_labels[0], "clock_m", dispTime)
    update_label_cached(currenttime_labels[1], "clock_s", dispSec)
    update_label_cached(currenttime_labels[2], "clock_mer", dispMeridian)

    # 6. Update Prayer Row Content
    raw_keys = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
    for i in [0, 2, 3, 4, 5]:
        key = raw_keys[i]
        update_label_cached(prayer_labels[i], f"p_name_{i}", headers[i])
        update_label_cached(act_time_labels[i], f"p_act_{i}", CURRENT_DAY_DATA['Display'][key])
        update_label_cached(iqama_time_labels[i], f"p_iqama_{i}", CURRENT_DAY_DATA['Display'][f"{key}_iqama"])

    # 7. Update Footer / Status
    update_label_cached(status_labels[0], "stat_0", CURRENT_DAY_DATA['Display']['Sunrise'])
    update_label_cached(status_labels[1], "stat_1", f"{headers[1]} | {headers[5]}") # Sunrise | Isha
    update_label_cached(status_labels[2], "stat_2", CURRENT_DAY_DATA['Midnight_Disp'])

    # 8. Manage Highlights
    update_highlights(currentTime)

    root.update_idletasks()
    root.after(100, update_display)

# 4. UI BUILDING (Labels & Widgets)
my_image = ctk.CTkImage(light_image=Image.open("Images/ISoc (black).png"),
                        dark_image=Image.open("Images/ISoc (white).png"),
                        size=(100, 50))
ctk.CTkLabel(info_frame, image=my_image, text="").pack(expand=True, pady=(20, 10))

date_label = ctk.CTkLabel(master=info_frame, font=("Roboto", 60))
date_label.pack(expand=True)

day_label = ctk.CTkLabel(master=info_frame, font=("Roboto", 48))
day_label.pack(expand=True, ipady=10)

# Time Frame
time_frame = ctk.CTkFrame(master=info_frame, fg_color="transparent")
time_frame.pack(pady=10)
currenttime_labels = {
    0: ctk.CTkLabel(time_frame, font=("Roboto", 150, "bold")),
    1: ctk.CTkLabel(time_frame, font=("Roboto", 50, "bold")),
    2: ctk.CTkLabel(time_frame, font=("Roboto", 50, "normal"))
}
currenttime_labels[0].grid(row=0, column=0, padx=10)
currenttime_labels[1].grid(row=0, column=1, sticky='n', pady=20)
currenttime_labels[2].grid(row=0, column=1, sticky='s', pady=20)

# Notice
notice = ctk.CTkLabel(info_frame, font=("Roboto", 40, "bold"), text_color=GOLD)
notice.pack(pady=10)

# Prayer Grid Labels
adhan_label = ctk.CTkLabel(rows_frame)
adhan_label.grid(row=0, column=0, sticky="nsew")
iqamah_label = ctk.CTkLabel(rows_frame)
iqamah_label.grid(row=0, column=2, sticky="nsew")

prayer_labels = {}
act_time_labels = {}
iqama_time_labels = {}
status_labels = {}

row_idx = 1
for i in range(6):
    if i == 1: continue # Skip Sunrise in main list
    
    act_time_labels[i] = ctk.CTkLabel(rows_frame, font=("Roboto", 80))
    act_time_labels[i].grid(row=row_idx, column=0, pady=6, sticky="nsew")
    
    prayer_labels[i] = ctk.CTkLabel(rows_frame, font=("Roboto", 50))
    prayer_labels[i].grid(row=row_idx, column=1, pady=6, sticky="nsew")
    
    iqama_time_labels[i] = ctk.CTkLabel(rows_frame, font=("Roboto", 80))
    iqama_time_labels[i].grid(row=row_idx, column=2, pady=6, sticky="nsew")
    row_idx += 1

# Footer
for i in range(3):
    status_labels[i] = ctk.CTkLabel(rows_frame, font=("Roboto", 30), fg_color=("#969696", "#383838"))
    status_labels[i].grid(row=row_idx, column=i, pady=12, sticky="nsew")

# 5. LIFECYCLE START
refresh_daily_data()
status_toggle()
update_display()
root.mainloop()