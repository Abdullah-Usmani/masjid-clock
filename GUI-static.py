import tkinter as tk
from PIL import Image
import customtkinter as ctk
from datetime import datetime, timedelta, timezone
import arabic_reshaper
from bidi.algorithm import get_display
import os

# Importing optimized logic from time_checker.py
from time_checker import process_prayer_data, time_comparer

# --- 1. INITIALIZATION & DATA CACHING ---
OFFSET = 8  # GMT+8 for Malaysia
PRAYER_DATABASE = process_prayer_data('./prayerTimes.csv')
CURRENT_DAY_DATA = None

# UI Constants
GOLD = "#946d2e"
LIGHT = "#f2f4f5"
DARK = "#212121"

# Performance caching to prevent UI flickering
previous_values = {}
previous_highlight = None

def get_ms_until_midnight():
    """Calculates milliseconds until the next day to refresh data context."""
    now = datetime.now(timezone.utc) + timedelta(hours=OFFSET)
    tomorrow = datetime.combine(now.date() + timedelta(days=1), datetime.min.time(), tzinfo=now.tzinfo)
    return int((tomorrow - now).total_seconds() * 1000)

def refresh_daily_data():
    """Updates the CURRENT_DAY_DATA dictionary once a day."""
    global CURRENT_DAY_DATA
    now = datetime.now(timezone.utc) + timedelta(hours=OFFSET)
    today_str = now.strftime('%d-%b-%Y')
    CURRENT_DAY_DATA = PRAYER_DATABASE.get(today_str)
    
    if not CURRENT_DAY_DATA:
        print(f"CRITICAL: No prayer data found for {today_str}")
    
    # Schedule next refresh for exactly midnight
    root.after(get_ms_until_midnight(), refresh_daily_data)

# --- 2. UI SETUP ---
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title("Prayer Times - ISOC 24/25 (Static)")

# Resolution fixing for 1080x1920
root.geometry('1080x1920+1910+0') 
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

main_frame = ctk.CTkFrame(master=root, fg_color=(LIGHT, DARK))
main_frame.pack(padx=10, pady=10, fill='both', expand=True)

# Layout segments
info_frame = ctk.CTkFrame(master=main_frame, fg_color=(LIGHT, DARK))
info_frame.place(x=0, y=0, relwidth=1, relheight=0.45)

prayer_frame = ctk.CTkFrame(master=main_frame, fg_color=(LIGHT, DARK))
prayer_frame.place(x=0, rely=0.45, relwidth=1, relheight=.55)

rows_frame = ctk.CTkFrame(master=prayer_frame, fg_color=(LIGHT, DARK))
rows_frame.pack(fill='both', expand=True, ipady=30, ipadx=50)
rows_frame.columnconfigure((0, 2), weight=2, uniform='a')
rows_frame.columnconfigure(1, weight=1, uniform='a')

# --- 3. UI LOGIC HELPERS ---
notice_text = "unmisoc.com"

def update_label_cached(widget, key, new_value):
    """Updates widget text only if value changes to save CPU."""
    if previous_values.get(key) != new_value:
        widget.configure(text=new_value)
        previous_values[key] = new_value

def get_countdown_text():
    """Calculates time remaining until the next event."""
    if not CURRENT_DAY_DATA: return ""
    now_dt = datetime.now(timezone.utc) + timedelta(hours=OFFSET)
    now_time = now_dt.time()
    times = CURRENT_DAY_DATA['Times']
    
    events = [
        ('Fajr', times['Fajr']), ('Sunrise', times['Sunrise']), 
        ('Dhuhr', times['Dhuhr']), ('Asr', times['Asr']), 
        ('Maghrib', times['Maghrib']), ('Isha', times['Isha']), 
        ('Midnight', CURRENT_DAY_DATA['Midnight'])
    ]
    
    target_name, target_time = "Fajr", events[0][1]
    for name, t_time in events:
        if now_time < t_time:
            target_name, target_time = name, t_time
            break
            
    target_dt = datetime.combine(now_dt.date(), target_time)
    if target_dt < now_dt.replace(tzinfo=None): target_dt += timedelta(days=1)
    
    diff = target_dt - now_dt.replace(tzinfo=None)
    h, r = divmod(int(diff.total_seconds()), 3600)
    m, s = divmod(r, 60)
    return f"{target_name} in {h:02d}:{m:02d}:{s:02d}"

def update_highlights(currentTime):
    """Handles color changes for the active prayer row."""
    global previous_highlight
    if not CURRENT_DAY_DATA: return
    
    times, m_time = CURRENT_DAY_DATA['Times'], CURRENT_DAY_DATA['Midnight']
    p_keys = ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
    g_map = {0: 0, 1: 2, 2: 3, 3: 4, 4: 5}

    h_idx = 5 if (currentTime < m_time or currentTime > times['Isha']) else None
    if h_idx is None and currentTime >= times['Fajr']:
        for i, k in enumerate(p_keys):
            if currentTime < times[k]:
                h_idx = g_map.get(i-1); break

    if h_idx == previous_highlight: return
    
    # Reset old highlight
    if previous_highlight is not None:
        for lbl_dict in [prayer_labels, act_time_labels, iqama_time_labels]:
            lbl_dict[previous_highlight].configure(
                fg_color="transparent", 
                text_color=("black", "white"), 
                font=("Roboto", 50 if lbl_dict==prayer_labels else 80)
            )
            
    # Apply new highlight
    if h_idx is not None:
        for lbl_dict in [prayer_labels, act_time_labels, iqama_time_labels]:
            lbl_dict[h_idx].configure(
                fg_color=GOLD, 
                text_color="white", 
                font=("Roboto", 50 if lbl_dict==prayer_labels else 80, "bold")
            )
    previous_highlight = h_idx

