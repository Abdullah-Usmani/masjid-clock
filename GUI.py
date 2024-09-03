from tkinter import *
from timeChecker import *
from PIL import Image
import customtkinter as ctk
import datetime
import time

df, prayer_headers, prayer_headers_ar, iqama_headers = initializers()
selectedRow, date, hijri, day, headers, foundFlag = dateComparer(df, prayer_headers, 8)

# Initialize the app and UI elements
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()

root.title("Prayer Times - ISOC 24/25")
root.geometry('720x1080')

frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill="both", expand=True)
frame.columnconfigure((0,1,2,3), weight = 1)
frame.rowconfigure((0), weight = 1)
frame.rowconfigure((1,2), weight = 2)
frame.rowconfigure((3,4,5,6,7,8,9,10,11,12), weight = 1)


def get_milliseconds_until_midnight():
    now = time.gmtime()  
    now = time.localtime(time.mktime(now) + 8 * 3600)  
    now_datetime = datetime.datetime(year=now.tm_year, month=now.tm_mon, day=now.tm_mday,
                                     hour=now.tm_hour, minute=now.tm_min, second=now.tm_sec)
    midnight = datetime.datetime.combine(now_datetime.date() + datetime.timedelta(days=1), datetime.time(0, 0))
    remaining_time = midnight - now_datetime
    return int(remaining_time.total_seconds() * 1000)  # Convert seconds to milliseconds

toggle_state = False

def status_toggle():
    global toggle_state
    toggle_state = not toggle_state
    root.after(10000, status_toggle)

def update_display():
    currentTime, displayCurrentTime, displayCurrentTime_s, displayCurrentTime_meridian, act_times, iqama_times, display_act_times, display_iqama_times, current_prayer, next_prayer = timeComparer(selectedRow, df, prayer_headers, iqama_headers, 8)
    
    # Replace hyphens with spaces
    f_date = date.replace('-', ' ')
    f_hijri = hijri.replace('-', ' ')

    # Update labels
    if foundFlag:
        date_label.configure(text=f"{f_date} | {f_hijri}")
        day_label.configure(text=f"{day}")
    else:
        print("XX:XX - UPDATE REQUIRED")

    currenttime_labels[0].configure(text=f"{displayCurrentTime}")
    currenttime_labels[1].configure(text=f"{displayCurrentTime_s}")
    currenttime_labels[2].configure(text=f"{displayCurrentTime_meridian}")

    for i in range(len(prayer_headers)):
        if i == 1:
            continue  # Skip the element at index 2
        if i == 6:
            continue  # Skip the element at index 2
        
        sel = prayer_headers[i]
        prayer_labels[i].configure(text=f"{prayer_headers[i]}", font=("Roboto", 24, "normal"))
        act_time_labels[i].configure(text=f"{display_act_times[sel]}", font=("Roboto", 32, "normal"))
        iqama_time_labels[i].configure(text=f"{display_iqama_times[sel]}", font=("Roboto", 32, "normal"))
        prayer_labels_ar[i].configure(text=f"{prayer_headers_ar[i]}", font=("Roboto", 28, "normal"))

    for i in range(len(prayer_headers)):
        next = prayer_headers[i]
        if i == 2:
            continue
        if i == 7:
            continue
        if currentTime < act_times['Midnight']:  # Compare current time with the actual time
            prayer_labels[5].configure(font=("Roboto", 24, "bold"))
            act_time_labels[5].configure(font=("Roboto", 32, "bold"))
            iqama_time_labels[5].configure(font=("Roboto", 32, "bold"))
            prayer_labels_ar[5].configure(font=("Roboto", 28, "bold"))
            break
        if currentTime < act_times['Fajr']:  # Compare current time with the actual time
            break
        if currentTime < act_times['Zohor'] and i > 2:
            break
        elif currentTime < act_times[next]:  # Compare current time with the actual time
            prayer_labels[i-1].configure(font=("Roboto", 24, "bold"))
            act_time_labels[i-1].configure(font=("Roboto", 32, "bold"))
            iqama_time_labels[i-1].configure(font=("Roboto", 32, "bold"))
            prayer_labels_ar[i-1].configure(font=("Roboto", 28, "bold"))
            break
        elif currentTime > act_times['Isyak']:
            prayer_labels[5].configure(font=("Roboto", 24, "bold"))
            act_time_labels[5].configure(font=("Roboto", 32, "bold"))
            iqama_time_labels[5].configure(font=("Roboto", 32, "bold"))
            prayer_labels_ar[5].configure(font=("Roboto", 28, "bold"))
            break

    new_text0 = f"{prayer_headers[1]}" if toggle_state else f"{prayer_headers[6]}"
    status_labels[0].configure(text=new_text0)
    new_text1 = f"{display_act_times['Syuruk']}" if toggle_state else f"{display_act_times['Midnight']}"
    status_labels[1].configure(text=new_text1)
    new_text2 = f"{prayer_headers_ar[1]}" if toggle_state else f"{prayer_headers_ar[6]}"
    status_labels[2].configure(text=new_text2)

    # if currentTime < act_times[next_prayer]:  # Compare current time with the actual time
    #     status_label.configure(text=f"{next_prayer} is next!")
    # elif currentTime > act_times['Isyak']:
    #     status_label.configure(text=f"Fajr is next!")

    # Schedule the function to run again after 1 second (1000 milliseconds)
    root.after(1000, update_display)

