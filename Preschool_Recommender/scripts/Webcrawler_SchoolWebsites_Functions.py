from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import os
import re


def get_website(chromedriver, school_website):
    # Open the website
    url = f"www.{school_website}"
    try:
        # Try with https first
        chromedriver.get(f"https://{url}")
    except WebDriverException:
        try:
            # If that fails, try with http
            chromedriver.get(f"http://{url}")
        except WebDriverException:
            print(f"Could not open {url} with either http or https.")


def get_page_source(chromedriver):
    page_source = chromedriver.page_source
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    return soup


def save_page_source(chromedriver, school_website, directory_name):
    try:
        # Get the page source
        page_source = chromedriver.page_source
        # Specify the name of the file to be created
        school_website_cleaned = re.sub(r'\W+', '_', school_website.replace('/', '_'))[:100]
        file_name = f"{school_website_cleaned}.txt"

        # Specify the full path to the file
        full_path = os.path.join(directory_name, file_name)
        # Save the page source to a text file
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(page_source)
    except Exception as e:
        print(f"page_source_failed: {e}")


def convert_list_to_string(dataframe):
    dataframe = dataframe.map(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else ('' if x is None else x))
    return dataframe


def save_to_csv(dataframe, output_file_):
    try:
        dataframe = convert_list_to_string(dataframe)
        dataframe.to_csv(path_or_buf=output_file_, index=False)
    except Exception as e:
        print(f"An error occurred for save_to_csv: {e}")


def remove_current_search_term(search_terms, dataframe, input_file_):
    value_to_remove = search_terms
    dataframe = dataframe[dataframe['href'] != value_to_remove]
    save_to_csv(dataframe, input_file_)


def get_href_in_page(chromedriver, output, preschool_name):
    try:
        website = chromedriver.current_url  # Get current page url
        # Find all the `<a>` tags
        elements = chromedriver.find_elements(By.TAG_NAME, 'a')
        # Loop through each element and print the href attribute
        for element in elements:
            href = element.get_attribute('href')
            if href is not None and website in href:
                new_href_results = pd.DataFrame({
                    'Preschool_Name': [preschool_name],
                    'href': [href],
                    'Page_Source': [re.sub(r'\W+', '_', href.replace('/', '_'))[:100]]
                })
                df_href_current = pd.read_csv(output)
                df_href_results = pd.concat(objs=[df_href_current, new_href_results],
                                            ignore_index=True)
                df_href_results.drop_duplicates(keep='last', inplace=True)
                save_to_csv(dataframe=df_href_results, output_file_=output)
                save_to_csv(dataframe=df_href_results, output_file_=output.replace('.csv', '.txt'))
    except Exception as e:
        print(f"href_failed: {e}")


def get_page_source_files(path):
    abs_path = os.path.abspath(path)
    page_source_files = os.listdir(abs_path)
    return page_source_files
