from tkinter import *
from timeChecker import *
from PIL import Image
import customtkinter as ctk
import datetime
import time

df, prayer_headers, prayer_headers_ar, iqama_headers = initializers()
selectedRow, date, hijri, day, headers, foundFlag = dateComparer(df, prayer_headers, 8)
toggle_state = False

# Initialize the app and UI elements
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()

root.title("Prayer Times - ISOC 24/25")
root.geometry('720x1080+0+0')

main_frame = ctk.CTkFrame(master=root)
main_frame.pack(padx=20, pady=20, fill='both', expand=True)

info_frame = ctk.CTkFrame(master=main_frame)
info_frame.place(x=0,y=0,relwidth=1,relheight=0.55)
# info_frame.rowconfigure((0,1,2,3,4), weight = 2, uniform='a')

prayer_frame = ctk.CTkFrame(master=main_frame)
prayer_frame.place(x=0,rely=0.55,relwidth=1,relheight=.45)

rows_frame = ctk.CTkFrame(master=prayer_frame)
rows_frame.pack(fill='both', expand=True)
rows_frame.columnconfigure((0,1,2,3), weight = 1, uniform='a')
rows_frame.rowconfigure((0,1,2,3,4,5,6,7), weight = 1, uniform='a')




def get_milliseconds_until_midnight():
    now = time.gmtime()  
    now = time.localtime(time.mktime(now) + 6 * 3600)  
    now_datetime = datetime.datetime(year=now.tm_year, month=now.tm_mon, day=now.tm_mday,
                                     hour=now.tm_hour, minute=now.tm_min, second=now.tm_sec)
    midnight = datetime.datetime.combine(now_datetime.date() + datetime.timedelta(days=1), datetime.time(0, 0))
    remaining_time = midnight - now_datetime
    return int(remaining_time.total_seconds() * 1000)  # Convert seconds to milliseconds

def update_date():
    global selectedRow, date, hijri, day, headers, foundFlag
    selectedRow, date, hijri, day, headers, foundFlag = dateComparer(df, prayer_headers, 8)
    update_display()
    status_toggle()
    
    root.after(86400000, update_date)

def schedule_daily_update():
    milliseconds_until_midnight = get_milliseconds_until_midnight()
    root.after(milliseconds_until_midnight, update_date)

def status_toggle():
    global toggle_state
    toggle_state = not toggle_state
    root.after(10000, status_toggle)

def update_display():
    currentTime, displayCurrentTime, displayCurrentTime_s, displayCurrentTime_meridian, act_times, iqama_times, display_act_times, display_iqama_times = timeComparer(selectedRow, df, prayer_headers, iqama_headers, 8)


    date_text = f"{date}" if toggle_state else f"{hijri}"
    date_label.configure(text=date_text)
    # Update labels
    # if foundFlag:
    day_label.configure(text=f"{day}")
    # else:
    #     print("XX:XX - UPDATE REQUIRED")

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
        if currentTime < act_times['Dhuhr'] and i > 2:
            break
        elif currentTime < act_times[next]:  # Compare current time with the actual time
            prayer_labels[i-1].configure(font=("Roboto", 24, "bold"))
            act_time_labels[i-1].configure(font=("Roboto", 32, "bold"))
            iqama_time_labels[i-1].configure(font=("Roboto", 32, "bold"))
            prayer_labels_ar[i-1].configure(font=("Roboto", 28, "bold"))
            break
        elif currentTime > act_times['Isha']:
            prayer_labels[5].configure(font=("Roboto", 24, "bold"))
            act_time_labels[5].configure(font=("Roboto", 32, "bold"))
            iqama_time_labels[5].configure(font=("Roboto", 32, "bold"))
            prayer_labels_ar[5].configure(font=("Roboto", 28, "bold"))
            break

    new_text0 = f"{prayer_headers[1]}" if toggle_state else f"{prayer_headers[6]}"
    status_labels[0].configure(text=new_text0)
    new_text1 = f"{display_act_times['Sunrise']}" if toggle_state else f"{display_act_times['Midnight']}"
    status_labels[1].configure(text=new_text1)
    new_text2 = f"{prayer_headers_ar[1]}" if toggle_state else f"{prayer_headers_ar[6]}"
    status_labels[2].configure(text=new_text2)

    # Schedule the function to run again after 1 second (1000 milliseconds)
    root.after(1000, update_display)



my_image = ctk.CTkImage(light_image=Image.open("Images/ISoc (black).png"),
                                  dark_image=Image.open("Images/ISoc (white).png"),
                                  size=(100, 50))
image_label = ctk.CTkLabel(info_frame, image=my_image, text="")
image_label.pack(expand=True)

date_label = ctk.CTkLabel(master=info_frame, font=("Roboto", 48))
date_label.pack(expand=True)

