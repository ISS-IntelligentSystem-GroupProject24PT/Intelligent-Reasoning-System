from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
import time

PAGE_WAIT_TIME = 6
SCROLL_PAUSE_TIME = 1


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
        print(f"An error occurred for click_review_tab.")


def scroll_down(chromedriver, xpath):
    try:
        anchor = chromedriver.find_element(By.XPATH, xpath)
    except Exception as e:
        print(f"An error occurred for scroll_down.")
        return
    for i in range(10):
        anchor.send_keys(Keys.END)
        time.sleep(SCROLL_PAUSE_TIME)


def click_see_more(chromedriver):
    try:
        while True:
            wait_for_xpath_clickable(chromedriver=chromedriver, xpath='//button[@aria-label="See more"]')
    except Exception as e:
        print(f"An error occurred for click_see_more.")
        return


def get_page_source(chromedriver):
    page_source = chromedriver.page_source
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    return soup


def get_search_output(chromedriver):
    try:
        soup = get_page_source(chromedriver)
        preschools = soup.find_all('a', class_='hfpxzc')
        preschool_names = [preschool_name.get('aria-label') for preschool_name in preschools]
        return preschool_names
    except Exception as e:
        print(f"An error occurred for get_search_output: {e}")


def load_entire_search_page(chromedriver):
    try:
        scroll_down(chromedriver=chromedriver,
                    xpath='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]')
    except Exception as e:
        print(f"An error occurred for load_first_page): {e}")


def load_entire_review_page(chromedriver):
    try:
        click_review_tab(chromedriver)
    except Exception as e:
        print(f"An error occurred for load_entire_review_page (click review): {e}")
        return
    scroll_down(chromedriver=chromedriver, xpath='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')
    click_see_more(chromedriver)


def scrape_google_overview(chromedriver, search_terms):
    google_website_ = chromedriver.current_url
    soup = get_page_source(chromedriver)
    # EXTRACT ADDRESS
    try:
        address_button = soup.find(name='button', attrs={'aria-label': True, 'class': "CsEnBe"})
        address_ = address_button['aria-label'] if address_button is not None else ''
        address_ = address_.replace('Address: ', '')
    except Exception as e:
        print(f"An error occurred for scrape_google_overview (address): {e}")
    # EXTRACT OPENING HOURS
    try:
        opening_hours_div = soup.find(name='div', attrs={'aria-label': True, 'class': "t39EBf GUrTXd"})
        opening_hours_ = opening_hours_div['aria-label'] if opening_hours_div is not None else ''
        opening_hours_ = opening_hours_.replace(". Hide open hours for the week", '').replace("\u202f", '').replace(
            "; ", ";").split(';')
    except Exception as e:
        print(f"An error occurred for scrape_google_overview (opening hours): {e}")
    # EXTRACT PRESCHOOL WEBSITE
    try:
        preschool_website_a = soup.find(name='a', attrs={'aria-label': True, 'class': "CsEnBe"})
        preschool_website_ = preschool_website_a['href'] if preschool_website_a is not None else ''

    except Exception as e:
        print(f"An error occurred for scrape_google_overview (preschool website): {e}")
    # EXTRACT LOCATION TYPE
    try:
        location_type_ = soup.find(name='button', attrs={'jsaction': True, 'class': "DkEaL"}).text or ''
    except Exception as e:
        print(f"An error occurred for scrape_google_overview (location type): {e}")
    try:
        return google_website_, search_terms, address_, opening_hours_, preschool_website_, location_type_
    except Exception as e:
        print(f"An error occurred for scrape_google_overview: {e}")


