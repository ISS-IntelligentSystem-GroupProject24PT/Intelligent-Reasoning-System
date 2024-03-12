from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup
import time

SCROLL_PAUSE_TIME = 1
PAGE_WAIT_TIME = 5
INPUT_FILE = 'Preschool_List.csv'
TEMP_INPUT_FILE = 'Temp_Preschool_List.csv'
OUTPUT_FILE_REVIEWS = 'google_reviews_output.csv'
OUTPUT_FILE_LINKS = 'google_links_output.csv'

# NOTE: FOR TROUBLESHOOTING TO KEEP WINDOW OPEN
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option('detach', True)
# driver = webdriver.Chrome(options=chrome_options)


# Initialize the Chrome driver
driver = webdriver.Chrome()


def wait_for_class_name_clickable(chromedriver, class_name):
    wait = WebDriverWait(chromedriver, timeout=PAGE_WAIT_TIME).until(
        EC.element_to_be_clickable((By.CLASS_NAME, class_name)))
    return wait


def wait_for_xpath_clickable(chromedriver, xpath):
    wait = WebDriverWait(chromedriver, timeout=PAGE_WAIT_TIME).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    wait.click()
    return wait


def click_review_tab(chromedriver):
    try:
        wait_for_xpath_clickable(chromedriver=chromedriver, xpath='//button[@jslog="145620; track:click;"]')
    except Exception as e:
        print(f"An error occurred for click_review_tab: {e}")


def scroll_down(chromedriver, xpath):
    try:
        anchor = chromedriver.find_element(By.XPATH, xpath)
        for i in range(10):
            anchor.send_keys(Keys.END)
            time.sleep(SCROLL_PAUSE_TIME)
    except Exception as e:
        print(f"An error occurred for scroll_down: {e}")


def click_see_more(chromedriver):
    try:
        while True:
            wait_for_xpath_clickable(chromedriver=chromedriver, xpath='//button[@aria-label="See more"]')
    except Exception as e:
        print(f"An error occurred for click_see_more: {e}")


def get_page_source():
    page_source = driver.page_source
# Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    return soup


def get_search_output():
    try:
        soup = get_page_source()
        preschools = soup.find_all('a', class_='hfpxzc')
        preschool_names = [preschool_name.get('aria-label') for preschool_name in preschools]
        print(preschool_names)
        return preschool_names
    except Exception as e:
        print(f"An error occurred for get_search_output): {e}")


def load_entire_search_page(chromedriver):
    try:
        scroll_down(chromedriver=chromedriver,
                    xpath='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]')

    except Exception as e:
        print(f"An error occurred for load_first_page): {e}")


def load_entire_review_page(chromedriver):
    click_review_tab(chromedriver)
    scroll_down(chromedriver=chromedriver, xpath='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')
    click_see_more(chromedriver)


def scrape_google_overview(chromedriver, search_terms):
    try:
        google_website_ = chromedriver.current_url
        soup = get_page_source()
        # EXTRACT ADDRESS
        address_ = soup.find('button', attrs={'aria-label': True, 'class': "CsEnBe"})['aria-label']
        address_ = address_.replace('Address: ', '')
        # EXTRACT OPENING HOURS
        opening_hours_ = soup.find('div', attrs={'aria-label': True, 'class': "t39EBf GUrTXd"})['aria-label']
        opening_hours_ = opening_hours_.replace(". Hide open hours for the week", '').replace("\u202f", '').replace("; ", ";").split(';')
        # EXTRACT PRESCHOOL WEBSITE
        preschool_website_ = soup.find('a', attrs={'aria-label': True, 'class': "CsEnBe"})['href']
        # EXTRACT LOCATION TYPE
        location_type_ = soup.find('button', attrs={'jsaction': True, 'class': "DkEaL"}).text
        return google_website_, address_, opening_hours_, preschool_website_, location_type_
    except Exception as e:
        print(f"An error occurred for scrape_google_reviews: {e}")


def scrape_google_reviews(chromedriver, search_terms):
    try:
        google_website_ = chromedriver.current_url
        soup = get_page_source()
# Extract review texts
        reviews = soup.find_all('div', class_='MyEned')
        review_comment_ = [review.find('span').text.replace("\n", ' ') for review in reviews if
                           review.find('span')]
