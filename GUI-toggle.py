from tkinter import *
from timeChecker import *
from PIL import Image
import customtkinter as ctk
import datetime
import time
# import tracemalloc
# import psutil

# starting the monitoring
# tracemalloc.start()

df, prayer_headers, prayer_headers_ar, iqama_headers = initializers()
selectedRow, date, hijri, day, day_ar, headers, foundFlag, act_times, iqama_times, display_act_times, display_iqama_times  = dateComparer(df, prayer_headers, iqama_headers, 8)
toggle_state = False

# Initialize the app and UI elements
ctk.set_appearance_mode("dark")
# ctk.set_default_color_theme("green")
light = "#f2f4f5"
dark = "#212121"

root = ctk.CTk()

root.title("Prayer Times - ISOC 24/25")
root.geometry('1080x1920+1910+0')  # Width x Height + X + Y
# root.geometry('2560x1600+0+0')  # Width x Height + X + Y

# Make the window fullscreen
root.attributes("-fullscreen", True)

# Optional: Bind the Escape key to exit fullscreen
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

main_frame = ctk.CTkFrame(master=root, fg_color=(light, dark))
main_frame.pack(padx=10, pady=10, fill='both', expand=True)

info_frame = ctk.CTkFrame(master=main_frame, fg_color=(light, dark))
info_frame.place(x=0,y=0,relwidth=1,relheight=0.45)

prayer_frame = ctk.CTkFrame(master=main_frame, fg_color=(light, dark))
prayer_frame.place(x=0,rely=0.45,relwidth=1,relheight=.55)

rows_frame = ctk.CTkFrame(master=prayer_frame, fg_color=(light, dark))
rows_frame.pack(fill='both', expand=True, ipady=30, ipadx=60)
rows_frame.columnconfigure((0,2), weight = 2, uniform='a')
rows_frame.columnconfigure((1), weight = 1, uniform='a')
rows_frame.rowconfigure((0,1,2,3,4,5), weight = 1, uniform='a')


def get_milliseconds_until_midnight():
    now = time.gmtime()  
    now = time.localtime(time.mktime(now) + 8 * 5400)  
    now_datetime = datetime.datetime(year=now.tm_year, month=now.tm_mon, day=now.tm_mday,
                                     hour=now.tm_hour, minute=now.tm_min, second=now.tm_sec)
    midnight = datetime.datetime.combine(now_datetime.date() + datetime.timedelta(days=1), datetime.time(0, 0))
    remaining_time = midnight - now_datetime
    return int(remaining_time.total_seconds() * 1000)  # Convert seconds to milliseconds

def update_date():
    global selectedRow, date, hijri, day, day_ar, headers, foundFlag, act_times, iqama_times, display_act_times, display_iqama_times 
    selectedRow, date, hijri, day, day_ar, headers, foundFlag, act_times, iqama_times, display_act_times, display_iqama_times  = dateComparer(df, prayer_headers, iqama_headers, 8)
    update_display()
    status_toggle()
    
    root.after(86400000, update_date)

def schedule_daily_update():
    milliseconds_until_midnight = get_milliseconds_until_midnight()
    root.after(milliseconds_until_midnight, update_date)


notice_text = "scaled-back version"

def input_dialog():
    dialog = ctk.CTkInputDialog(text="Enter a notice:", title="Notice Change")
    notice_text = dialog.get_input()  # waits for input
    return notice_text

# Function to be triggered by keybind or button
def show_dialog():
    global notice_text
    notice_text = input_dialog()  # Get input from the user and update the variable

# Bind the key (e.g., "d" key) to the dialog function
root.bind("<e>", lambda event: show_dialog())  # You can change "d" to any ke

def status_toggle():
    global toggle_state
    toggle_state = not toggle_state
    root.after(5000, status_toggle)

# Example of caching
default_font = ("Roboto", 54, "bold")
previous_values = {}


def update_label(widget, key, new_value):
    if previous_values.get(key) != new_value:
        widget.configure(text=new_value)
        previous_values[key] = new_value

# Cache for previously updated indices
previous_highlight = None