def update_date():
    selectedRow, date, hijri, day, headers, foundFlag = dateComparer(df, prayer_headers, 8)
    update_display()
    status_toggle()
    
    root.after(86400000, update_date)

def schedule_daily_update():
    milliseconds_until_midnight = get_milliseconds_until_midnight()
    root.after(milliseconds_until_midnight, update_date)



my_image = ctk.CTkImage(light_image=Image.open("Images/ISoc (black).png"),
                                  dark_image=Image.open("Images/ISoc (white).png"),
                                  size=(100, 50))
image_label = ctk.CTkLabel(frame, image=my_image, text="")
image_label.grid(sticky="nsew", row=0, column=0, columnspan=4, pady=6, padx=12)

date_label = ctk.CTkLabel(master=frame, font=("Roboto", 48))
date_label.grid(sticky="nsew", row=1, column=0, columnspan=4, pady=12, padx=10)

day_label = ctk.CTkLabel(master=frame, font=("Roboto", 32))
day_label.grid(sticky="nsew", row=2, column=0, columnspan=4, pady=6, padx=10)

# currenttime_label_holder = ctk.CTkLabel(master=frame, font=("Roboto", 56, "bold"))
# currenttime_label_holder.grid(sticky="n", row=3, column=0, columnspan=4, pady=30, padx=10)
currenttime_labels = {}
currenttime_labels[0] = ctk.CTkLabel(master=frame, font=("Roboto", 56, "bold"))
currenttime_labels[0].grid(sticky="n", row=3, column=1, columnspan=2, pady=30, padx=10)
currenttime_labels[1] = ctk.CTkLabel(master=frame, font=("Roboto", 24, "normal"))
currenttime_labels[1].grid(sticky="ne", row=3, column=2, columnspan=1, pady=30, padx=10)
currenttime_labels[2] = ctk.CTkLabel(master=frame, font=("Roboto", 24, "bold"))
currenttime_labels[2].grid(sticky="e", row=3, column=2, columnspan=1, pady=30, padx=10)

# Grid headers
ctk.CTkLabel(frame, text="               ", font=("Roboto", 24)).grid(row=4, column=0, padx=10, pady=5, sticky="nsew")
ctk.CTkLabel(frame, text="Adhan ", font=("Roboto", 24)).grid(row=4, column=1, padx=10, pady=5, sticky="nsew")
ctk.CTkLabel(frame, text="Iqamah", font=("Roboto", 24)).grid(row=4, column=2, padx=10, pady=5, sticky="nsew")
ctk.CTkLabel(frame, text="               ", font=("Roboto", 24)).grid(row=4, column=3, padx=10, pady=5, sticky="nsew")


# Create grid structure for prayer times
prayer_labels = {}
act_time_labels = {}
iqama_time_labels = {}
prayer_labels_ar = {}
status_labels = {}

row_counter = 5  # Initialize the row counter for grid placement

for i in range(len(prayer_headers)):
    if i == 1:
        continue  # Skip the element at index 2
    if i == 6:
        continue  # Skip the element at index 7
    
    sel = prayer_headers[i]
    prayer_labels[i] = ctk.CTkLabel(master=frame, font=("Roboto", 24))
    prayer_labels[i].grid(row=row_counter, column=0, pady=6, sticky="nsew")
    
    act_time_labels[i] = ctk.CTkLabel(master=frame, font=("Roboto", 32))
    act_time_labels[i].grid(row=row_counter, column=1, pady=6, sticky="nsew")
    
    iqama_time_labels[i] = ctk.CTkLabel(master=frame, font=("Roboto", 32))
    iqama_time_labels[i].grid(row=row_counter, column=2, pady=6, sticky="nsew")
    
    prayer_labels_ar[i] = ctk.CTkLabel(master=frame, font=("Roboto", 28))
    prayer_labels_ar[i].grid(row=row_counter, column=3, pady=6, sticky="nsew")
    
    row_counter += 1  # Increment row counter for the next set of labels



status_labels[0] = ctk.CTkLabel(master=frame, font=("Roboto", 24), bg_color="lightgray")
status_labels[0].grid(row=row_counter, column=0, columnspan=1, pady=12, padx=0, sticky="nsew")
status_labels[1] = ctk.CTkLabel(master=frame, font=("Roboto", 24), bg_color="lightgray")
status_labels[1].grid(row=row_counter, column=1, columnspan=2, pady=12, padx=0, sticky="nsew")
status_labels[2] = ctk.CTkLabel(master=frame, font=("Roboto", 28), bg_color="lightgray")
status_labels[2].grid(row=row_counter, column=3, columnspan=1, pady=12, padx=0, sticky="nsew")

# Call the schedule_daily_update function once to start the periodic updates
update_date()
schedule_daily_update()

# Execute Tkinter
root.mainloop()
