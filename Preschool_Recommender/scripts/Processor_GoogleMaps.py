import os
from datetime import datetime
import pandas as pd
import numpy as np


INPUT_FILE_EXCEL = 'Google_Reviews_Output.csv'
INPUT_FILE_TXT = 'Google_Reviews_Output.txt'
OUTPUT_FILE = 'ProcessedGoogleMaps_Output.csv'
INPUT_FILE_EXCEL_WITH_DATE = f"Google_Reviews_Output_{datetime.now().date()}.csv"
INPUT_FILE_TXT_WITH_DATE = f"Google_Reviews_Output_{datetime.now().date()}.txt"
OUTPUT_FILE_WITH_DATE = f"ProcessedGoogleMaps_Output_{datetime.now().date()}.csv"

INPUT_DIRECTORY_NAME = "..//resources//ProcessedGoogleMaps//ProcessedGoogleMaps_Input_Files"
OUTPUT_DIRECTORY_NAME = "..//resources//ProcessedGoogleMaps//ProcessedGoogleMaps_Output_Files"
ARCHIVES_DIRECTORY_NAME = "..//resources//ProcessedGoogleMaps//ProcessedGoogleMaps_Archives"
COMPILED_DIRECTORY_NAME = "..//resources//Compiled"

# Set up directory
if not os.path.exists(OUTPUT_DIRECTORY_NAME):
    os.mkdir(OUTPUT_DIRECTORY_NAME)

if not os.path.exists(ARCHIVES_DIRECTORY_NAME):
    os.mkdir(ARCHIVES_DIRECTORY_NAME)

if not os.path.exists(COMPILED_DIRECTORY_NAME):
    os.mkdir(COMPILED_DIRECTORY_NAME)

input_file_excel = os.path.join(INPUT_DIRECTORY_NAME, INPUT_FILE_EXCEL)
input_file_txt = os.path.join(INPUT_DIRECTORY_NAME, INPUT_FILE_TXT)
output_file = os.path.join(OUTPUT_DIRECTORY_NAME, OUTPUT_FILE)
input_file_excel_with_date = os.path.join(ARCHIVES_DIRECTORY_NAME, INPUT_FILE_EXCEL_WITH_DATE)
input_file_txt_with_date = os.path.join(ARCHIVES_DIRECTORY_NAME, INPUT_FILE_TXT_WITH_DATE)
output_file_with_date = os.path.join(ARCHIVES_DIRECTORY_NAME, OUTPUT_FILE_WITH_DATE)

# Set the display options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Read input files
df_structured_input_file = pd.read_csv(input_file_excel)
df_unstructured_input_file = pd.read_csv(input_file_txt)

# Processing for Latitude & Longitude
google_websites = df_structured_input_file['Google_Website']

df_lat_long = pd.DataFrame(columns=['Google_Website','Latitude','Longitude'])

for google_website in google_websites:
    geocoordinates = google_website.split('/')[6]
    latitude = geocoordinates.split(',')[0].replace("@", '')
    longitude = geocoordinates.split(',')[1]
    lat_long_row = pd.DataFrame({
        'Google_Website': [google_website],
        'Latitude': [latitude],
        'Longitude': [longitude]
    })
    df_lat_long = pd.concat([df_lat_long, lat_long_row], ignore_index=True)

compiled_output_file = pd.merge(df_structured_input_file, df_lat_long, on='Google_Website', how='left', indicator=True).drop(columns=['_merge'])
# print(compiled_output_file.head())

# Processing for Opening Hours
opening_hours = df_structured_input_file['Opening_Hours']

df_opening_hours = pd.DataFrame(columns=[
    'Opening_Hours',
    'Sunday_Start',
    'Sunday_End',
    'Monday_Start',
    'Monday_End',
    'Tuesday_Start',
    'Tuesday_End',
    'Wednesday_Start',
    'Wednesday_End',
    'Thursday_Start',
    'Thursday_End',
    'Friday_Start',
    'Friday_End',
    'Saturday_Start',
    'Saturday_End'
])

for opening_hour in opening_hours:
    print(opening_hour)
    if isinstance(opening_hour, str) or np.isnan(opening_hours):
        print('empty')
    else:
        opening_hour_token = opening_hour.split(',')
        opening_hour_L1_dict = {opening_hour_token[i].strip(): opening_hour_token[i + 1].strip() for i in range(0, len(opening_hour_token), 2)}
        opening_hour_L2_dict = {}
        for day, hours in opening_hour_L1_dict.items():
            if hours != 'Closed':
                start, end = hours.split(' to ')
                opening_hour_L2_dict[f'{day}_Start'] = start
                opening_hour_L2_dict[f'{day}_End'] = end
        opening_hour_row = pd.DataFrame({
            'Opening_Hours': [opening_hour],
            'Sunday_Start': [opening_hour_L2_dict.get('Sunday_Start', '')],
            'Sunday_End': [opening_hour_L2_dict.get('Sunday_End', '')],
            'Monday_Start': [opening_hour_L2_dict.get('Monday_Start', '')],
            'Monday_End': [opening_hour_L2_dict.get('Monday_End', '')],
            'Tuesday_Start': [opening_hour_L2_dict.get('Tuesday_Start', '')],
            'Tuesday_End': [opening_hour_L2_dict.get('Tuesday_End', '')],
            'Wednesday_Start': [opening_hour_L2_dict.get('Wednesday_Start', '')],
            'Wednesday_End': [opening_hour_L2_dict.get('Wednesday_End', '')],
            'Thursday_Start': [opening_hour_L2_dict.get('Thursday_Start', '')],
            'Thursday_End': [opening_hour_L2_dict.get('Thursday_End', '')],
            'Friday_Start': [opening_hour_L2_dict.get('Friday_Start', '')],
            'Friday_End': [opening_hour_L2_dict.get('Friday_End', '')],
            'Saturday_Start': [opening_hour_L2_dict.get('Saturday_Start', '')],
            'Saturday_End': [opening_hour_L2_dict.get('Saturday_End', '')]
        })
        df_opening_hours = pd.concat([df_opening_hours, opening_hour_row], ignore_index=True)
        print(df_opening_hours.head())
compiled_output_file = pd.merge(compiled_output_file, df_opening_hours, on='Opening_Hours', how='left', indicator=True).drop(columns=['_merge'])
print(compiled_output_file.head())

# Save output files
# structured_input_file.to_csv(path_or_buf=input_file_excel_with_date, index=False)
# unstructured_input_file.to_csv(path_or_buf=input_file_txt_with_date, index=False)
# compiled_output_file.to_csv(path_or_buf=output_file, index=False)
# compiled_output_file.to_csv(path_or_buf=output_file_with_date, index=False)
