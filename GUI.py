from tkinter import *
from timeChecker import *
from PIL import Image
import customtkinter as ctk
import datetime
import time

df, prayer_headers, prayer_headers_ar, iqama_headers = initializers()
selectedRow, date, hijri, day, day_ar, headers, foundFlag = dateComparer(df, prayer_headers, 8)
toggle_state = False

# Initialize the app and UI elements
ctk.set_appearance_mode("system")
# ctk.set_default_color_theme("green")
light = "#f2f4f5"
dark = "#212121"

root = ctk.CTk()

root.title("Prayer Times - ISOC 24/25")
root.geometry('720x1280+0+0')

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
# rows_frame.rowconfigure((0,6), weight = 1, uniform='a')




def get_milliseconds_until_midnight():
    now = time.gmtime()  
    now = time.localtime(time.mktime(now) + 6 * 3600)  
    now_datetime = datetime.datetime(year=now.tm_year, month=now.tm_mon, day=now.tm_mday,
                                     hour=now.tm_hour, minute=now.tm_min, second=now.tm_sec)
    midnight = datetime.datetime.combine(now_datetime.date() + datetime.timedelta(days=1), datetime.time(0, 0))
    remaining_time = midnight - now_datetime
    return int(remaining_time.total_seconds() * 1000)  # Convert seconds to milliseconds

def update_date():
    global selectedRow, date, hijri, day, day_ar, headers, foundFlag
    selectedRow, date, hijri, day, day_ar, headers, foundFlag = dateComparer(df, prayer_headers, 8)
    update_display()
    status_toggle()
    
    root.after(86400000, update_date)

def schedule_daily_update():
    milliseconds_until_midnight = get_milliseconds_until_midnight()
    root.after(milliseconds_until_midnight, update_date)


notice_text = ""

def input_dialog():
    dialog = ctk.CTkInputDialog(text="Enter a notice:", title="Notice Change")
    notice_text = dialog.get_input()  # waits for input
    return notice_text

# Function to be triggered by keybind or button
def show_dialog():
    global notice_text
    notice_text = input_dialog()  # Get input from the user and update the variable

# Bind the key (e.g., "d" key) to the dialog function
root.bind("<d>", lambda event: show_dialog())  # You can change "d" to any ke



def status_toggle():
    global toggle_state
    toggle_state = not toggle_state
    root.after(15000, status_toggle)

def update_display():
    currentTime, displayCurrentTime, displayCurrentTime_s, displayCurrentTime_meridian, act_times, iqama_times, display_act_times, display_iqama_times = timeComparer(selectedRow, df, prayer_headers, iqama_headers, 17)

    global notice_text

    # notice_text = "" if toggle_state else "ISHA DELAYED"
    # notice_text = ""
    # notice_text = "ISHA DELAYED"
    notice.configure(text=notice_text)

    # eng_size2 = 48
    # ar_size2 = 56
    # date_size = eng_size2 if toggle_state else ar_size2
    # switch_font = "Roboto" if toggle_state else "Simplified Arabic"
    switch_font = "Roboto"
    
    date_text = f"{date}" if toggle_state else f"{hijri}"
    date_label.configure(text=date_text, font=(switch_font, 48))
    day_eng_text=f"{day}"
    day_ar_text=f"{day_ar}"
    day_text = day_eng_text if toggle_state else day_ar_text
    day_label.configure(text=day_text, font=(switch_font, 32))

    currenttime_labels[0].configure(text=f"{displayCurrentTime}")
    currenttime_labels[1].configure(text=f"{displayCurrentTime_s}")
    currenttime_labels[2].configure(text=f"{displayCurrentTime_meridian}")

    for i in range(len(prayer_headers)):
        if i == 1:
            continue  # Skip the element at index 2
        if i == 6:
            continue  # Skip the element at index 2
        
        sel = prayer_headers[i]
        eng_text=f"{prayer_headers[i]}"
        ar_text=f"{prayer_headers_ar[i]}"
        prayer_text = eng_text if toggle_state else ar_text
        eng_size = 28
        ar_size = 36
        prayer_size = eng_size if toggle_state else ar_size
        prayer_labels[i].configure(text=prayer_text, font=(switch_font, prayer_size, "normal"))

        eng_size1 = 18
        ar_size1 = 26

        adhan_text = "Adhan" if toggle_state else "أذان"
        adhan_size = eng_size1 if toggle_state else ar_size1
        adhan_label.configure(text=adhan_text, font=(switch_font, adhan_size, "normal"))

        iqamah_text = "Iqamah" if toggle_state else "إقامة"
        iqamah_size = eng_size1 if toggle_state else ar_size1
        iqamah_label.configure(text=iqamah_text, font=(switch_font, iqamah_size, "normal"))
        
        # adhan_size = eng_size1 if toggle_state else ar_size1
        status_labels[2].configure(font=(switch_font, 28, "normal"))
        
        act_time_labels[i].configure(text=f"{display_act_times[sel]}", font=("Roboto", 36, "normal"))
        iqama_time_labels[i].configure(text=f"{display_iqama_times[sel]}", font=("Roboto", 36, "normal"))


    for i in range(len(prayer_headers)):
        next = prayer_headers[i]
        if i == 2:
            continue
        if i == 7:
            continue
        if currentTime < act_times['Midnight']:  # Compare current time with the actual time
            prayer_labels[5].configure(font=(switch_font, prayer_size, "bold"), fg_color="#946d2e", text_color="white")
            act_time_labels[5].configure(font=("Roboto", 36, "bold"), fg_color="#946d2e", text_color="white")
            iqama_time_labels[5].configure(font=("Roboto", 36, "bold"), fg_color="#946d2e", text_color="white")
            break
        if currentTime < act_times['Fajr']:  # Compare current time with the actual time
            break
        if currentTime < act_times['Dhuhr'] and i > 2:
            break
        elif currentTime < act_times[next]:  # Compare current time with the actual time
            prayer_labels[i-1].configure(font=(switch_font, prayer_size, "bold"), fg_color="#946d2e", text_color="white")
            act_time_labels[i-1].configure(font=("Roboto", 36, "bold"), fg_color="#946d2e", text_color="white")
            iqama_time_labels[i-1].configure(font=("Roboto", 36, "bold"), fg_color="#946d2e", text_color="white")
            break
        elif currentTime > act_times['Isha']:
            prayer_labels[5].configure(font=(switch_font, prayer_size, "bold"), fg_color="#946d2e", text_color="white")
            act_time_labels[5].configure(font=("Roboto", 36, "bold"), fg_color="#946d2e", text_color="white")
            iqama_time_labels[5].configure(font=("Roboto", 36, "bold"), fg_color="#946d2e", text_color="white")
            break

    new_text0 = f"{prayer_headers[1]}" if toggle_state else f"{prayer_headers[6]}"
    status_labels[0].configure(text=new_text0)
    new_text1 = f"{display_act_times['Sunrise']}" if toggle_state else f"{display_act_times['Midnight']}"
    status_labels[1].configure(text=new_text1)
    new_text2 = f"{prayer_headers_ar[1]}" if toggle_state else f"{prayer_headers_ar[6]}"
    status_labels[2].configure(text=new_text2)

    # Schedule the function to run again after 1 second (1000 milliseconds)
    root.after(500, update_display)



