from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from time import sleep

import save_restore

from rspba import driver

# driver = webdriver.Chrome()


# Define a function to process the links
def process_all_games_links(games_dict):

    all_games_data = []
    for game_id, game in games_dict.items():

        game_link   = game['link']

        print(f"Process {game_id}: {game_link}")

        load_results = save_restore.import_from_json(game_id)

        if load_results is not None:
            print("Get "+game_id+" from file!")

            game_results = load_results['results']
            games_dict[game_id]['results'] = game_results

        else:

            game_results = process_game(game_link)

            if game_results is None:
                # TODO not sure what else to try here....
                continue;

            games_dict[game_id]['results'] = game_results

            save_restore.write_games_table_to_csv(game_results, game_id)

            save_restore.export_to_json(games_dict[game_id], game_id)

    return games_dict



def process_game(game_link):
    # Open the link
    driver.get(game_link)

    # Find dropdown options and iterate over them
    try:
        select_grade = driver.find_element(By.ID, 'select_grade')
    except NoSuchElementException as e:
        print(f'Error: {e.msg}')
        return None

    options = select_grade.find_elements(By.TAG_NAME, 'option')

    results = {}

    for grade_option in options:

        if grade_option.text.strip() == "Select Grade":
            continue
        # Select option
        grade_option.click()
        grade_text = grade_option.text.strip()

        print([f"Get results for {grade_text}:"])

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


        table_data, placing_by_band = get_table_data(results_table_by_grade)

        res_dict = {}
        res_dict['table'] = table_data
        res_dict['placings'] = placing_by_band

        results[grade_text] = res_dict


    return results

def get_table_data(table):

    table_rows = table.find_elements(By.TAG_NAME, 'tr')

    table_data = []
    placing_by_band = {}
    for row in table_rows:
        row_data = []
        data_cells = row.find_elements(By.TAG_NAME, 'td')
        header_cells = row.find_elements(By.TAG_NAME, 'th')
        if data_cells:

            band_name = data_cells[1].text
            placing = data_cells[-1].text
            placing_by_band[band_name] = placing

            for cell in data_cells:
                if len(cell.text):
                    row_data.append(cell.text)

        elif header_cells:

            for cell in header_cells:
                if len(cell.text):
                    row_data.append(cell.text)
        else:
            assert()
        table_data.append(row_data) if row_data else None

    return table_data, placing_by_band

if __name__ == "__main__":
    # TODO this should be a in a test.

    game_data = process_game("https://rspba.org/results/bands/contests/2022-pitlochry")
    game_name = "test"
    save_restore.write_games_table_to_csv(game_data, game_name)

    game_dict = {}
    game_dict['id'] = game_name
    game_dict['results'] = game_data
    save_restore.export_to_json(game_dict, game_name)

    load_results = save_restore.import_from_json(game_name)