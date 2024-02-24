from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Start a WebDriver session
driver = webdriver.Chrome()
driver.get("https://www.e-solat.gov.my/index.php?siteId=24&pageId=24#")

# Add a delay to wait for the page to load
time.sleep(5)  # Adjust the delay time as needed

# Get the page source after it's been modified by JavaScript
page_source = driver.page_source

# Close the WebDriver session
driver.quit()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(page_source, "html.parser")

# Find all table rows except the first one
rows = soup.find_all("tr")

for row in rows:
    # Find all th and td tags within the current row
    th_tags = row.find_all("th")
    td_tags = row.find_all("td")
    
    # Print th tag text
    for th in th_tags:
        print(th.text.strip())

    # Print td tag text
    for td in td_tags:
        print(td.text.strip())

    # Separate rows by an empty line
    print("\nnext row\n")
