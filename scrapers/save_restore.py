
import csv
import json
import os


def export_to_json(my_dict, short_id):

    subdir = "json"
    if not os.path.exists(subdir):
        os.mkdir(subdir)

    json_path = subdir + "/" + short_id + ".json"

    print("Export for: "  + short_id)

    with open(json_path, "w") as outfile:
        # Write the dictionary to the file in JSON format
        json.dump(my_dict, outfile)

def import_from_json(short_id):
    json_path = "json/" + short_id + ".json"
    if not os.path.exists(json_path):
        return None

    print("Import for: "  + short_id + " from " + json_path)


    with open(json_path, "r") as infile:
        # Load the contents of the file as a dictionary
        my_dict = json.load(infile)
    return my_dict
    
def write_games_table_to_csv(game_results, game_name):
    subdir = "rspba_data"
    if not os.path.exists(subdir):
        os.mkdir(subdir)
    # output as CSV file
    # TODO - JSON instead and spit out the whole dictionary
    with open(subdir + "/" + game_name + ".csv", 'w', newline='') as file:
        writer = csv.writer(file)
        
        if game_results is None:
            print("Nothing to write!")
            return
        for grade_id, grade_results in game_results.items():
            writer.writerow([grade_id])
            for row in grade_results['table']:
                writer.writerow(row)
