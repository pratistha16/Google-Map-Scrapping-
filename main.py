from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

# Constants
filename = "data"
# Update the URL to search for hotels and restaurants in a specific area
link = "https://www.google.com/maps/search/hotels+and+resturants+/@27.6682089,83.4423029,13z/data=!3m1!4b1?entry=ttu&g_ep=EgoyMDI0MDkxNS4wIKXMDSoASAFQAw%3D%3D"
# If you need to include both hotels and restaurants, you could use:
# link = "https://www.google.com/maps/search/hotels+restaurants+in+Chicago,+IL,+USA/@41.8336478,-87.8720473,11z/data=!3m1!4b1"

# Setup Selenium
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
action = ActionChains(browser)

# Variables to store data
record = []
visited_names = set()  # Use set for faster lookup
max_retries = 20  # For detecting when scrolling stops
retry_counter = 0

def Selenium_extractor():
    global retry_counter

    # Find all result elements initially
    elements = browser.find_elements(By.CLASS_NAME, "hfpxzc")

    # Scroll until we have a sufficient number of results
    while len(elements) < 1000:
        prev_len = len(elements)
        print(f"Loaded {len(elements)} results")

        # Scroll the page
        scroll_origin = ScrollOrigin.from_element(elements[-1])
        action.scroll_from_origin(scroll_origin, 0, 1000).perform()
        time.sleep(2)  # Wait for new results to load

        # Update the list of elements
        elements = browser.find_elements(By.CLASS_NAME, "hfpxzc")

        # Break if no new elements were loaded after multiple retries
        if len(elements) == prev_len:
            retry_counter += 1
            if retry_counter >= max_retries:
                print("No more new results, exiting scroll loop.")
                break
        else:
            retry_counter = 0

    # Process each result
    for i, element in enumerate(elements):
        try:
            scroll_origin = ScrollOrigin.from_element(element)
            action.scroll_from_origin(scroll_origin, 0, 100).perform()
            action.move_to_element(element).perform()
            element.click()
            time.sleep(2)  # Wait for the details page to load

            # Parse the page source
            source = browser.page_source
            soup = BeautifulSoup(source, 'html.parser')

            # Extract name
            name_html = soup.find('h1', {"class": "DUwDvf fontHeadlineLarge"})
            if not name_html:
                continue

            name = name_html.text.strip()

            # If already visited, skip
            if name in visited_names:
                continue

            visited_names.add(name)

            # Extract phone, address, and website
            divs = soup.findAll('div', {"class": "Io6YTe fontBodyMedium"})
            phone = next((div.text for div in divs if div.text.startswith("+")), "Not available")
            address = divs[0].text if divs else "Not available"
            website = next((div.text for div in divs if div.text.endswith(".")), "Not available")

            # Store the data
            print([name, phone, address, website])
            record.append((name, phone, address, website))

            # Save data to CSV after every new entry
            df = pd.DataFrame(record, columns=['Name', 'Phone number', 'Address', 'Website'])
            df.to_csv(filename + '.csv', index=False, encoding='utf-8')

        except Exception as e:
            print(f"Error processing element {i}: {e}")
            continue

# Run the scraping process
try:
    browser.get(link)
    time.sleep(10)  # Let the page load fully
    Selenium_extractor()
finally:
    # Ensure the browser closes even if an error occurs
    browser.quit()
