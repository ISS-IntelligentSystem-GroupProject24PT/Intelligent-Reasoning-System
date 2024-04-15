import os
from datetime import datetime
import pandas as pd
import re


def initialise_reviews():
    from Processor_GoogleMapsReviews import GoogleMapsReviews


def convert_time(time_str):
    if time_str == 'Closed':
        hours = 'Closed'
        minutes = ''
    else:
        time_str_no_am_no_pm = time_str.replace('am', '').replace('pm', '')
        if ':' in time_str_no_am_no_pm:
            time_parts = time_str_no_am_no_pm.split(":")
            if 'pm' in time_str and int(time_parts[0]) == 12:
                hours = int(time_parts[0])
            elif 'am' in time_str and int(time_parts[0]) == 12:
                hours = 0
            elif 'pm' in time_str:
                hours = int(time_parts[0]) + 12
            else:
                hours = int(time_parts[0])
            minutes = int(time_parts[1]) / 60
        else:
            if '12pm' in time_str:
                hours = int(time_str_no_am_no_pm)
            elif '12am' in time_str:
                hours = 0
            elif 'pm' in time_str:
                hours = int(time_str_no_am_no_pm) + 12
            else:
                hours = int(time_str_no_am_no_pm)
            minutes = 0
    return hours + minutes


INPUT_FILE_EXCEL = 'Google_Reviews_Output.csv'
INPUT_FILE_TXT = 'Google_Reviews_Output.txt'
OUTPUT_FILE = 'ProcessedGoogleMaps_Output.csv'
INPUT_FILE_EXCEL_WITH_DATE = f"Google_Reviews_Output_{datetime.now().date()}.csv"
INPUT_FILE_TXT_WITH_DATE = f"Google_Reviews_Output_{datetime.now().date()}.txt"
OUTPUT_FILE_WITH_DATE = f"ProcessedGoogleMaps_Output_{datetime.now().date()}.csv"
REVIEW_OUTPUT_FILE = '6_Topics_ProcessedGoogleMaps_Output_Reviews.csv'

INPUT_DIRECTORY_NAME = "..//resources//ProcessedGoogleMaps//ProcessedGoogleMaps_Input_Files"
OUTPUT_DIRECTORY_NAME = "..//resources//ProcessedGoogleMaps//ProcessedGoogleMaps_Output_Files"
ARCHIVES_DIRECTORY_NAME = "..//resources//ProcessedGoogleMaps//ProcessedGoogleMaps_Archives"
PROCESSED_DIRECTORY_NAME = "..//resources//BusinessRulesEngine//BusinessRulesEngine_Input_Files"

# Set up directory
if not os.path.exists(OUTPUT_DIRECTORY_NAME):
    os.mkdir(OUTPUT_DIRECTORY_NAME)

if not os.path.exists(ARCHIVES_DIRECTORY_NAME):
    os.mkdir(ARCHIVES_DIRECTORY_NAME)

input_file_excel = os.path.join(INPUT_DIRECTORY_NAME, INPUT_FILE_EXCEL)
input_file_txt = os.path.join(INPUT_DIRECTORY_NAME, INPUT_FILE_TXT)
output_file = os.path.join(OUTPUT_DIRECTORY_NAME, OUTPUT_FILE)
processed_output_file = os.path.join(PROCESSED_DIRECTORY_NAME, OUTPUT_FILE)
input_file_excel_with_date = os.path.join(ARCHIVES_DIRECTORY_NAME, INPUT_FILE_EXCEL_WITH_DATE)
input_file_txt_with_date = os.path.join(ARCHIVES_DIRECTORY_NAME, INPUT_FILE_TXT_WITH_DATE)
output_file_with_date = os.path.join(ARCHIVES_DIRECTORY_NAME, OUTPUT_FILE_WITH_DATE)
review_output_file = os.path.join(OUTPUT_DIRECTORY_NAME, REVIEW_OUTPUT_FILE)

# Set the display options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Read input files
df_structured_input_file = pd.read_csv(input_file_excel)
df_unstructured_input_file = pd.read_csv(input_file_txt)

