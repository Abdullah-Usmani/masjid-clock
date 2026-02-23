import tkinter as tk
from PIL import Image
import customtkinter as ctk
from datetime import datetime, timedelta, timezone
import arabic_reshaper
from bidi.algorithm import get_display
import os

from time_checker import process_prayer_data, time_comparer

# --- CONFIG ---
OFFSET = 8
PRAYER_DATABASE = process_prayer_data('./prayerTimes.csv')
CURRENT_DAY_DATA = None
GOLD = "#946d2e"
LIGHT = "#f2f4f5"
DARK = "#212121"
previous_values = {}
previous_highlight = None

def get_ms_until_midnight():
    now = datetime.now(timezone.utc) + timedelta(hours=OFFSET)
    tomorrow = datetime.combine(now.date() + timedelta(days=1), datetime.min.time(), tzinfo=now.tzinfo)
    return int((tomorrow - now).total_seconds() * 1000)

def refresh_daily_data():
    global CURRENT_DAY_DATA
    now = datetime.now(timezone.utc) + timedelta(hours=OFFSET)
    today_str = now.strftime('%d-%b-%Y')
    CURRENT_DAY_DATA = PRAYER_DATABASE.get(today_str)
    root.after(get_ms_until_midnight(), refresh_daily_data)

# --- UI SETUP ---
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title("Prayer Times - ISOC Static")
root.geometry('1080x1920') # Portrait resolution
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

main_frame = ctk.CTkFrame(master=root, fg_color=(LIGHT, DARK))
main_frame.pack(padx=10, pady=10, fill='both', expand=True)

# Adjusted height proportions to fill the screen better
info_frame = ctk.CTkFrame(master=main_frame, fg_color="transparent")
info_frame.place(x=0,y=0,relwidth=1,relheight=0.45)

prayer_frame = ctk.CTkFrame(master=main_frame, fg_color="transparent")
prayer_frame.place(x=0,rely=0.45,relwidth=1,relheight=.55)

rows_frame = ctk.CTkFrame(master=prayer_frame, fg_color="transparent")
rows_frame.pack(fill='both', expand=True, ipady=30, ipadx=50)

# Grid configuration to force rows to fill the vertical space
rows_frame.columnconfigure((0, 2), weight=2, uniform='a')
rows_frame.columnconfigure(1, weight=1, uniform='a')

# Force all 7 rows (Header + 6 Times) to expand equally
for i in range(7):
    rows_frame.rowconfigure(i, weight=1)

# --- HELPERS ---
def update_label_cached(widget, key, new_value):
    if previous_values.get(key) != new_value:
        widget.configure(text=new_value)
        previous_values[key] = new_value

def get_countdown_text():
    if not CURRENT_DAY_DATA: return ""
    now_dt = datetime.now(timezone.utc) + timedelta(hours=OFFSET)
    now_time = now_dt.time()
    times = CURRENT_DAY_DATA['Times']
    
    events = [('Fajr', times['Fajr']), ('Sunrise', times['Sunrise']), ('Dhuhr', times['Dhuhr']), 
              ('Asr', times['Asr']), ('Maghrib', times['Maghrib']), ('Isha', times['Isha']), 
              ('Midnight', CURRENT_DAY_DATA['Midnight'])]
    
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
    global previous_highlight
    if not CURRENT_DAY_DATA: return
    
    times = CURRENT_DAY_DATA['Times']
    m_time = CURRENT_DAY_DATA['Midnight']
    
    # Define specific active windows for highlighting
    # Logic: Highlight is ONLY active from the start of the prayer time
    # until the 'cutoff' event (Sunrise for Fajr, or the next prayer).
    
    highlight_index = None

    # Window 1: Isha / Midnight (Isha -> Midnight)
    if currentTime >= times['Isha'] or currentTime < m_time:
        highlight_index = 5
    # Window 2: Fajr (Fajr -> Sunrise)
    elif times['Fajr'] <= currentTime < times['Sunrise']:
        highlight_index = 0
    # Window 3: Dhuhr (Dhuhr -> Asr)
    elif times['Dhuhr'] <= currentTime < times['Asr']:
        highlight_index = 2
    # Window 4: Asr (Asr -> Maghrib)
    elif times['Asr'] <= currentTime < times['Maghrib']:
        highlight_index = 3
    # Window 5: Maghrib (Maghrib -> Isha)
    elif times['Maghrib'] <= currentTime < times['Isha']:
        highlight_index = 4
    
    # If currentTime is between Sunrise and Dhuhr, highlight_index remains None.

    if highlight_index == previous_highlight:
        return
    
    # Reset old highlight if it exists
    if previous_highlight is not None:
        for lbl_dict in [prayer_labels, act_time_labels, iqama_time_labels]:
            lbl_dict[previous_highlight].configure(
                fg_color="transparent", 
                text_color=("black", "white"), 
                font=("Roboto", 50 if lbl_dict==prayer_labels else 80)
            )
            
    # Apply new highlight if we are in an active window
    if highlight_index is not None:
        for lbl_dict in [prayer_labels, act_time_labels, iqama_time_labels]:
            lbl_dict[highlight_index].configure(
                fg_color=GOLD, 
                text_color="white", 
                font=("Roboto", 50 if lbl_dict==prayer_labels else 80, "bold")
            )
            
    previous_highlight = highlight_index