def update_highlights(currentTime):
    global previous_highlight

    # Pre-check conditions outside the loop
    if currentTime < act_times['Midnight']:
        highlight_index = 5
    elif currentTime < act_times['Fajr']:
        return  # No highlighting needed
    elif currentTime > act_times['Isha']:
        highlight_index = 5
    else:
        # Check the loop-dependent conditions
        highlight_index = None
        for i in [1, 3, 4, 5, 6]:
            next_prayer_time = act_times[prayer_headers[i]]
            if currentTime < next_prayer_time:
                highlight_index = i - 1
                break

    # Skip redundant updates
    if highlight_index == previous_highlight:
        return

    # Reset previous highlights
    if previous_highlight is not None:
        prayer_labels[previous_highlight].configure(font=("Roboto", 36), fg_color=(light, dark), text_color=("black", "white"))
        act_time_labels[previous_highlight].configure(font=("Roboto", 48), fg_color=(light, dark), text_color=("black", "white"))
        iqama_time_labels[previous_highlight].configure(font=("Roboto", 48), fg_color=(light, dark), text_color=("black", "white"))

    # Apply new highlights
    prayer_labels[highlight_index].configure(font=("Roboto", 36, "bold"), fg_color="#946d2e", text_color="white")
    act_time_labels[highlight_index].configure(font=("Roboto", 48, "bold"), fg_color="#946d2e", text_color="white")
    iqama_time_labels[highlight_index].configure(font=("Roboto", 48, "bold"), fg_color="#946d2e", text_color="white")

    # Update the cache
    previous_highlight = highlight_index


def update_display():
    global toggle_state, notice_text, prayer_headers, act_times, iqama_times, display_act_times, display_iqama_times
    
    notice.configure(text=notice_text)

    # Caching repeated values
    currentTime, displayCurrentTime, displayCurrentTime_s, displayCurrentTime_meridian = timeComparer(8)
    
    # date_text, day_text, prayer_size, switch_font, adhan_text, iqamah_text, adhan_size = date, day, 42, "Roboto", "Adhan", "Iqamah", 27
    if toggle_state:
        date_text, day_text, prayer_size, switch_font, adhan_text, iqamah_text, adhan_size = date, day, 42, "Roboto", "Adhan", "Iqamah", 27
    else:
        date_text, day_text, prayer_size, switch_font, adhan_text, iqamah_text, adhan_size = hijri, day_ar, 54, "Roboto", "أذان", "إقامة", 39
        # date_text, day_text, prayer_size, switch_font, adhan_text, iqamah_text, adhan_size = date, day, 42, "Roboto", "Adhan", "Iqamah", 27
    
    # Updating date
    update_label(date_label, "date_text", date_text)
    update_label(day_label, "day_text", day_text)

    # Time labels
    currenttime_labels[0].configure(text=f"{displayCurrentTime}")
    currenttime_labels[1].configure(text=f"{displayCurrentTime_s}")
    currenttime_labels[2].configure(text=f"{displayCurrentTime_meridian}")

    adhan_label.configure(text=adhan_text, font=(switch_font, adhan_size, "normal"))
    iqamah_label.configure(text=iqamah_text, font=(switch_font, adhan_size, "normal"))
    
    # Update Prayer Times - Using indices rather than repeated lookup
    for i in [0, 2, 3, 4, 5]:
        sel = prayer_headers[i]
        update_label(prayer_labels[i], f"prayer_{i}", prayer_headers[i] if toggle_state else prayer_headers_ar[i])
        update_label(act_time_labels[i], f"act_time_{i}", display_act_times[sel])
        update_label(iqama_time_labels[i], f"iqama_time_{i}", display_iqama_times[sel]) 
    # Cache for previously updated indices

    update_highlights(currentTime)
    
    update_label(status_labels[0], "status_0", prayer_headers[1] if toggle_state else prayer_headers[6])
    update_label(status_labels[1], "status_1", display_act_times["Sunrise"] if toggle_state else display_act_times["Midnight"])
    update_label(status_labels[2], "status_2", prayer_headers_ar[1] if toggle_state else prayer_headers_ar[6])

    # current_memory, peak_memory = tracemalloc.get_traced_memory()
    # print(f"Current memory usage: {current_memory / 1024:.2f} KB; Peak: {peak_memory / 1024:.2f} KB")

    # Track CPU usage
    # cpu_usage = psutil.cpu_percent(interval=0.1)  # Non-blocking
    # print(f"CPU Usage: {cpu_usage}%")

    root.update_idletasks()  # Forces all idle tasks to update at once
    root.after(100, update_display)

