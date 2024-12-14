import re
import pandas as pd

# Updated DMS to Decimal function
def dms_to_decimal(coordinate, row_number=None):
    try:
        # Check for NaN or empty coordinates
        if not isinstance(coordinate, str) or not coordinate.strip():
            print(f"Skipping row {row_number}: Empty or NaN value.")
            return None

        # Updated regex to handle various characters and formats
        match = re.match(
            r"([NSWE])\s*(\d+)\s*[°]\s*(\d+)\s*[′’']?\s*(\d+(?:\.\d+)?)?\s*[″’’''\s]?",
            coordinate.strip()
        )

        if not match:
            print(f"Failed to match regex for row {row_number}: '{coordinate.strip()}'")
            return None

        direction, degrees, minutes, seconds = match.groups()
        degrees = int(degrees)
        minutes = int(minutes)
        seconds = float(seconds) if seconds else 0.0  # Handle missing seconds

        # Convert to decimal degrees
        decimal = degrees + (minutes / 60) + (seconds / 3600)

        # Make it negative for South or West directions
        if direction in ['S', 'W']:
            decimal = -decimal

        return decimal
    except Exception as e:
        print(f"Error processing coordinate (row {row_number}): {coordinate}. Error: {e}")
        return None


# Read the file
custom_columns = ['Location', 'Latitude', 'Longitude']
coordinates = pd.read_csv(
    r'C:\Code\Geolocation Scraper\coordinates.txt',
    header=None,
    names=custom_columns,
    skiprows=1,
    encoding='utf-8'
)

# Apply function with row number tracking
for idx, row in coordinates.iterrows():
    coordinates.at[idx, 'Latitude'] = dms_to_decimal(row['Latitude'], row_number=idx)
    coordinates.at[idx, 'Longitude'] = dms_to_decimal(row['Longitude'], row_number=idx)

# Handle empty or failed rows
coordinates.dropna(subset=['Latitude', 'Longitude'], inplace=True)

# Optionally, print out the updated DataFrame
pd.set_option('display.max_rows', None)
print(coordinates.head())

latitude_list = coordinates['Latitude'].tolist()
longitude_list = coordinates['Longitude'].tolist()
location_list = coordinates['Location'].tolist()

print(f"Locations: {len(location_list)}, Latitudes: {len(latitude_list)}, Longitudes: {len(longitude_list)}")