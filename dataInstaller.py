from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

# Initialize the Chrome WebDriver
try:
    driver = webdriver.Chrome()
    driver.get("https://www.e-solat.gov.my/index.php?siteId=24&pageId=24#")

    # Wait until the table element is present on the page
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))

    # Get the page source
    page_source = driver.page_source

finally:
    # Ensure the browser quits even if an error occurs
    driver.quit()

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, "html.parser")

# Find all table rows
rows = soup.find_all("tr")

# Create a DataFrame to store prayer times
dataFrame = pd.DataFrame(columns=['Date', 'Hijri', 'Day', 'Imsak', 'Fajr', 'Syuruk', 'Zohor', 'Asar', 'Maghrib', 'Isyak'])

# Extract data from rows and populate the DataFrame
for row in rows[1:]:  # Skip the header row
    th_tags = row.find_all("th")
    td_tags = row.find_all("td")

    individualRowData = []

    # Extract data from <th> tags
    for th in th_tags:
        individualRowData.append(th.text.strip())

    # Extract data from <td> tags
    for td in td_tags:
        individualRowData.append(td.text.strip())

    # Append the data to the DataFrame
    length = len(dataFrame)
    dataFrame.loc[length] = individualRowData
    print(f"{individualRowData}")

# Save the DataFrame to a CSV file
dataFrame.to_csv('./prayerTimes.csv', index=False)

print("Prayer times have been successfully saved to prayerTimes.csv.")
