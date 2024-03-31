import pandas as pd

from Webcrawler_GoogleMaps_Functions import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

INPUT_FILE_REFRESH = 'Preschool_List_Refresh.csv'

OUTPUT_FILE_LINKS_SEARCH = 'Google_Links_Output_Search.csv'
OUTPUT_FILE_REVIEWS_SEARCH = 'Google_Reviews_Output_Search.csv'
OUTPUT_FILE_REVIEWS_TEXT_SEARCH = 'Google_Reviews_Output_Search.txt'

OUTPUT_FILE_REVIEWS_REFRESH = 'Google_Reviews_Output_Refresh.csv'
OUTPUT_FILE_LINKS_REFRESH = 'Google_Links_Output_Refresh.csv'
OUTPUT_FILE_REVIEWS_TEXT_REFRESH = 'Google_Reviews_Output_Refresh.txt'

INPUT_FILE_REFRESH_WITH_DATE = f"Preschool_List_Refresh_{datetime.now().date()}.csv"
OUTPUT_FILE_REVIEWS_REFRESH_WITH_DATE = f"Google_Reviews_Output_Refresh_{datetime.now().date()}.csv"
OUTPUT_FILE_LINKS_REFRESH_WITH_DATE = f"Google_Links_Output_Refresh_{datetime.now().date()}.csv"
OUTPUT_FILE_REVIEWS_TEXT_REFRESH_WITH_DATE = f"Google_Reviews_Output_Refresh_{datetime.now().date()}.txt"

OUTPUT_FILE_LINKS = 'Google_Links_Output.csv'
OUTPUT_FILE_REVIEWS = 'Google_Reviews_Output.csv'
OUTPUT_FILE_REVIEWS_TEXT = 'Google_Reviews_Output.txt'

TEMP_FILES_DIRECTORY_NAME = "..//resources//GoogleMaps//GoogleMaps_Refresh_Temp_Files"
MAIN_FILES_DIRECTORY_NAME = "..//resources//GoogleMaps//GoogleMaps_Refresh_Main_Files"
ARCHIVES_DIRECTORY_NAME = "..//resources//GoogleMaps//GoogleMaps_Refresh_Archives"
COMPILED_DIRECTORY_NAME = "..//resources//GoogleMaps//GoogleMaps_Compiled_Files"
INPUT_DIRECTORY_NAME = "..//resources//GoogleMaps//GoogleMaps_Input_Files"

SEARCH_MAIN_FILES_DIRECTORY_NAME = "..//resources//GoogleMaps//GoogleMaps_Search_Main_Files"
PROCESSED_INPUT_DIRECTORY_NAME = "..//resources//ProcessedGoogleMaps//ProcessedGoogleMaps_Input_Files"

if not os.path.exists(TEMP_FILES_DIRECTORY_NAME):
    os.mkdir(TEMP_FILES_DIRECTORY_NAME)

if not os.path.exists(MAIN_FILES_DIRECTORY_NAME):
    os.mkdir(MAIN_FILES_DIRECTORY_NAME)

if not os.path.exists(ARCHIVES_DIRECTORY_NAME):
    os.mkdir(ARCHIVES_DIRECTORY_NAME)

# Set the display options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

input_file_refresh = os.path.join(INPUT_DIRECTORY_NAME, INPUT_FILE_REFRESH)

output_file_reviews_search = os.path.join(SEARCH_MAIN_FILES_DIRECTORY_NAME, OUTPUT_FILE_REVIEWS_SEARCH)
output_file_links_search = os.path.join(SEARCH_MAIN_FILES_DIRECTORY_NAME, OUTPUT_FILE_LINKS_SEARCH)
output_file_reviews_text_search = os.path.join(SEARCH_MAIN_FILES_DIRECTORY_NAME, OUTPUT_FILE_REVIEWS_TEXT_SEARCH)

output_file_reviews_refresh = os.path.join(MAIN_FILES_DIRECTORY_NAME, OUTPUT_FILE_REVIEWS_REFRESH)
output_file_links_refresh = os.path.join(MAIN_FILES_DIRECTORY_NAME, OUTPUT_FILE_LINKS_REFRESH)
output_file_reviews_text_refresh = os.path.join(MAIN_FILES_DIRECTORY_NAME, OUTPUT_FILE_REVIEWS_TEXT_REFRESH)

input_file_refresh_with_date = os.path.join(ARCHIVES_DIRECTORY_NAME, INPUT_FILE_REFRESH_WITH_DATE)

output_file_reviews_refresh_with_date = os.path.join(ARCHIVES_DIRECTORY_NAME, OUTPUT_FILE_REVIEWS_REFRESH_WITH_DATE)
output_file_links_refresh_with_date = os.path.join(ARCHIVES_DIRECTORY_NAME, OUTPUT_FILE_LINKS_REFRESH_WITH_DATE)
output_file_reviews_text_refresh_with_date = os.path.join(ARCHIVES_DIRECTORY_NAME, OUTPUT_FILE_REVIEWS_TEXT_REFRESH_WITH_DATE)

output_file_links = os.path.join(COMPILED_DIRECTORY_NAME, OUTPUT_FILE_LINKS)
output_file_reviews = os.path.join(COMPILED_DIRECTORY_NAME, OUTPUT_FILE_REVIEWS)
output_file_reviews_text = os.path.join(COMPILED_DIRECTORY_NAME, OUTPUT_FILE_REVIEWS_TEXT)

