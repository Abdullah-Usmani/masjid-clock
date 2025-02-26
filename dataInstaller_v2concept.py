import requests
import csv

"Made this because I found the api link from inspecting the network tab of the website. Instead of parsing the data from a chrome instance"

url = "https://www.e-solat.gov.my/index.php?r=esolatApi/takwimsolat&period=year&zone=SGR03"  # Replace with your JSON URL
response = requests.get(url)

if response.status_code == 200:
    data = response.json()["prayerTime"]

    # Ensure data is a list of dictionaries
    if isinstance(data, dict):
        data = [data]  

    with open("prayerTimes_v2concept.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())  # Use JSON keys as headers
        writer.writeheader()
        writer.writerows(data)  # Write data rows

    # print("CSV file saved as data.csv")
else:
    # idk how the error handling works in this so this the default
    print(f"Failed to fetch data. Status code: {response.status_code}")