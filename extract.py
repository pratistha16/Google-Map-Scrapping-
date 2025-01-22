from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Constants
output_filename = "D:/Tuna Technology/GoogleMapsScrapping/dairies_in_nepal.txt"  # Changed filename
link = "https://www.google.com/maps/search/dairies+in+nepal/@27.6801848,83.4265621,12z/data=!3m1!4b1?entry=ttu&g_ep=EgoyMDI0MTAyMy4wIKXMDSoASAFQAw%3D%3D"

# Setup Selenium with Firefox and GeckoDriver
service = Service("C:/Users/panth/Downloads/geckodriver-v0.35.0-win64/geckodriver.exe")  # Path to geckodriver
driver = webdriver.Firefox(service=service)
driver.get(link)

# Wait for the main container to load
wait = WebDriverWait(driver, 20)
try:
    main_container = wait.until(EC.presence_of_element_located((By.ID, "app-container")))
except Exception as e:
    print(f"Error locating main container: {e}")
    driver.quit()
    exit()

# Scroll to load more elements if necessary
for _ in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)

# Locate search result elements within the main container using the specified class selector
try:
    search_results = main_container.find_elements(By.CSS_SELECTOR, ".m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ecceSd")
except Exception as e:
    print(f"Error locating search results: {e}")
    search_results = []

# Open the text file for writing
with open(output_filename, "w", encoding="utf-8") as file:
    # Extract text from each result and write to the file
    for result in search_results:
        try:
            # Get all text content from the result element
            result_text = result.text
            
            # Write the text content to the file
            file.write(result_text + "\n\n")  # Add extra line breaks for readability
        except Exception as e:
            print(f"Error extracting data from a result: {e}")

# Close driver
driver.quit()

print(f"Data saved to {output_filename}")