day_label = ctk.CTkLabel(master=info_frame, font=("Roboto", 32))
day_label.pack(expand=True)

# currenttime_label_holder = ctk.CTkLabel(master=info_frame, font=("Roboto", 56, "bold"))
# currenttime_label_holder.grid(sticky="n", row=3, columnspan=4, pady=30, padx=10)
currenttime_labels = {}

# Create a info_frame that spans columns 1 and 2
time_frame = ctk.CTkFrame(master=info_frame)
time_frame.pack(fill='none',expand=False)

# Add elements to the container frame using `grid()`
currenttime_labels[0] = ctk.CTkLabel(master=time_frame, font=("Roboto", 100, "bold"))
currenttime_labels[0].grid(row=0, column=2, padx=(0, 5), pady=10)

currenttime_labels[1] = ctk.CTkLabel(master=time_frame, font=("Roboto", 24, "bold"))
currenttime_labels[1].grid(row=0, column=3, padx=(5, 5), pady=10)

currenttime_labels[2] = ctk.CTkLabel(master=time_frame, font=("Roboto", 24, "normal"))
currenttime_labels[2].grid(row=0, column=4, padx=(5, 5), pady=10)
ctk.CTkLabel(time_frame, text="", font=("Roboto", 24)).grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
ctk.CTkLabel(time_frame, text="", font=("Roboto", 24)).grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

# Configure columns to handle layout expansion and centering
time_frame.columnconfigure((0,1,3,4), weight=1, uniform='a')  # Empty column for spacing on the left
time_frame.columnconfigure(2, weight=2)
time_frame.rowconfigure(0, weight=0)

# Create a info_frame that spans columns 1 and 2
noti_frame = ctk.CTkFrame(master=info_frame, fg_color="transparent")
noti_frame.pack(fill='x', expand=True)
notice = ctk.CTkLabel(noti_frame, text="ISHA DELAYED", font=("Roboto", 24, "bold"), text_color=("maroon", "red"))
notice.pack(padx=10, pady=5)


# Prayers Frame


# Grid headers
ctk.CTkLabel(rows_frame, text="", font=("Roboto", 24)).grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
ctk.CTkLabel(rows_frame, text="Adhan ", font=("Roboto", 24)).grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
ctk.CTkLabel(rows_frame, text="Iqamah", font=("Roboto", 24)).grid(row=0, column=2, padx=10, pady=5, sticky="nsew")
ctk.CTkLabel(rows_frame, text="", font=("Roboto", 24)).grid(row=0, column=3, padx=10, pady=5, sticky="nsew")


# Create grid structure for prayer times
prayer_labels = {}
act_time_labels = {}
iqama_time_labels = {}
prayer_labels_ar = {}
status_labels = {}

row_counter = 1  # Initialize the row counter for grid placement

for i in range(len(prayer_headers)):
    if i == 1:
        continue  # Skip the element at index 2
    if i == 6:
        continue  # Skip the element at index 7
    
    sel = prayer_headers[i]
    prayer_labels[i] = ctk.CTkLabel(master=rows_frame, font=("Roboto", 24))
    prayer_labels[i].grid(row=row_counter, column=0, pady=6, sticky="nsew")
    
    act_time_labels[i] = ctk.CTkLabel(master=rows_frame, font=("Roboto", 32))
    act_time_labels[i].grid(row=row_counter, column=1, pady=6, sticky="nsew")
    
    iqama_time_labels[i] = ctk.CTkLabel(master=rows_frame, font=("Roboto", 32))
    iqama_time_labels[i].grid(row=row_counter, column=2, pady=6, sticky="nsew")
    
    prayer_labels_ar[i] = ctk.CTkLabel(master=rows_frame, font=("Roboto", 28))
    prayer_labels_ar[i].grid(row=row_counter, column=3, pady=6, sticky="nsew")
    
    row_counter += 1  # Increment row counter for the next set of labels



status_labels[0] = ctk.CTkLabel(master=rows_frame, font=("Roboto", 24), bg_color=("lightgray", "darkgray"), text_color="black")
status_labels[0].grid(row=row_counter, column=0, columnspan=1, pady=12, padx=0, sticky="nsew")
status_labels[1] = ctk.CTkLabel(master=rows_frame, font=("Roboto", 24), bg_color=("lightgray", "darkgray"), text_color="black")
status_labels[1].grid(row=row_counter, column=1, columnspan=2, pady=12, padx=0, sticky="nsew")
status_labels[2] = ctk.CTkLabel(master=rows_frame, font=("Roboto", 28), bg_color=("lightgray", "darkgray"), text_color="black")
status_labels[2].grid(row=row_counter, column=3, columnspan=1, pady=12, padx=0, sticky="nsew")

# Call the schedule_daily_update function once to start the periodic updates
update_date()
schedule_daily_update()

# Execute Tkinter
root.mainloop()
