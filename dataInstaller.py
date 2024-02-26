from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas

# Start a WebDriver session
driver = webdriver.Chrome()
driver.get("https://www.e-solat.gov.my/index.php?siteId=24&pageId=24#")

# Add a delay to wait for the page to load
time.sleep(15)  # Adjust the delay time as needed

# Get the page source after it's been modified by JavaScript
page_source = driver.page_source

# Close the WebDriver session
driver.quit()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(page_source, "html.parser")

# Find all table rows except the first one
rows = soup.find_all("tr")

dataFrame = pandas.DataFrame(columns=['Date', 'Hijri', 'Day', 'Imsak', 'Fajr', 'Syuruk', 'Zohor', 'Asar', 'Maghrib', 'Isyak'])

for row in rows[1:]:
    # Find all th and td tags within the current row
    th_tags = row.find_all("th")
    td_tags = row.find_all("td")
    
    # Print th tag text
    individualRowData = []
    for th in th_tags:
        # print(th.text.strip())
        individualRowData.append(th.text.strip())

    # Print td tag text
    for td in td_tags:
        # print(td.text.strip())
        individualRowData.append(td.text.strip())

    # Separate rows by an empty line
    # print("\nnext row\n")
    length = len(dataFrame)
    dataFrame.loc[length] = individualRowData
    print(f"{individualRowData}")

dataFrame.to_csv(r'C:\Users\Abdullah Usmani\Documents\MasjidClock\athan-plus-iqamah-time-clock\prayerTimes.csv')