# Processing for Latitude & Longitude
google_websites = df_structured_input_file[['Preschool_Name', 'Google_Website']]
df_lat_long = pd.DataFrame(columns=['Preschool_Name', 'Preschool_Latitude', 'Preschool_Longitude'])

for index, row in google_websites.iterrows():
    preschool_name = row['Preschool_Name']
    google_website = row['Google_Website']
    geocoordinates = google_website.split('/')[6]
    latitude = geocoordinates.split(',')[0].replace("@", '')
    longitude = geocoordinates.split(',')[1]
    lat_long_row = pd.DataFrame({
        'Preschool_Name': [preschool_name],
        'Preschool_Latitude': [latitude],
        'Preschool_Longitude': [longitude]
    })
    df_lat_long = pd.concat([df_lat_long, lat_long_row], ignore_index=True).drop_duplicates()

# Processing for Opening Hours (7am = 7.0, 7pm = 19.0, 7:30am = 7.5)
opening_hours = df_structured_input_file[['Preschool_Name', 'Opening_Hours']]

df_opening_hours = pd.DataFrame(columns=[
    'Preschool_Name',
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
    'Saturday_End',
    'Sunday_Start_Number',
    'Sunday_End_Number',
    'Monday_Start_Number',
    'Monday_End_Number',
    'Tuesday_Start_Number',
    'Tuesday_End_Number',
    'Wednesday_Start_Number',
    'Wednesday_End_Number',
    'Thursday_Start_Number',
    'Thursday_End_Number',
    'Friday_Start_Number',
    'Friday_End_Number',
    'Saturday_Start_Number',
    'Saturday_End_Number'
])

for index, row in opening_hours.iterrows():
    preschool_name = row['Preschool_Name']
    opening_hour = row['Opening_Hours']
    if isinstance(opening_hour, str):
        try:
            opening_hour = re.sub('to (\d{1,2})pm, (\d{1,2}) to', 'to', opening_hour)
            opening_hour = re.sub('to (\d{1,2})am, (\d{1,2}) to', 'to', opening_hour)
            opening_hour = opening_hour.replace('Hours might differ,', '')
            opening_hour = opening_hour.replace('(Good Friday)', '')
            opening_hour = opening_hour.replace('Holiday hours,', '')
            opening_hour = opening_hour.replace('Open 24 hours', 'Closed')
            opening_hour = opening_hour.replace(' ', '')
            # Putting into a dictionary of day and timing
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            schedule_list = opening_hour.split(',')
            schedule_dict = {}
            for i in range(0, len(schedule_list), 2):
                day = schedule_list[i]
                if schedule_list[i + 1] == 'Closed':
                    schedule_dict[day + '_Start'] = 'Closed'
                    schedule_dict[day + '_End'] = 'Closed'
                else:
                    start_time, end_time = schedule_list[i + 1].split('to')
                    # Keep as AM, PM
                    if 'am' in start_time or 'pm' in start_time:
                        schedule_dict[day + '_Start'] = start_time
                    else:
                        if 'am' in end_time:
                            schedule_dict[day + '_Start'] = start_time + 'am'
                        elif 'pm' in end_time:
                            schedule_dict[day + '_Start'] = start_time + 'pm'
                        else:
                            schedule_dict[day + '_Start'] = start_time
                    schedule_dict[day + '_End'] = end_time
            # Ensure all days are in the dictionary
            for day in days:
                if day + '_Start' not in schedule_dict:
                    schedule_dict[day + '_Start'] = 'Closed'
                    schedule_dict[day + '_End'] = 'Closed'

            opening_hour_row = pd.DataFrame({
                'Preschool_Name': [preschool_name],
                'Sunday_Start': [schedule_dict.get('Sunday_Start', 'null')],
                'Sunday_End': [schedule_dict.get('Sunday_End', 'null')],
                'Monday_Start': [schedule_dict.get('Monday_Start', 'null')],
                'Monday_End': [schedule_dict.get('Monday_End', 'null')],
                'Tuesday_Start': [schedule_dict.get('Tuesday_Start', 'null')],
                'Tuesday_End': [schedule_dict.get('Tuesday_End', 'null')],
                'Wednesday_Start': [schedule_dict.get('Wednesday_Start', 'null')],
                'Wednesday_End': [schedule_dict.get('Wednesday_End', 'null')],
                'Thursday_Start': [schedule_dict.get('Thursday_Start', 'null')],
                'Thursday_End': [schedule_dict.get('Thursday_End', 'null')],
                'Friday_Start': [schedule_dict.get('Friday_Start', 'null')],
                'Friday_End': [schedule_dict.get('Friday_End', 'null')],
                'Saturday_Start': [schedule_dict.get('Saturday_Start', 'null')],
                'Saturday_End': [schedule_dict.get('Saturday_End', 'null')],
                'Sunday_Start_Number': [convert_time(schedule_dict.get('Sunday_Start', 'null'))],
                'Sunday_End_Number': [convert_time(schedule_dict.get('Sunday_End', 'null'))],
                'Monday_Start_Number': [convert_time(schedule_dict.get('Monday_Start', 'null'))],
                'Monday_End_Number': [convert_time(schedule_dict.get('Monday_End', 'null'))],
                'Tuesday_Start_Number': [convert_time(schedule_dict.get('Tuesday_Start', 'null'))],
                'Tuesday_End_Number': [convert_time(schedule_dict.get('Tuesday_End', 'null'))],
                'Wednesday_Start_Number': [convert_time(schedule_dict.get('Wednesday_Start', 'null'))],
                'Wednesday_End_Number': [convert_time(schedule_dict.get('Wednesday_End', 'null'))],
                'Thursday_Start_Number': [convert_time(schedule_dict.get('Thursday_Start', 'null'))],
                'Thursday_End_Number': [convert_time(schedule_dict.get('Thursday_End', 'null'))],
                'Friday_Start_Number': [convert_time(schedule_dict.get('Friday_Start', 'null'))],
                'Friday_End_Number': [convert_time(schedule_dict.get('Friday_End', 'null'))],
                'Saturday_Start_Number': [convert_time(schedule_dict.get('Saturday_Start', 'null'))],
                'Saturday_End_Number': [convert_time(schedule_dict.get('Saturday_End', 'null'))]
            })
            df_opening_hours = (pd.concat([df_opening_hours, opening_hour_row], ignore_index=True)
                                .drop_duplicates(subset='Preschool_Name'))
        except Exception as e:
            print(f"Not in hours format - {e}")
            print(opening_hour)
    else:
        print('empty')

