import os
from datetime import datetime
import pandas as pd

INPUT_FILE_EXCEL = 'ProcessedGoogleMaps_Output.csv'
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
output_file = os.path.join(OUTPUT_DIRECTORY_NAME, OUTPUT_FILE)
input_file_excel_with_date = os.path.join(ARCHIVES_DIRECTORY_NAME, INPUT_FILE_EXCEL_WITH_DATE)
output_file_with_date = os.path.join(ARCHIVES_DIRECTORY_NAME, OUTPUT_FILE_WITH_DATE)

# Set the display options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Read input files
