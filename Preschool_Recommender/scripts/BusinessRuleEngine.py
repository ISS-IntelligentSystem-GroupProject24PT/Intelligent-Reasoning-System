import math
def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    # Radius of earth in kilometers is about 6371
    km = 6371* c
    return km

import os
from datetime import datetime
import pandas as pd

INPUT_FILE_EXCEL = 'ProcessedGoogleMaps_Output.csv'
USER_INPUT_FILE = 'UserInput.csv'
OUTPUT_FILE = 'BusinessRuleEngine_Distance_OpeningHours.csv'
INPUT_FILE_EXCEL_WITH_DATE = f"ProcessedGoogleMaps_Output_{datetime.now().date()}.csv"
OUTPUT_FILE_WITH_DATE = f"BusinessRuleEngine_Distance_OpeningHours_{datetime.now().date()}.csv"

INPUT_DIRECTORY_NAME = "..//resources//BusinessRulesEngine//BusinessRulesEngine_Input_Files"
OUTPUT_DIRECTORY_NAME = "..//resources//BusinessRulesEngine//BusinessRulesEngine_Output_Files"
ARCHIVES_DIRECTORY_NAME = "..//resources//BusinessRulesEngine//BusinessRulesEngine_Archives"

# Set up directory
if not os.path.exists(INPUT_DIRECTORY_NAME):
    os.mkdir(INPUT_DIRECTORY_NAME)

if not os.path.exists(OUTPUT_DIRECTORY_NAME):
    os.mkdir(OUTPUT_DIRECTORY_NAME)

if not os.path.exists(ARCHIVES_DIRECTORY_NAME):
    os.mkdir(ARCHIVES_DIRECTORY_NAME)

input_file_excel = os.path.join(INPUT_DIRECTORY_NAME, INPUT_FILE_EXCEL)
user_input_file = os.path.join(INPUT_DIRECTORY_NAME, USER_INPUT_FILE)
output_file = os.path.join(OUTPUT_DIRECTORY_NAME, OUTPUT_FILE)
input_file_excel_with_date = os.path.join(ARCHIVES_DIRECTORY_NAME, INPUT_FILE_EXCEL_WITH_DATE)
output_file_with_date = os.path.join(ARCHIVES_DIRECTORY_NAME, OUTPUT_FILE_WITH_DATE)

# Set the display options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Read input files
processed_googlemaps = pd.read_csv(input_file_excel)
# user_input = pd.read_csv(user_input_file)

# Get preschool lat long
df_lat_long = processed_googlemaps[['Preschool_Name', 'Preschool_Latitude', 'Preschool_Longitude']]
# user_lat = user_input['User_Latitude']
# user_long = user_input['User_Longitude']
user_lat = 1.443452
user_long = 103.815545

# Distance Calculation
df_distance = pd.DataFrame(columns=['Preschool_Name', 'Preschool_Latitude', 'Preschool_Longitude', 'Distance_To_User_km'])
for index, row in df_lat_long.iterrows():
    preschool_name = row['Preschool_Name']
    preschool_latitude = row['Preschool_Latitude']
    preschool_longitude = row['Preschool_Longitude']
    distance = haversine(user_lat, user_long, preschool_latitude, preschool_longitude)
    distance_row = pd.DataFrame({
        'Preschool_Name': [preschool_name],
        'Preschool_Latitude': [preschool_latitude],
        'Preschool_Longitude': [preschool_longitude],
        'Distance_To_User_km': [distance]
    })
    df_distance = pd.concat([df_distance, distance_row], ignore_index=True).drop_duplicates()

# Save output files
processed_googlemaps.to_csv(path_or_buf=input_file_excel_with_date, index=False)
df_distance.to_csv(path_or_buf=output_file, index=False)
df_distance.to_csv(path_or_buf=output_file_with_date, index=False)
