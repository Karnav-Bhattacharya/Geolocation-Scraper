# Geolocation Scraper

## Overview
This project automates the extraction of latitude and longitude coordinates for a list of locations using Selenium and web scraping techniques. The script processes location names, searches them on [GeoNames](https://www.geonames.org/advanced-search.html), and retrieves the coordinates.

---

## Features
- Reads location names from an input file.
- Automatically opens a browser and searches each location.
- Extracts latitude and longitude from the search results.
- Writes the results to an output file in a structured format.
- Handles errors such as missing or incomplete data.

---

## Prerequisites
Ensure the following tools are installed:
- **Python** (>=3.8)
- **Google Chrome** (latest version)
- **ChromeDriver** (compatible with your Chrome version)

Install the required Python libraries using:

```bash
pip install -r requirements.txt
```

---

## File Structure
- `geolocation_scraper.py` : Main script for extracting geolocation data.
- `location.txt` : Input file containing location names (one per line).
- `coordinates.txt` : Output file where results are saved.
- `requirements.txt` : List of required Python libraries.

---

## Update the File Paths
Open `geolocation_scraper.py` and ensure the paths for the following variables are correct:

- **ChromeDriver**:
    ```python
    CHROME_DRIVER_PATH = r'C:\Path\to\chromedriver.exe'
    ```
- **Input file**:
    ```python
    INPUT_FILE = 'location.txt'
    ```
- **Output file**:
    ```python
    OUTPUT_FILE = 'coordinates.txt'
    ```

---

## Input Data
Add location names into `location.txt`. Use one location name per line:

Example:
```plaintext
Vishakhapatnam Village
Chippada Viillage
Madhurawada Villages
```

---

## Running the Project
To execute the script, run the following command:

```bash
python geolocation_scraper.py
```

### How It Works:
1. The script opens Chrome using Selenium.
2. It searches for each location name from `location.txt` on the [GeoNames](https://www.geonames.org/advanced-search.html) website.
3. It retrieves the latitude and longitude (if available).
4. Results are written to `coordinates.txt` in this format:

**Output Example:**
```plaintext
Vishakhapatnam, 17°40′48″, 83.201389
Chippada, 20°47′27″, 85.3025
```

---

## Example Workflow
### Input (location.txt):
```plaintext
Vishakhapatnam Village
Chippada Village
Dawarkapuram and Palepolam
```

### Output (coordinates.txt):
```plaintext
Vishakhapatnam, 17°40′48″, 83.201389
Chippada, 20°47′27″, 85.3025
Dawarkapuram, 15°32′45″, 80.123456
Palepolam, 15°31′40″, 80.120987
```

---

## Error Handling
- **Invalid Data**: If a location cannot be found, the script logs an empty entry in `coordinates.txt`.
- **Missing Table**: If the expected data table is not found, the script will skip the location.
- **Timeout**: If the search page takes too long to load, an error will be printed to the console, and the script continues with the next location.

Example Output for Errors:
```plaintext
Dawarkapuram, ,
Palepolam, 15°31′40″, 80.120987
```

---

## Notes
- If you're not using a virtual environment, run `pip freeze > requirements.txt` directly in your project folder to capture the exact dependencies.
- Ensure ChromeDriver is compatible with your Chrome version. Download the correct version [here](https://chromedriver.chromium.org/downloads).

---

## Future Enhancements
- Add support for alternative geolocation APIs.
- Implement retry logic for failed searches.
- Improve logging and error reporting.

---

## Author
- Karnav Bhattacharya
- email: bhattacharyakarnav@gmail.com

---

## License
This project is licensed under the Apache License 2.0.