my_image = ctk.CTkImage(light_image=Image.open("Images/ISoc (black).png"),
                                  dark_image=Image.open("Images/ISoc (white).png"),
                                  size=(100, 50))
image_label = ctk.CTkLabel(info_frame, image=my_image, text="")
image_label.pack(expand=True, pady=(20,40))

date_label = ctk.CTkLabel(master=info_frame, font=("Roboto", 24))
date_label.pack(expand=True)

day_label = ctk.CTkLabel(master=info_frame, font=("Roboto", 18))
day_label.pack(expand=True, ipady=40)

currenttime_labels = {}

# Create a info_frame that spans columns 1 and 2
time_frame = ctk.CTkFrame(master=info_frame, fg_color=(light, dark))
time_frame.pack(fill='none',expand=False)

# Add elements to the container frame using `grid()`
# 150 time, 
currenttime_labels[0] = ctk.CTkLabel(master=time_frame, font=("Roboto", 100, "bold")) 
currenttime_labels[0].grid(row=0, column=2, padx=(0, 5), pady=10)

currenttime_labels[1] = ctk.CTkLabel(master=time_frame, font=("Roboto", 36, "bold"))
currenttime_labels[1].grid(row=0, column=3, padx=(5, 5), pady=10)

currenttime_labels[2] = ctk.CTkLabel(master=time_frame, font=("Roboto", 36, "normal"))
currenttime_labels[2].grid(row=0, column=4, padx=(5, 5), pady=10)
ctk.CTkLabel(time_frame, text="").grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
ctk.CTkLabel(time_frame, text="").grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

# Configure columns to handle layout expansion and centering
time_frame.columnconfigure((0,1,3,4), weight=1, uniform='a')  # Empty column for spacing on the left
time_frame.columnconfigure(2, weight=2)
time_frame.rowconfigure(0, weight=0)

# Create a info_frame that spans columns 1 and 2
noti_frame = ctk.CTkFrame(master=info_frame, fg_color=(light, dark))
noti_frame.pack(fill='x', expand=True)

notice = ctk.CTkLabel(noti_frame, font=("Roboto", 24, "bold"), text_color=("maroon", "red"))
notice.pack(padx=10, pady=5)

# Prayers Frame
# Grid headers
adhan_label = ctk.CTkLabel(rows_frame)
adhan_label.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
ctk.CTkLabel(rows_frame, text="").grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
iqamah_label = ctk.CTkLabel(rows_frame)
iqamah_label.grid(row=0, column=2, padx=10, pady=5, sticky="nsew")

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
    prayer_labels[i] = ctk.CTkLabel(master=rows_frame,  font=("Roboto", 36))
    prayer_labels[i].grid(row=row_counter, column=1, pady=6, sticky="nsew")
    
    act_time_labels[i] = ctk.CTkLabel(master=rows_frame, font=("Roboto", 48))
    act_time_labels[i].grid(row=row_counter, column=0, pady=6, sticky="nsew")
    
    iqama_time_labels[i] = ctk.CTkLabel(master=rows_frame, font=("Roboto", 48))
    iqama_time_labels[i].grid(row=row_counter, column=2, pady=6, sticky="nsew")
    
    row_counter += 1  # Increment row counter for the next set of labels


status_labels[0] = ctk.CTkLabel(master=rows_frame, font=("Roboto", 36), fg_color=("#969696", "#383838"))
status_labels[0].grid(row=row_counter, column=0, columnspan=1, pady=12, padx=0, sticky="nsew")
status_labels[1] = ctk.CTkLabel(master=rows_frame, font=("Roboto", 36), fg_color=("#969696", "#383838"))
status_labels[1].grid(row=row_counter, column=1, columnspan=1, pady=12, padx=0, sticky="nsew")
status_labels[2] = ctk.CTkLabel(master=rows_frame, font=("Roboto", 42), fg_color=("#969696", "#383838"))
status_labels[2].grid(row=row_counter, column=2, columnspan=1, pady=12, padx=0, sticky="nsew")

# Call the schedule_daily_update function once to start the periodic updates
update_date()
schedule_daily_update()
root.mainloop()
