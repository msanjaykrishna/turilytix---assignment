import pandas as pd
import re
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Load the data from the Excel files
address_df = pd.read_excel('/home/sanjay/Downloads/Address.xlsx')
area_status_df = pd.read_excel('/home/sanjay/Downloads/Area status.xlsx')

# Function to extract post code
def extract_post_code(address):
    match = re.search(r'\b\d{6}\b', address)  # Adjust regex as needed for the post code format
    return match.group() if match else None

# Initialize Nominatim API for geocoding
geolocator = Nominatim(user_agent="myGeocoder")
# Apply rate limiter to respect usage policy
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Function to geocode address
def geocode_address(address):
    try:
        location = geocode(address)
        return (location.latitude, location.longitude) if location else (None, None)
    except Exception as e:
        return (None, None)

# Extract post code from the address
address_df['Post Code'] = address_df['Address'].apply(extract_post_code)

# Geocode address to get latitude and longitude
address_df['Latitude'], address_df['Longitude'] = zip(*address_df['Address'].apply(geocode_address))

# Rename columns for merging
area_status_df.rename(columns={'Pincode': 'Post Code'}, inplace=True)
area_status_df['Post Code'] = area_status_df['Post Code'].astype(str)

# Merge the dataframes to include Area Status
merged_df = pd.merge(address_df, area_status_df, on='Post Code', how='left')

# Save the merged dataframe to an Excel file
merged_df.to_excel('outcome.xlsx', index=False)

print("The process is completed. The 'outcome.xlsx' file has been created.")
