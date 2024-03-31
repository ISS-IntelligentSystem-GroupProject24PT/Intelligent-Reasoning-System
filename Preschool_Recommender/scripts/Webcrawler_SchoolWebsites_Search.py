import time

from Webcrawler_SchoolWebsites_Functions import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import datetime

PAGE_WAIT_TIME = 2

OUTPUT_FILE_REVIEWS_REFRESH = 'Google_Reviews_Output.csv'
OUTPUT_HREF_SEARCH = 'Preschool_href.csv'
TEMP_OUTPUT_HREF_SEARCH = 'Temp_Preschool_href_Search.csv'

PAGE_SOURCE_DIRECTORY_NAME = "SchoolPage_Page_Source"
PAGE_LINKS_DIRECTORY_NAME = "SchoolPage_Website_Links"
ARCHIVES_DIRECTORY_NAME = "SchoolPage_Search_Archives"
REFRESH_MAIN_FILES_DIRECTORY_NAME = "..\\resources\\Compiled"

OUTPUT_HREF_SEARCH_WITH_DATE = f"Preschool_List_Search_{datetime.now().date()}.csv"
TEMP_OUTPUT_HREF_SEARCH_WITH_DATE = f"Google_Reviews_Output_Search_{datetime.now().date()}.csv"

if not os.path.exists(PAGE_SOURCE_DIRECTORY_NAME):
    os.mkdir(PAGE_SOURCE_DIRECTORY_NAME)

if not os.path.exists(PAGE_LINKS_DIRECTORY_NAME):
    os.mkdir(PAGE_LINKS_DIRECTORY_NAME)

if not os.path.exists(ARCHIVES_DIRECTORY_NAME):
    os.mkdir(ARCHIVES_DIRECTORY_NAME)

output_href_search = os.path.join(PAGE_LINKS_DIRECTORY_NAME, OUTPUT_HREF_SEARCH)
temp_output_href_search = os.path.join(PAGE_LINKS_DIRECTORY_NAME, TEMP_OUTPUT_HREF_SEARCH)
output_href_search_with_date = os.path.join(ARCHIVES_DIRECTORY_NAME, OUTPUT_HREF_SEARCH_WITH_DATE)
temp_output_href_search_with_date = os.path.join(ARCHIVES_DIRECTORY_NAME, TEMP_OUTPUT_HREF_SEARCH_WITH_DATE)
output_file_reviews_refresh = os.path.join(REFRESH_MAIN_FILES_DIRECTORY_NAME, OUTPUT_FILE_REVIEWS_REFRESH)


# Set the display options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Set chrome webdriver options
options = Options()
options.add_argument("--headless")  # Run in headless mode
driver = webdriver.Chrome(options=options)  # Pass the options argument


# Restart Temp File
df_href_results_temp = pd.DataFrame(columns=['Preschool_Name', 'href', 'Page_Source'])
save_to_csv(df_href_results_temp, temp_output_href_search)

try:
    # Get Previous Result
    df_href_results = pd.read_csv(output_href_search).drop_duplicates()
    save_to_csv(df_href_results, output_href_search)
except Exception as e:
    save_to_csv(df_href_results_temp, output_href_search)
    df_href_results = pd.read_csv(output_href_search).drop_duplicates()

# Get Preschool Websites from Google Result
df_file_reviews_refresh = pd.read_csv(output_file_reviews_refresh).drop_duplicates()
df_school_websites = (pd.DataFrame({
    'Preschool_Name': [str(preschool_name) for preschool_name in df_file_reviews_refresh['Preschool_Name']],
    'href': [str(preschool_website)
                          .replace("www.", "")
                          .replace("https://", "")
                          .replace("http://", "")
                          .split('/')[0]
                          for preschool_website in df_file_reviews_refresh['Preschool_Website']]
    }).drop_duplicates())
print(df_school_websites)


# Remove search terms that are already extracted from href refresh
df_href_results_no_http = (pd.DataFrame({
    'href': [str(preschool_website)
                          .replace("www.", "")
                          .replace("https://", "")
                          .replace("http://", "")
                          .split('/')[0]
                          for preschool_website in df_href_results['href']]})
                           .drop_duplicates())
merged = pd.merge(df_school_websites, df_href_results_no_http, on='href', how='left', indicator=True)
df_school_websites = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge']).drop_duplicates()

print(df_school_websites)

page_source_files = get_page_source_files(PAGE_SOURCE_DIRECTORY_NAME)

list_of_domains_skip = ['linkedin', 'facebook', 'google', 'yahoo', 'twitter', 'pinterest', 'nan', 'goo.gl', 'skoolopedia']
for preschool_name, school_website in zip(df_school_websites['Preschool_Name'],df_school_websites['href']):
    df_href_results = pd.read_csv(output_href_search).drop_duplicates()
    if school_website in df_href_results['href']:
        print(f"Repeated {school_website}")
    elif any(substring in school_website for substring in list_of_domains_skip):
        print(f"Not School Site: {school_website}")
    else:
        get_website(driver, school_website)
        preschool_website_link = driver.current_url
        print(school_website)
        time.sleep(PAGE_WAIT_TIME)
        save_page_source(driver, preschool_website_link, PAGE_SOURCE_DIRECTORY_NAME)
        get_href_in_page(driver, output_href_search, preschool_name)
        get_href_in_page(driver, temp_output_href_search, preschool_name)

    temp_href_file = pd.read_csv(temp_output_href_search)
    while len(temp_href_file['href']) != 0:
        page_source_files = get_page_source_files(PAGE_SOURCE_DIRECTORY_NAME)
        temp_href_file = pd.read_csv(temp_output_href_search).drop_duplicates(subset='href')
        print(temp_href_file)
        for href_preschool_name, href, page_source in zip(temp_href_file['Preschool_Name'], temp_href_file['href'], temp_href_file['Page_Source']):
            if f"{page_source}.txt" in page_source_files:
                print(f"Repeated {href}")
            elif any(substring in href for substring in list_of_domains_skip):
                print(f"Not School Site: {href}")
            else:
                driver.get(href)
                print(href)
                time.sleep(PAGE_WAIT_TIME)
                get_href_in_page(driver, output_href_search, href_preschool_name)
                get_href_in_page(driver, temp_output_href_search, href_preschool_name)
                save_page_source(driver, href, PAGE_SOURCE_DIRECTORY_NAME)
            remove_current_search_term(href, temp_href_file, temp_output_href_search)
            df_href_results = pd.read_csv(output_href_search).drop_duplicates()
            save_to_csv(dataframe=df_href_results, output_file_=output_href_search)
            temp_href_file = pd.read_csv(temp_output_href_search).drop_duplicates(subset='href')
            page_source_files = get_page_source_files(PAGE_SOURCE_DIRECTORY_NAME)
            print(temp_href_file)
            print(page_source_files)

save_to_csv(dataframe=df_href_results, output_file_=output_href_search_with_date)

df_href_results_temp = pd.read_csv(temp_output_href_search).drop_duplicates()
save_to_csv(dataframe=df_href_results_temp, output_file_=temp_output_href_search_with_date)

# Close the driver
driver.quit()