my_image = ctk.CTkImage(light_image=Image.open("Images/ISoc (black).png"),
                                  dark_image=Image.open("Images/ISoc (white).png"),
                                  size=(100, 50))
image_label = ctk.CTkLabel(info_frame, image=my_image, text="")
image_label.pack(expand=True, pady=(20,40))

date_label = ctk.CTkLabel(master=info_frame)
date_label.pack(expand=True)

day_label = ctk.CTkLabel(master=info_frame)
day_label.pack(expand=True, ipady=40)

currenttime_labels = {}

# Create a info_frame that spans columns 1 and 2
time_frame = ctk.CTkFrame(master=info_frame, fg_color=(light, dark))
time_frame.pack(fill='none',expand=False)

# Add elements to the container frame using `grid()`
currenttime_labels[0] = ctk.CTkLabel(master=time_frame, font=("Roboto", 100, "bold"))
currenttime_labels[0].grid(row=0, column=2, padx=(0, 5), pady=10)

currenttime_labels[1] = ctk.CTkLabel(master=time_frame, font=("Roboto", 24, "bold"))
currenttime_labels[1].grid(row=0, column=3, padx=(5, 5), pady=10)

currenttime_labels[2] = ctk.CTkLabel(master=time_frame, font=("Roboto", 24, "normal"))
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
    prayer_labels[i] = ctk.CTkLabel(master=rows_frame)
    prayer_labels[i].grid(row=row_counter, column=1, pady=6, sticky="nsew")
    
    act_time_labels[i] = ctk.CTkLabel(master=rows_frame, font=("Roboto", 32))
    act_time_labels[i].grid(row=row_counter, column=0, pady=6, sticky="nsew")
    
    iqama_time_labels[i] = ctk.CTkLabel(master=rows_frame, font=("Roboto", 32))
    iqama_time_labels[i].grid(row=row_counter, column=2, pady=6, sticky="nsew")
    
    row_counter += 1  # Increment row counter for the next set of labels



status_labels[0] = ctk.CTkLabel(master=rows_frame, font=("Roboto", 24), fg_color=("#969696", "#383838"))
status_labels[0].grid(row=row_counter, column=0, columnspan=1, pady=12, padx=0, sticky="nsew")
status_labels[1] = ctk.CTkLabel(master=rows_frame, font=("Roboto", 24), fg_color=("#969696", "#383838"))
status_labels[1].grid(row=row_counter, column=1, columnspan=1, pady=12, padx=0, sticky="nsew")
status_labels[2] = ctk.CTkLabel(master=rows_frame, fg_color=("#969696", "#383838"))
status_labels[2].grid(row=row_counter, column=2, columnspan=1, pady=12, padx=0, sticky="nsew")

# Call the schedule_daily_update function once to start the periodic updates
update_date()
schedule_daily_update()

# Execute Tkinter
root.mainloop()
