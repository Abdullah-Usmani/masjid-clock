from tkinter import *
from timeChecker import *
from PIL import Image
import customtkinter as ctk

df, prayer_headers, iqama_headers = initializers()
selectedRow, date, hijri, day, headers, foundFlag = dateComparer(df, prayer_headers, 8)

# Initialize the app and UI elements
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

root = ctk.CTk()

root.title("Prayer Times - ISOC 24/25")
root.geometry('720x1080')

frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)


def get_milliseconds_until_midnight():
    now = time.gmtime()  
    now = time.localtime(time.mktime(now) + 8 * 3600)  
    now_datetime = datetime.datetime(year=now.tm_year, month=now.tm_mon, day=now.tm_mday,
                                     hour=now.tm_hour, minute=now.tm_min, second=now.tm_sec)
    midnight = datetime.datetime.combine(now_datetime.date() + datetime.timedelta(days=1), datetime.time(0, 0))
    remaining_time = midnight - now_datetime
    return int(remaining_time.total_seconds() * 1000)  # Convert seconds to milliseconds

def update_display():
    currentTime, displayCurrentTime, act_times, iqama_times, display_act_times, display_iqama_times, current_prayer, next_prayer = timeComparer(selectedRow, df, prayer_headers, iqama_headers, 8)
    
    # Update labels
    if foundFlag:
        date_label.configure(text=f"{date} | {hijri}")
        day_label.configure(text=f"{day}")
    else:
        print("XX:XX - UPDATE REQUIRED")

    currenttime_label.configure(text=f"{displayCurrentTime}")

    for i in range(len(prayer_headers)):
        if i == 1:
            continue  # Skip the element at index 2
        sel = prayer_headers[i]
        prayer_labels[i].configure(text=f"{prayer_headers[i]} - {display_act_times[sel]} : {display_iqama_times[sel]}")

    if currentTime < act_times[next_prayer]:  # Compare current time with the actual time
        status_label.configure(text=f"{next_prayer} is next!")
    elif currentTime > act_times['Isyak']:
        status_label.configure(text=f"Fajr is next!")

    # Schedule the function to run again after 1 second (1000 milliseconds)
    root.after(1000, update_display)

def update_date():
    selectedRow, date, hijri, day, headers, foundFlag = dateComparer(df, prayer_headers, 8)
    update_display()
    
    root.after(86400000, update_date)

def schedule_daily_update():
    milliseconds_until_midnight = get_milliseconds_until_midnight()
    root.after(milliseconds_until_midnight, update_date)




my_image = ctk.CTkImage(light_image=Image.open("Images/ISoc (black).png"),
                                  dark_image=Image.open("Images/ISoc (white).png"),
                                  size=(100, 50))
image_label = ctk.CTkLabel(frame, image=my_image, text="")
image_label.pack(pady=24, padx=12)


# label = ctk.CTkLabel(master=frame, text=f"Prayer Times", font=("Roboto", 24))
# label.pack(pady=12, padx=10)

date_label = ctk.CTkLabel(master=frame, font=("Roboto", 48))
date_label.pack(pady=12, padx=10)

day_label = ctk.CTkLabel(master=frame, font=("Roboto", 32))
day_label.pack(pady=6, padx=10)

currenttime_label = ctk.CTkLabel(master=frame, font=("Roboto", 48))
currenttime_label.pack(pady=30, padx=10)

prayer_labels = {}
for i in range(len(prayer_headers)):
    if i == 1:
        continue  # Skip the element at index 2
    sel = prayer_headers[i]
    prayer_labels[i] = ctk.CTkLabel(master=frame, font=("Roboto", 32))
    prayer_labels[i].pack(pady=12, padx=10)

status_label = ctk.CTkLabel(master=frame, font=("Roboto", 32))
status_label.pack(pady=12, padx=10)

# Call the schedule_daily_update function once to start the periodic updates
update_date()
update_display()
schedule_daily_update()

# Execute Tkinter
root.mainloop()
