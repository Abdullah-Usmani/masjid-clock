# Import Module
from tkinter import *
from timeChecker import *
from PIL import Image
import customtkinter as ctk

# %%
df, prayer_headers, iqama_headers, currentMYT = initializers(8)
selectedRow, date, hijri, day, headers, foundFlag = dateComparer(df, prayer_headers, currentMYT)
currentTime, displayCurrentTime, act_times, iqama_times, display_act_times, display_iqama_times, current_prayer, next_prayer= timeComparer(selectedRow, df, prayer_headers, iqama_headers, currentMYT)


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()

root.title("Prayer Times - ISOC 24/25")
root.geometry('720x1080')

my_image = ctk.CTkImage(light_image=Image.open("Images/ISoc (black).png"),
                                  dark_image=Image.open("Images/ISoc (white).png"),
                                  size=(30, 30))
image_label = ctk.CTkLabel(root, image=my_image, text="")

frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)


label = ctk.CTkLabel(master=frame, text=f"Prayer Times", font=("Roboto", 24))
label.pack(pady=12, padx=10)



if foundFlag == True:
    label = ctk.CTkLabel(master=frame, text=f"{date} | {hijri}", font=("Roboto", 48))
    label.pack(pady=12, padx=10)
    label = ctk.CTkLabel(master=frame, text=f"{day}", font=("Roboto", 32))
    label.pack(pady=6, padx=10)
    # print(f"{date} | {hijri}")
    # print(f"{day}")

if foundFlag == False:
    print("XX:XX - UPDATE REQUIRED")


currenttime_label = ctk.CTkLabel(master=frame, text=f"{displayCurrentTime}", font=("Roboto", 48))
currenttime_label.pack(pady=30, padx=10)
# label = ctk.CTkLabel(master=frame, text=f"{current_prayer} is now!", font=("Roboto", 32))
# label.pack(pady=12, padx=10)
# label = ctk.CTkLabel(master=frame, text=f"Next: {display_times[next_prayer]}", font=("Roboto", 32))
# label.pack(pady=12, padx=10)

prayer_labels = {}

for i in range(len(prayer_headers)):
    if i == 1:
        continue  # Skip the element at index 2
    sel = prayer_headers[i]
    prayer_labels[i] = ctk.CTkLabel(master=frame, text=f"{prayer_headers[i]} - {display_act_times[sel]} : {display_iqama_times[sel]}", font=("Roboto", 32))
    prayer_labels[i].pack(pady=12, padx=10)

if currentTime < act_times[next_prayer]:  # Compare current time with the actual time

    label = ctk.CTkLabel(master=frame, text=f"{next_prayer} is next!", font=("Roboto", 32))
    label.pack(pady=12, padx=10)
elif currentTime > act_times['Isyak']:
    # print(f"{current_prayer} is now!")
    # print(f"next_prayer: {display_times[next_prayer]}")
    # print(f"Fajr is next_prayer!")
    label = ctk.CTkLabel(master=frame, text=f"Fajr is next!", font=("Roboto", 32))
    label.pack(pady=12, padx=10)

# # adding a label to the root window
# lbl = Label(root, text = "Prayer Times")
# lbl.grid()

# adding Entry Field
txt = ctk.CTkEntry(master=frame, placeholder_text="Testing")


# function to display user text when 
# button is clicked
# def clicked():

#     res = "You wrote" + txt.get()
#     label.configure(text = res)

# # button widget with red color text inside
# btn = ctk.CTkButton(root, text = "Click me" , fg = "red", command=clicked)
# # Set Button Grid
# btn.grid(column=2, row=0)

# Execute Tkinter
root.mainloop()