def update_display():
    cTime, dTime, dSec, dMer = time_comparer(OFFSET)
    hijri_s = get_display(arabic_reshaper.reshape(CURRENT_DAY_DATA['Hijri']))
    
    update_label_cached(date_label, "date", CURRENT_DAY_DATA['Display_Date'])
    update_label_cached(hijri_label, "hijri", hijri_s)
    update_label_cached(day_label, "day", CURRENT_DAY_DATA['Day_En'])
    update_label_cached(countdown_label, "countdown", get_countdown_text())
    update_label_cached(currenttime_labels[0], "c_m", dTime)
    update_label_cached(currenttime_labels[1], "c_s", dSec)
    update_label_cached(currenttime_labels[2], "c_mer", dMer)

    raw = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
    for i in [0, 2, 3, 4, 5]:
        update_label_cached(act_time_labels[i], f"pa_{i}", CURRENT_DAY_DATA['Display'][raw[i]])
        update_label_cached(iqama_time_labels[i], f"pi_{i}", CURRENT_DAY_DATA['Display'][f"{raw[i]}_iqama"])

    # STATIC STATUS LABELS
    update_label_cached(status_labels[0], "st0", CURRENT_DAY_DATA['Display']['Sunrise'])
    update_label_cached(status_labels[1], "st1", "Sunrise | Midnight")
    update_label_cached(status_labels[2], "st2", CURRENT_DAY_DATA['Midnight_Disp'])

    update_highlights(cTime)
    root.update_idletasks()
    root.after(1000, update_display)

# --- UI BUILDING ---
qr_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
qr_frame.place(relx=0.9, rely=0.05, anchor="ne")
try:
    qr_img = ctk.CTkImage(Image.open("Images/website_qr.png"), size=(140, 140))
    ctk.CTkLabel(qr_frame, image=qr_img, text="").pack()
    ctk.CTkLabel(qr_frame, text="Scan for website", font=("Roboto", 12)).pack()
except:
    ctk.CTkLabel(qr_frame, text="[QR CODE]", font=("Roboto", 12)).pack()

try:
    logo_path_light = "Images/ISoc (black).png"
    logo_path_dark = "Images/ISoc (white).png"
    
    my_image = ctk.CTkImage(
        light_image=Image.open(logo_path_light), 
        dark_image=Image.open(logo_path_dark), 
        size=(100,50)
    )
    logo_label = ctk.CTkLabel(info_frame, image=my_image, text="")
    logo_label.pack(pady=(20, 40))
except Exception as e:
    print(f"Logo failed to load: {e}")
    ctk.CTkLabel(info_frame, text="[ISOC LOGO MISSING]", text_color="red").pack(pady=20)

# 2. Date Section
date_label = ctk.CTkLabel(info_frame, font=("Roboto", 60))
date_label.pack(expand=True)

hijri_label = ctk.CTkLabel(master=info_frame, font=("Roboto", 60))
hijri_label.pack(expand=True, ipady=10)

day_label = ctk.CTkLabel(master=info_frame, font=("Roboto", 48))
day_label.pack(expand=True, ipady=10)

# 3. Clock Section
t_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
t_frame.pack(fill='none',expand=False)

currenttime_labels = {
    0: ctk.CTkLabel(t_frame, font=("Roboto", 150, "bold")), 
    1: ctk.CTkLabel(t_frame, font=("Roboto", 50, "bold")), 
    2: ctk.CTkLabel(t_frame, font=("Roboto", 50, "normal"))
}
currenttime_labels[0].grid(row=0, column=0, padx=15)
currenttime_labels[1].grid(row=0, column=1, sticky='n', pady=25)
currenttime_labels[2].grid(row=0, column=1, sticky='s', pady=25)

# 4. Countdown & Notice
countdown_label = ctk.CTkLabel(info_frame, font=("Roboto", 30, "normal"), text_color=GOLD)
countdown_label.pack(pady=10, padx=15)

ctk.CTkLabel(info_frame, text="unmisoc.com", font=("Roboto", 45, "bold"), text_color=GOLD).pack(pady=15)

prayer_labels, act_time_labels, iqama_time_labels, status_labels = {}, {}, {}, {}
p_names = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
ctk.CTkLabel(rows_frame, text="Adhan", font=("Roboto", 30)).grid(row=0, column=0)
ctk.CTkLabel(rows_frame, text="Iqamah", font=("Roboto", 30)).grid(row=0, column=2)

r_idx = 1
for i in range(6):
    if i == 1: continue
    act_time_labels[i] = ctk.CTkLabel(rows_frame, font=("Roboto", 80)); act_time_labels[i].grid(row=r_idx, column=0, pady=6, sticky="nsew")
    prayer_labels[i] = ctk.CTkLabel(rows_frame, text=p_names[i], font=("Roboto", 50)); prayer_labels[i].grid(row=r_idx, column=1, pady=6, sticky="nsew")
    iqama_time_labels[i] = ctk.CTkLabel(rows_frame, font=("Roboto", 80)); iqama_time_labels[i].grid(row=r_idx, column=2, pady=6, sticky="nsew")
    r_idx += 1

for i in range(3):
    status_labels[i] = ctk.CTkLabel(rows_frame, font=("Roboto", 24), fg_color=("#969696", "#383838")); status_labels[i].grid(row=r_idx, column=i, pady=12, sticky="nsew")

refresh_daily_data(); update_display(); root.mainloop()