# Extract stars
        stars = soup.find_all('div', class_='DU9Pgb')
# Extract review texts
        stars_number_ = [
            int(star.find('span', attrs={'aria-label': True})['aria-label'].replace(' stars', '').replace(' star', ''))
            for star in stars if star.find('span', attrs={'aria-label': True})]
# Calculate average stars
        try:
            avg_star_ = sum(stars_number_) / len(stars_number_)
        except ZeroDivisionError:
            avg_star_ = 0
        return google_website_, search_terms, review_comment_, stars_number_, avg_star_
    except Exception as e:
        print(f"An error occurred for scrape_google_reviews: {e}")


def save_to_csv(dataframe, output_file_):
    try:
        dataframe.to_csv(path_or_buf=output_file_, index=False)
    except Exception as e:
        print(f"An error occurred for save_to_csv: {e}")


# Create table labels
df_extraction_results = pd.DataFrame(
    columns=['Preschool_Name', 'Location_Type', 'Address', 'Opening_Hours', 'Preschool_Website', 'Review_Comments', 'Stars', 'Average_Stars', 'Google_Website', 'Update_Time'])
df_link_results = pd.DataFrame(columns=['Preschool_Name', 'Google_Website'])

# Copy search into a temp file
df_original = pd.read_csv(INPUT_FILE)
save_to_csv(df_original, TEMP_INPUT_FILE)
df = pd.read_csv(TEMP_INPUT_FILE).drop_duplicates()  # Get preschools

# Loop search terms and newly found search terms
for index, preschool in df['Preschool_Name'].items():
    if preschool in df_original:
        print(f"Repeated! {preschool}")
    else:
        df = pd.read_csv(TEMP_INPUT_FILE).drop_duplicates()  # Get preschools
        driver.get(f"https://www.google.com/maps/search/{preschool}")  # Search preschool on Google
        time.sleep(PAGE_WAIT_TIME)  # Wait for page to load
        websites = driver.current_url  # Get current page url
# Extract & Append to Google Links Output
        df_link_results = pd.read_csv(OUTPUT_FILE_LINKS).drop_duplicates()  # Get previous outputs
        new_link_result_row = pd.DataFrame({
            'Preschool_Name': [preschool],
            'Google_Website': [websites]
        })
        df_link_results = pd.concat([df_link_results, new_link_result_row], ignore_index=True).drop_duplicates()  #
# Combine into df
        save_to_csv(df_link_results, OUTPUT_FILE_LINKS)  # Save into file links
        print(websites)
# Extract & Append New Search Terms to Input File
        if 'search' in websites:
            try:
                load_entire_search_page(driver)
                new_search_terms = get_search_output()
                new_values = [search_value for search_value in new_search_terms if
                              search_value not in df['Preschool_Name'].values]
                df = pd.concat([df, pd.DataFrame(new_values, columns=['Preschool_Name'])], ignore_index=True)
            except Exception as e:
                print(f"An error occurred for search_page_loop: {e}")
        else:
# Extract & Append Google Reviews Output
            try:
                google_website, address, opening_hours, preschool_website, location_type = scrape_google_overview(driver,preschool)
                load_entire_review_page(driver)
                google_website, search_term, review_comment, star, avg_star = scrape_google_reviews(driver, preschool)
                new_row = pd.DataFrame({
                    'Preschool_Name': [search_term],
                    'Location_Type': [location_type],
                    'Address': [address],
                    'Opening_Hours': [opening_hours],
                    'Preschool_Website': [preschool_website],
                    'Review_Comments': [review_comment],
                    'Stars': [star],
                    'Average_Stars': [avg_star],
                    'Google_Website': [google_website],
                    'Update_Time': [datetime.now()]
                })
                print(new_row)
                df_extraction_results = pd.concat([df_extraction_results, new_row], ignore_index=True)
                save_to_csv(df_extraction_results, OUTPUT_FILE_REVIEWS)
            except Exception as e:
                print(f"An error occurred for scrape_google_reviews_loop: {e}")
# Remove searched value
    print(df_extraction_results)
    value_to_remove = preschool
    df = df[df['Preschool_Name'] != value_to_remove]
    save_to_csv(df, TEMP_INPUT_FILE)

# Close the browser
driver.quit()
