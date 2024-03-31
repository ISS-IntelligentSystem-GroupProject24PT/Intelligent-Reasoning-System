import time

from Webcrawler_SchoolWebsites_Functions import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import datetime

PAGE_WAIT_TIME = 2

INPUT_HREF_REFRESH = 'Preschool_href_Refresh.csv'
OUTPUT_HREF_REFRESH = 'Preschool_href.csv'
TEMP_OUTPUT_HREF_REFRESH = 'Temp_Preschool_href_Refresh.csv'

PAGE_SOURCE_DIRECTORY_NAME = "SchoolPage_Page_Source"
PAGE_LINKS_DIRECTORY_NAME = "SchoolPage_Website_Links"
ARCHIVES_DIRECTORY_NAME = "SchoolPage_Refresh_Archives"

OUTPUT_HREF_REFRESH_WITH_DATE = f"Preschool_List_Refresh_{datetime.now().date()}.csv"
TEMP_OUTPUT_HREF_REFRESH_WITH_DATE = f"Google_Reviews_Output_Refresh_{datetime.now().date()}.csv"

if not os.path.exists(PAGE_SOURCE_DIRECTORY_NAME):
    os.mkdir(PAGE_SOURCE_DIRECTORY_NAME)

if not os.path.exists(PAGE_LINKS_DIRECTORY_NAME):
    os.mkdir(PAGE_LINKS_DIRECTORY_NAME)

if not os.path.exists(ARCHIVES_DIRECTORY_NAME):
    os.mkdir(ARCHIVES_DIRECTORY_NAME)

output_href_refresh = os.path.join(PAGE_LINKS_DIRECTORY_NAME, OUTPUT_HREF_REFRESH)
temp_output_href_refresh = os.path.join(PAGE_LINKS_DIRECTORY_NAME, TEMP_OUTPUT_HREF_REFRESH)
output_href_refresh_with_date = os.path.join(ARCHIVES_DIRECTORY_NAME, OUTPUT_HREF_REFRESH_WITH_DATE)
temp_output_href_refresh_with_date = os.path.join(ARCHIVES_DIRECTORY_NAME, TEMP_OUTPUT_HREF_REFRESH_WITH_DATE)

# Set the display options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Set chrome webdriver options
options = Options()
options.add_argument("--headless")  # Run in headless mode
driver = webdriver.Chrome(options=options)  # Pass the options argument

# Get Preschool Websites
df_href_refresh = pd.read_csv(INPUT_HREF_REFRESH).drop_duplicates()

# Create DataFrame
df_href_results = pd.read_csv(output_href_refresh).drop_duplicates()
save_to_csv(df_href_results, temp_output_href_refresh)

for preschool_name, school_website in zip(df_href_results['Preschool_Name'],df_href_results['href']):
    driver.get(school_website)
    print(school_website)
    time.sleep(PAGE_WAIT_TIME)
    save_page_source(driver, school_website, PAGE_SOURCE_DIRECTORY_NAME)
    get_href_in_page(driver, output_href_refresh, preschool_name)
    get_href_in_page(driver, temp_output_href_refresh, preschool_name)

df_href_results = pd.read_csv(output_href_refresh)
save_to_csv(dataframe=df_href_results, output_file_=output_href_refresh_with_date)

df_href_results_temp = pd.read_csv(temp_output_href_refresh)
save_to_csv(dataframe=df_href_results_temp, output_file_=temp_output_href_refresh_with_date)

# Close the driver
driver.quit()