processed_input_file_links = os.path.join(PROCESSED_INPUT_DIRECTORY_NAME, OUTPUT_FILE_LINKS)
processed_input_file_reviews = os.path.join(PROCESSED_INPUT_DIRECTORY_NAME, OUTPUT_FILE_REVIEWS)
processed_input_file_reviews_text = os.path.join(PROCESSED_INPUT_DIRECTORY_NAME, OUTPUT_FILE_REVIEWS_TEXT)

# Set chrome webdriver options
options = Options()
options.add_argument("--headless")  # Run in headless mode
driver = webdriver.Chrome(options=options)  # Pass the options argument

# Create table labels
try:
    df_review = pd.read_csv(output_file_reviews_refresh)
except Exception as e:
    df_review = pd.DataFrame(
        columns=['Preschool_Name', 'Location_Type', 'Address', 'Opening_Hours', 'Preschool_Website',
                 'Stars', 'Average_Stars', 'Google_Website', 'Update_Time'])
    save_to_csv(df_review, output_file_reviews_refresh)  # Save into file links

try:
    df_link_results = pd.read_csv(output_file_links_refresh)
except Exception as e:
    df_link_results = pd.DataFrame(columns=['Preschool_Name', 'Google_Website'])
    save_to_csv(df_link_results, output_file_links_refresh)  # Save into file links

try:
    df_review_comments = pd.read_csv(output_file_reviews_text_refresh)
except Exception as e:
    df_review_comments = pd.DataFrame(columns=['Preschool_Name', 'Review_Comments'])
    save_to_csv(df_review_comments, output_file_reviews_text_refresh)

df = pd.read_csv(input_file_refresh, encoding='latin-1')

for index, preschool in df["Preschool_Name"].items():
    driver.get(f"https://www.google.com/maps/search/{preschool}")  # Search preschool on Google
    time.sleep(PAGE_WAIT_TIME)  # Wait for page to load
    websites = driver.current_url  # Get current page url
    save_google_links(preschool, websites, output_file_links_refresh)
    print(websites)
    # Extract & Append New Search Terms to Input File
    if 'search' in websites:
        print('skip search')
    else:
        # Extract & Append Google Reviews Output
        try:
            google_overview = save_google_overview(chromedriver=driver, search_terms=preschool)
        except Exception as e:
            print(f"An error occurred for google_overview: {e}")
        google_reviews = pd.DataFrame({
            'Preschool_Name': [preschool]
        })
        try:
            google_reviews, google_star = save_google_reviews(chromedriver=driver, search_terms=preschool)
        except Exception as e:
            print(f"An error occurred for save_google_reviews: {e}")
        try:
            df_review_comments = pd.read_csv(output_file_reviews_text_refresh, sep=',')
            df_review_comments = pd.concat(objs=[convert_list_to_string(google_reviews), df_review_comments], ignore_index=True).drop_duplicates()
            save_to_csv(dataframe=df_review_comments, output_file_=output_file_reviews_text_refresh)
        except Exception as e:
            print(f"An error occurred for google_reviews: {e}")
        try:
            new_row = convert_list_to_string(pd.concat(objs=[google_overview, google_star], axis=1))
            print(new_row)
        except Exception as e:
            new_row = convert_list_to_string(pd.concat(objs=[google_overview], axis=1))
            print(f"An error occurred for google_overview or google_star: {e}")
        try:
            df_review = convert_list_to_string(df_review)
            df_review = pd.concat(objs=[new_row, df_review], ignore_index=True).drop_duplicates()
            save_to_csv(dataframe=df_review, output_file_=output_file_reviews_refresh)
        except Exception as e:
            print(f"An error occurred for save_to_csv_extracted_review_results: {e}")

# Save Results with Timestamp
df = pd.read_csv(input_file_refresh, encoding='latin-1')
save_to_csv(df, output_file_=input_file_refresh_with_date)

df_review = pd.read_csv(output_file_reviews_refresh)
save_to_csv(dataframe=df_review, output_file_=output_file_reviews_refresh_with_date)

df_link_results = pd.read_csv(output_file_links_refresh)
save_to_csv(df_link_results, output_file_=output_file_links_refresh_with_date)  # Save into file links

df_review_comments = pd.read_csv(output_file_reviews_text_refresh)
save_to_csv(df_link_results, output_file_=output_file_reviews_text_refresh_with_date)  # Save into file links

# Combine refresh & search results
df_link_results_all = pd.concat([pd.read_csv(output_file_links_search), df_link_results], ignore_index=True).drop_duplicates()
save_to_csv(df_link_results_all, output_file_=OUTPUT_FILE_LINKS)

df_review_all = pd.concat([pd.read_csv(output_file_reviews_search), df_review], ignore_index=True).drop_duplicates()
save_to_csv(df_review_all, output_file_=OUTPUT_FILE_REVIEWS)

df_review_comments_all = pd.concat([pd.read_csv(output_file_reviews_text_search), df_review_comments], ignore_index=True).drop_duplicates()
save_to_csv(df_review_comments_all, output_file_=OUTPUT_FILE_REVIEWS_TEXT)

# Close the browser
driver.quit()
