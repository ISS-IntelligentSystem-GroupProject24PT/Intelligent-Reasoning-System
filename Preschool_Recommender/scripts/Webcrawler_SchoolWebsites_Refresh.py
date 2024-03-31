import time
from Webcrawler_SchoolWebsites_Functions import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

PAGE_WAIT_TIME = 2

OUTPUT_HREF_SEARCH = 'SchoolPages_Preschool_href.csv'
TEMP_OUTPUT_HREF_SEARCH = 'Temp_SchoolPages_Preschool_href.csv'

PAGE_SOURCE_DIRECTORY_NAME = "..//resources//SchoolPages//SchoolPage_Page_Source"
PAGE_LINKS_DIRECTORY_NAME = "..//resources//SchoolPages//SchoolPage_Website_Links"

if not os.path.exists(PAGE_SOURCE_DIRECTORY_NAME):
    os.mkdir(PAGE_SOURCE_DIRECTORY_NAME)

if not os.path.exists(PAGE_LINKS_DIRECTORY_NAME):
    os.mkdir(PAGE_LINKS_DIRECTORY_NAME)

output_href_search = os.path.join(PAGE_LINKS_DIRECTORY_NAME, OUTPUT_HREF_SEARCH)
temp_output_href_search = os.path.join(PAGE_LINKS_DIRECTORY_NAME, TEMP_OUTPUT_HREF_SEARCH)

# Set the display options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Set chrome webdriver options
options = Options()
options.add_argument("--headless")  # Run in headless mode
driver = webdriver.Chrome(options=options)  # Pass the options argument

df_href_results = pd.read_csv(output_href_search).drop_duplicates()
df_href_refresh = pd.read_csv(output_href_search).drop_duplicates()
page_source_files = get_page_source_files(PAGE_SOURCE_DIRECTORY_NAME)
list_of_domains_skip = ['linkedin', 'facebook', 'google', 'yahoo', 'twitter', 'pinterest', 'nan', 'goo.gl', 'skoolopedia']

print(len(df_href_refresh['href'].drop_duplicates()))
for school_website in df_href_refresh['href'][::-1].drop_duplicates():
    if any(substring in school_website for substring in list_of_domains_skip):
        print(f"Not School Site: {school_website}")
    else:
        try:
            driver.get(school_website)
        except Exception as e:
            print(f"{school_website} - {e}")
        preschool_website_link = driver.current_url
        print(f"{school_website}")
        time.sleep(PAGE_WAIT_TIME)
        save_page_source(driver, preschool_website_link, PAGE_SOURCE_DIRECTORY_NAME)

# Close the driver
driver.quit()