def update_display():
    """Main loop for updating time and UI elements."""
    cTime, dTime, dSec, dMer = time_comparer(OFFSET)
    
    # Static data display (English headers + Arabic Hijri Date)
    hijri_reshaped = get_display(arabic_reshaper.reshape(CURRENT_DAY_DATA['Hijri']))
    hdrs = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']

    update_label_cached(date_label, "date", CURRENT_DAY_DATA['Display_Date'])
    update_label_cached(hijri_label, "hijri", hijri_reshaped)
    update_label_cached(day_label, "day", CURRENT_DAY_DATA['Day_En'])
    update_label_cached(notice, "notice", notice_text)
    update_label_cached(countdown_label, "countdown", get_countdown_text())
    
    update_label_cached(currenttime_labels[0], "c_m", dTime)
    update_label_cached(currenttime_labels[1], "c_s", dSec)
    update_label_cached(currenttime_labels[2], "c_mer", dMer)

    # Update Main Prayer Grid
    raw_keys = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
    for i in [0, 2, 3, 4, 5]:
        update_label_cached(prayer_labels[i], f"pn_{i}", hdrs[i])
        update_label_cached(act_time_labels[i], f"pa_{i}", CURRENT_DAY_DATA['Display'][raw_keys[i]])
        update_label_cached(iqama_time_labels[i], f"pi_{i}", CURRENT_DAY_DATA['Display'][f"{raw_keys[i]}_iqama"])

    # Fixed Status Bar: Sunrise | Midnight
    update_label_cached(status_labels[0], "st0", CURRENT_DAY_DATA['Display']['Sunrise'])
    update_label_cached(status_labels[1], "st1", "Sunrise | Midnight")
    update_label_cached(status_labels[2], "st2", CURRENT_DAY_DATA['Midnight_Disp'])

    update_highlights(cTime)
    root.update_idletasks()
    root.after(1000, update_display)

# --- 4. BUILDING UI WIDGETS ---
# QR Code placement (Top Right)
qr_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
qr_frame.place(relx=0.9, rely=0.05, anchor="ne")
try:
    qr_img = ctk.CTkImage(Image.open("Images/website_qr.png"), size=(140, 140))
    ctk.CTkLabel(qr_frame, image=qr_img, text="").pack()
    ctk.CTkLabel(qr_frame, text="Scan for website", font=("Roboto", 12)).pack()
except:
    ctk.CTkLabel(qr_frame, text="[QR CODE]", font=("Roboto", 12)).pack()

# Center Information
my_image = ctk.CTkImage(
    light_image=Image.open("Images/ISoc (black).png"), 
    dark_image=Image.open("Images/ISoc (white).png"), 
    size=(100, 50)
)
ctk.CTkLabel(info_frame, image=my_image, text="").pack(pady=(20, 10))

date_label = ctk.CTkLabel(info_frame, font=("Roboto", 60))
date_label.pack()

hijri_label = ctk.CTkLabel(info_frame, font=("Roboto", 48))
hijri_label.pack()

day_label = ctk.CTkLabel(info_frame, font=("Roboto", 48))
day_label.pack(pady=5)

# Clock Frame
t_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
t_frame.pack()
currenttime_labels = {
    0: ctk.CTkLabel(t_frame, font=("Roboto", 150, "bold")), 
    1: ctk.CTkLabel(t_frame, font=("Roboto", 50, "bold")), 
    2: ctk.CTkLabel(t_frame, font=("Roboto", 50, "normal"))
}
currenttime_labels[0].grid(row=0, column=0, padx=10)
currenttime_labels[1].grid(row=0, column=1, sticky='n', pady=20)
currenttime_labels[2].grid(row=0, column=1, sticky='s', pady=20)

# Countdown and Notice
countdown_label = ctk.CTkLabel(info_frame, font=("Roboto", 30, "italic"), text_color=GOLD)
countdown_label.pack(pady=5)

notice = ctk.CTkLabel(info_frame, font=("Roboto", 40, "bold"), text_color=GOLD)
notice.pack(pady=10)

# Prayer List Grid
prayer_labels, act_time_labels, iqama_time_labels, status_labels = {}, {}, {}, {}
ctk.CTkLabel(rows_frame, text="Adhan", font=("Roboto", 30)).grid(row=0, column=0)
ctk.CTkLabel(rows_frame, text="Iqamah", font=("Roboto", 30)).grid(row=0, column=2)

r_idx = 1
for i in range(6):
    if i == 1: continue  # Skipping Sunrise in main list
    act_time_labels[i] = ctk.CTkLabel(rows_frame, font=("Roboto", 80))
    act_time_labels[i].grid(row=r_idx, column=0, pady=6, sticky="nsew")
    
    prayer_labels[i] = ctk.CTkLabel(rows_frame, font=("Roboto", 50))
    prayer_labels[i].grid(row=r_idx, column=1, pady=6, sticky="nsew")
    
    iqama_time_labels[i] = ctk.CTkLabel(rows_frame, font=("Roboto", 80))
    iqama_time_labels[i].grid(row=r_idx, column=2, pady=6, sticky="nsew")
    r_idx += 1

# Bottom Status Bar (Sunrise | Midnight)
for i in range(3):
    status_labels[i] = ctk.CTkLabel(rows_frame, font=("Roboto", 30), fg_color=("#969696", "#383838"))
    status_labels[i].grid(row=r_idx, column=i, pady=12, sticky="nsew")

# Initial Lifecycle calls
refresh_daily_data()
update_display()
root.mainloop()