from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select

import games
import save_restore
import datetime

driver = webdriver.Chrome()

def get_available_years(driver):

    # Initialize Chrome driver


    # Navigate to webpage
    url = "https://rspba.org/results/bands/contests/"
    driver.get(url)

    year_texts = get_years_from_dropdown(driver)
    # start from the beginning...
    year_texts = sorted(year_texts, key=lambda year_texts: int(year_texts))

    return year_texts

def get_years_from_dropdown(driver):

    # Find the drop down selector
    year_dropdown = driver.find_element(By.CLASS_NAME, "results_picker")

    # Find all options in the dropdown
    year_texts = [year_option.text for year_option in Select(year_dropdown).options]

    return year_texts

def get_contests(driver, year):
    # Find the table element
    table = driver.find_element(By.ID, "contests")

    # Find all rows in the table
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Extract text and links from second column of each row and store them in a dictionary
    games_dict = {}
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) < 2:
            continue
        game_col = cols[1]
        date_col = cols[2]
        game_col_text = game_col.text.strip()
        date_col_text = date_col.text.strip()
        date_text_formatted = date_col_text.replace('th', '').replace('nd', '').replace('st', '').replace('rd', '')
        game_datetime = datetime.datetime.strptime(date_text_formatted + " " + year, "%d %b %Y")
        game_sortable_date = game_datetime.strftime("%Y-%m-%d")

        # Get the link from the anchor tag in the second column, if it exists
        try:
            game_col_link = game_col.find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            game_col_link = None

        # The last bit of the URL seems like a good identifier.
        short_name = game_col_link.rsplit('/', 1)[-1]

        if game_col_text:  # skip empty cells
            # Save the date and the link!
            this_game_dict = {}
            this_game_dict['link'] = game_col_link
            this_game_dict['date'] = game_sortable_date
            this_game_dict['name'] = game_col_text
            this_game_dict['id']   = short_name

            games_dict[short_name] = this_game_dict
        else:
            assert()

    return games_dict



if __name__ == "__main__":


    year_texts = get_available_years(driver)


    games_dict_by_year = {}
    games_results_by_year = {}

    for year_text in year_texts:
        
        load_results = save_restore.import_from_json(year_text)
        if load_results is not None:
            print("Got games for year: " + year_text + " from file!")
            this_years_contests = load_results
        else:
            # Navigate to webpage
            url = "https://rspba.org/results/bands/contests/" + year_text + "/"
            driver.get(url)

            print("Get games for year: " + year_text)

            this_years_contests = get_contests(driver, year_text)

            save_restore.export_to_json(this_years_contests, year_text)
            

        games_dict_by_year[year_text] = this_years_contests
        # Pretty print
        for key, value in this_years_contests.items():
            print(f"{key}: {value}")
            
        print("----------------------------------------")
        # Call the process_links() function to process the links
        games_results_for_year = games.process_all_games_links(this_years_contests)

        games_results_by_year[year_text] = games_results_for_year
        # REMOVE ME
        break;

    # Close the browser window
    driver.quit()