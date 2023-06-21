from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep

import csv

# Define a function to process the links
def process_all_games_links(games_dict):

    all_games_data = []
    for game_text, game_link in games_dict.items():
        print(f"Process {game_text}: {game_link}")
        this_game_data = process_game(game_link)
        write_games_to_file(this_game_data, game_text)

def write_games_to_file(this_game_data, game_name):
    # output as CSV file
    with open(f'{game_name}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for value in this_game_data:
            writer.writerow(value)

def process_game(game_link):
    # Open the link
    driver = webdriver.Chrome()
    driver.get(game_link)

    # Find dropdown options and iterate over them
    select_grade = driver.find_element(By.ID, 'select_grade')
    options = select_grade.find_elements(By.TAG_NAME, 'option')
    
    table_data = []
    
    for grade_option in options:

        if grade_option.text.strip() == "Select Grade":
            continue
        # Select option
        grade_option.click()

        # Find table and extract data
        gr_val = grade_option.get_attribute("value")
        table_div_id = "div_" + gr_val
        table_wrapper_id = gr_val + "wrapper"
        table_id = gr_val
        table_class = "dataTable"
        table_xpath = "//*[@id=\"" + gr_val + "\"]"

        table_div = driver.find_element(By.ID, table_div_id)
        # table_wrapper = driver.find_element(By.ID, table_wrapper_id)
        results_table_by_grade = table_div.find_element(By.CLASS_NAME, table_class)
        # results_table_by_grade = driver.find_element(By.XPATH, table_id)

        table_rows = results_table_by_grade.find_elements(By.TAG_NAME, 'tr')

        table_data.append([f"Results for {grade_option.text}:"])
        for row in table_rows:
            row_data = []
            cells = row.find_elements(By.TAG_NAME, 'td')
            if cells:
                for cell in cells:
                    row_data.append(cell.text)
                table_data.append(row_data) if row_data else None
            else:
                header_cells = row.find_elements(By.TAG_NAME, 'th')
                row_data = [header_cell.text for header_cell in header_cells]
                table_data.append(row_data) if row_data else None
    
    driver.quit()
    return table_data
if __name__ == "__main__":
    
    game_data = process_game("https://rspba.org/results/bands/contests/2022-pitlochry")
    game_name = "test"
    write_games_to_file(game_data, game_name)