# Combine Files
compiled_output_file = (pd.merge(df_structured_input_file, df_lat_long,
                                 on='Preschool_Name', how='left', indicator=True)
                        .drop(columns=['_merge'])).drop_duplicates(subset='Preschool_Name')
compiled_output_file = (pd.merge(compiled_output_file, df_opening_hours,
                                 on='Preschool_Name', how='left', indicator=True)
                        .drop(columns=['_merge'])).drop_duplicates(subset='Preschool_Name')

# Save output files
df_structured_input_file.to_csv(path_or_buf=input_file_excel_with_date, index=False)
df_unstructured_input_file.to_csv(path_or_buf=input_file_txt_with_date, index=False)
compiled_output_file.to_csv(path_or_buf=output_file, index=False)
compiled_output_file.to_csv(path_or_buf=output_file_with_date, index=False)
compiled_output_file.to_csv(path_or_buf=processed_output_file, index=False)
print('Process 1 done!')

# Review Processing
df_review_file = pd.read_csv(review_output_file)
initialise_reviews()
compiled_output_file = (pd.merge(compiled_output_file, df_review_file,
                                 on='Preschool_Name', how='left', indicator=True)
                        .drop(columns=['_merge'])).drop_duplicates(subset='Preschool_Name')

# Save output files
df_structured_input_file.to_csv(path_or_buf=input_file_excel_with_date, index=False)
df_unstructured_input_file.to_csv(path_or_buf=input_file_txt_with_date, index=False)
compiled_output_file.to_csv(path_or_buf=output_file, index=False)
compiled_output_file.to_csv(path_or_buf=output_file_with_date, index=False)
compiled_output_file.to_csv(path_or_buf=processed_output_file, index=False)
