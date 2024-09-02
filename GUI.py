# Import Module
from tkinter import *
from timeChecker import *
import customtkinter as ctk
from PIL import Image

df, prayer_headers, currentMYT = initializers(8)
selectedRow, date, hijri, day, headers, foundFlag = dateComparer(df, prayer_headers, currentMYT)
currentTime, displayCurrentTime, act_times, display_times, current_prayer, next_prayer= timeComparer(selectedRow, df, prayer_headers, currentMYT)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()

root.title("Prayer Times - ISOC 24/25")
root.geometry('1280x720')

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
    label.pack(pady=12, padx=10)
    # print(f"{date} | {hijri}")
    # print(f"{day}")

if foundFlag == False:
    print("XX:XX - UPDATE REQUIRED")


label = ctk.CTkLabel(master=frame, text=f"Current: {displayCurrentTime}", font=("Roboto", 32))
label.pack(pady=12, padx=10)
label = ctk.CTkLabel(master=frame, text=f"{current_prayer} is now!", font=("Roboto", 32))
label.pack(pady=12, padx=10)
label = ctk.CTkLabel(master=frame, text=f"Next: {display_times[next_prayer]}", font=("Roboto", 32))
label.pack(pady=12, padx=10)

for i in range(len(prayer_headers)):  # Iterate over the prayer headers

    # next_prayer = prayer_headers[i]
    # currrent_prayer = prayer_headers[i-1]

    if currentTime < act_times[next_prayer]:  # Compare current time with the actual time
        # print(f"\nCurrent: {displayCurrentTime}")
        # print(f"{current_prayer} is now!")
        # print(f"next_prayer: {display_times[next_prayer]}")
        # print(f"{next_prayer} is next_prayer!")

        label = ctk.CTkLabel(master=frame, text=f"{next_prayer} is next!", font=("Roboto", 32))
        label.pack(pady=12, padx=10)
        break
    elif currentTime > act_times['Isyak']:
        # print(f"{current_prayer} is now!")
        # print(f"next_prayer: {display_times[next_prayer]}")
        # print(f"Fajr is next_prayer!")
        label = ctk.CTkLabel(master=frame, text=f"Fajr is next!", font=("Roboto", 32))
        label.pack(pady=12, padx=10)
        break

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
