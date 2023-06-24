# Step 1: Import necessary modules and classes
from openskill import Rating, rate, ordinal
import re
import operator
import save_restore


# ------------------------------------------------------
# TODO: move to new class
CURRENT_BAND_RATINGS = {}

def get_ratings(band_grade, band_name):
    global CURRENT_BAND_RATINGS

    if band_grade not in CURRENT_BAND_RATINGS:
        CURRENT_BAND_RATINGS[band_grade] = {}

    if band_name not in CURRENT_BAND_RATINGS[band_grade]:
        CURRENT_BAND_RATINGS[band_grade][band_name] = Rating()

    rating = CURRENT_BAND_RATINGS[band_grade][band_name]
    return rating


def update_ratings(band_grade, band_name, rating):
    global CURRENT_BAND_RATINGS
    CURRENT_BAND_RATINGS[band_grade][band_name] = rating;

def leaderboard():
    global CURRENT_BAND_RATINGS
    for grade_id in CURRENT_BAND_RATINGS.keys():
        print("" + grade_id)
        # print("------------")
        leader_board_for_grade(grade_id)
        print()

def leader_board_for_grade(band_grade):
    global CURRENT_BAND_RATINGS
    # Print leaderboard of top N bands after each contest
    N = 5  # Define the number of top bands to display

    # Sort current_band_ratings based on the updated ratings in descending order
    sorted_ratings = sorted(CURRENT_BAND_RATINGS[band_grade].items(), key=lambda x: ordinal(x[1]), reverse=True)

    # Display the leaderboard of top N bands
    for band_name, rating in sorted_ratings[:N]:
        print(f"   {band_name: <40}: {ordinal(rating):.3f}")

# ------------------------------------------------------

def process_games(results_to_process):

    # Sort contests within the year based on dates
    sorted_contests = sorted(results_to_process.values(), key=lambda x: x['date'])

    # Iterate over contests in chronological order
    for contest in sorted_contests:

        if not "results" in contest:
            print("NO RESULTS FOR " + contest['name'])
            continue

        contest_results = contest['results']

        # Iterate over grades in contest results
        for grade_id in contest_results.keys():
            actual_placings = contest_results[grade_id]['placings']

            ratings_of_competing_bands, ranks, names_of_competing_bands = create_input_for_openskill(grade_id, actual_placings)

            # Compute updated ratings
            updated_band_ratings = rate(ratings_of_competing_bands, rank = ranks)

            # Save updated ratings
            for i, band_name in enumerate(names_of_competing_bands):
                update_ratings(grade_id, band_name, updated_band_ratings[i][0])

        # Leaderboard
        print(f"Leaderboard after {contest['name']} on {contest['date']}")
        print("-----------------------------------------------")
        leaderboard()
        print()


def create_input_for_openskill(grade, placings_table):

    # Step 7: Prepare ratings and placings for OpenSkill rate function
    names_of_competing_bands = []
    ratings_of_competing_bands = []
    ranks = []
    for band_name, placing in placings_table.items():

        if placing == "DISQ":
            # Playing for sheets! Let's not draw conclusions....
            continue

        # Strip off text like "EP" and "PP"
        numeric_placing = re.search(r'\d+', placing).group()
        ranks.append(int(numeric_placing))

        current_rating = get_ratings(grade, band_name)


        ratings_of_competing_bands.append( [current_rating] )
        names_of_competing_bands.append(band_name)

    return ratings_of_competing_bands, ranks, names_of_competing_bands

if __name__ == "__main__":

    games_results_by_year = save_restore.import_from_json('test_dump')

    for year in sorted(games_results_by_year.keys()):
        year_results = games_results_by_year[year]

        process_games(year_results)
        #TODO FIXME REMOVE
        break;



