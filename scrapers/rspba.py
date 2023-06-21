from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import games

def get_years(driver):

    # Find the drop down selector
    year_dropdown = driver.find_element(By.CLASS_NAME, "results_picker")

    # Find all options in the dropdown
    year_options = year_dropdown.find_elements(By.TAG_NAME, "option")
    print("Years:")
    # Extract text from each option and print it
    for year_option in year_options:
        option_text = year_option.text.strip()
        if option_text:  # skip empty options
            print(option_text)
    return year_options

def get_contests(driver):
    # Find the table element
    table = driver.find_element(By.ID, "contests")

    # Find all rows in the table
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Extract text and links from second column of each row and store them in a dictionary
    games_dict = {}
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) > 1:
            second_col = cols[1]
            second_col_text = second_col.text.strip()
            # Get the link from the anchor tag in the second column, if it exists
            try:
                second_col_link = second_col.find_element(By.TAG_NAME, "a").get_attribute("href")
            except:
                second_col_link = None

            if second_col_text:  # skip empty cells
                games_dict[second_col_text] = second_col_link

    return games_dict

if __name__ == "__main__":
    # Initialize Chrome driver
    driver = webdriver.Chrome()

    # Navigate to webpage
    url = "https://rspba.org/results/bands/contests/2022/"
    driver.get(url)

    year_options = get_years(driver)


    games_dict = get_contests(driver)
    # Pretty print
    for key, value in games_dict.items():
        print(f"{key}: {value}")
    # Call the process_links() function to process the links
    games.process_all_games_links(games_dict)

    # Close the browser window
    driver.quit()