def scrape_google_reviews(chromedriver, search_terms):
    google_website_ = chromedriver.current_url
    soup = get_page_source(chromedriver)
    # Extract review texts
    try:
        reviews = soup.find_all(name='div', class_='MyEned') or ''
        review_comment_ = [review.find('span').text.replace("\n", ' ') for review in reviews if
                           review.find('span')]
    except Exception as e:
        print(f"An error occurred for scrape_google_reviews (review comment): {e}")
    # Extract stars
    try:
        stars = soup.find_all(name='div', class_='DU9Pgb') or ''
        # Extract review texts
        stars_number_ = [
            int(star.find('span', attrs={'aria-label': True})['aria-label'].replace(' stars', '').replace(' star', ''))
            for star in stars if star.find('span', attrs={'aria-label': True})]
    except Exception as e:
        print(f"An error occurred for scrape_google_reviews (stars number): {e}")
    # Calculate average stars
    try:
        try:
            avg_star_ = sum(stars_number_) / len(stars_number_)
        except ZeroDivisionError:
            avg_star_ = 0
    except Exception as e:
        print(f"An error occurred for scrape_google_reviews (avg star): {e}")
    try:
        return google_website_, search_terms, review_comment_, stars_number_, avg_star_
    except Exception as e:
        print(f"An error occurred for scrape_google_reviews: {e}")


def convert_list_to_string(dataframe):
    dataframe = dataframe.map(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else ('' if x is None else x))
    return dataframe


def save_to_csv(dataframe, output_file_):
    try:
        # Convert lists to strings
        dataframe = convert_list_to_string(dataframe)
        dataframe.to_csv(path_or_buf=output_file_, index=False)
    except Exception as e:
        print(f"An error occurred for save_to_csv: {e}")


def save_google_overview(chromedriver, search_terms):
    google_website, search_term, address, opening_hours, preschool_website, location_type = scrape_google_overview(
        chromedriver, search_terms)
    new_google_overview_row = pd.DataFrame({
        'Preschool_Name': [search_term],
        'Location_Type': [location_type],
        'Address': [address],
        'Opening_Hours': [opening_hours],
        'Preschool_Website': [preschool_website],
        'Google_Website': [google_website],
        'Update_Time': [datetime.now()]
    })
    return new_google_overview_row


def save_google_reviews(chromedriver, search_terms):
    try:
        load_entire_review_page(chromedriver)
    except Exception as e:
        print(f"An error occurred for save_google_reviews: {e}")
        return
    google_website, search_term, review_comment, star, avg_star = scrape_google_reviews(chromedriver, search_terms)
    new_google_stars_row = pd.DataFrame({
        'Stars': [star],
        'Average_Stars': [avg_star]
    })
    new_google_reviews_row = pd.DataFrame({
        'Preschool_Name': [search_term],
        'Review_Comments': [review_comment]
    })
    return new_google_reviews_row, new_google_stars_row


def save_google_links(preschool, websites, output_file_):
    # Extract & Append to Google Links Output
    df_link_result = pd.read_csv(output_file_).drop_duplicates()  # Get previous outputs
    new_link_result_row = pd.DataFrame({
        'Preschool_Name': [preschool],
        'Google_Website': [websites]
    })
    df_link_result = pd.concat([df_link_result, new_link_result_row], ignore_index=True).drop_duplicates(keep='last')  #
    # Combine into df
    save_to_csv(df_link_result, output_file_)  # Save into file links


def save_new_search_terms(chromedriver, dataframe, output_file_):
    try:
        load_entire_search_page(chromedriver)
        new_search_term = get_search_output(chromedriver)
        new_values = [search_value for search_value in new_search_term if
                      search_value not in dataframe['Preschool_Name'].values]
        new_search_terms = pd.concat([dataframe, pd.DataFrame(new_values, columns=['Preschool_Name'])],
                                     ignore_index=True).drop_duplicates()
        save_to_csv(new_search_terms, output_file_)
    except Exception as e:
        print(f"An error occurred for save_new_search_terms: {e}")


def remove_current_search_term(search_terms, dataframe, input_file_):
    value_to_remove = search_terms
    dataframe = dataframe[dataframe['Preschool_Name'] != value_to_remove]
    save_to_csv(dataframe, input_file_)
