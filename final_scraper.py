from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import time

# Constants
URL = "https://www.geonames.org/advanced-search.html?q=&country=IN&featureClass=P&continentCode=AS&fuzzy=0.6"
CHROME_DRIVER_PATH = r'C:\Program Files\chromedriver-win64\chromedriver.exe'
INPUT_FILE = "location.txt"
OUTPUT_FILE = "coordinates.txt"

# Initialize WebDriver
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)

import re

def read_locations(file_path):
    """Reads and processes location data from a file."""
    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()

    # Split the text into lines and process each line
    locations = []
    for line in data.splitlines():
        # Strip quotation marks and whitespace
        line = line.strip().strip('"').strip("'")

        # Remove common misspellings of "Village" using regex
        line = re.sub(r"V[iu]*l+l?ages?", "", line, flags=re.IGNORECASE).strip()
        # Split on "and" and commas to extract individual location names
        for part in line.split(" and "):
            first_part = part.split(",")[0].strip()  # Take the first part before a comma
            locations.append(first_part)

    return locations


# Example usage

# Join and print in desired format


def search_location(driver, location):
    """Searches for a location using the search input on the website."""
    try:
        search_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_input.clear()
        search_input.send_keys(location)
        search_input.send_keys(Keys.RETURN)
    except Exception as e:
        print(f"Error during search for location '{location}': {e}")
        return False
    return True

def extract_coordinates(driver, location):
    """Extracts coordinates from the second table on the results page."""
    try:
        tables = driver.find_elements(By.CLASS_NAME, "restable")
        if len(tables) < 2:
            print(f"Second table not found for location: {location}")
            return None, None

        second_table = tables[1]
        rows = second_table.find_elements(By.TAG_NAME, "tr")

        if len(rows) > 2:  # Ensure at least 3 rows (header + 2 data rows)
            row = rows[2]  # Third row (index 2)
            cells = row.find_elements(By.TAG_NAME, "td")

            if len(cells) >= 6:  # Ensure the row has at least 6 columns
                latitude = cells[4].text.strip()
                longitude = cells[5].text.strip()
                return latitude, longitude

        print(f"Not enough data in the table for location: {location}")
    except Exception as e:
        print(f"Error extracting coordinates for location '{location}': {e}")

    return None, None

def write_coordinates(file_path, location, latitude, longitude):
    """Writes coordinates to the output file."""
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(f"{location}, {latitude or ''}, {longitude or ''}\n")

def main():
    locations = read_locations(INPUT_FILE)

    try:
        driver.get(URL)

        for location in locations:
            print(f"Processing location: {location}")

            # Search for the location
            if not search_location(driver, location):
                write_coordinates(OUTPUT_FILE, location, None, None)
                continue

            # Wait for the search results to load
            time.sleep(5)  # Optional: Can be optimized based on page load time

            # Extract coordinates
            latitude, longitude = extract_coordinates(driver, location)

            # Write to file
            write_coordinates(OUTPUT_FILE, location, latitude, longitude)

    finally:
        driver.quit()
        print("Processing complete. WebDriver closed.")

if __name__ == "__main__":
    main()