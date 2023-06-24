# Step 1: Import necessary modules and classes
from openskill import Rating, rate, ordinal
import re
import operator
import save_restore

# Step 2: Initialize band ratings
current_band_ratings = {}

games_results_by_year = save_restore.import_from_json('test_dump')

# Step 3: Iterate over the years in games_results_by_year
for year in sorted(games_results_by_year.keys()):
    year_results = games_results_by_year[year]

    # Step 4: Sort contests within the year based on dates
    sorted_contests = sorted(year_results.values(), key=lambda x: x['date'])

    # Step 5: Iterate over contests in chronological order
    for contest in sorted_contests:

        if not "results" in contest:
            print("NO RESULTS FOR " + contest['name'])
            continue

        contest_results = contest['results']

        # Step 6: Iterate over divisions in contest results
        for division in contest_results.keys():
            actual_placings = contest_results[division]['placings']

            # Step 7: Prepare ratings and placings for OpenSkill rate function
            ratings_of_competing_bands = []
            ranks = []
            for band_name, placing in actual_placings.items():

                if placing == "DISQ":
                    # Playing for sheets! Let's not draw conclusions....
                    continue

                # Strip off text like "EP" and "PP"
                numeric_placing = re.search(r'\d+', placing).group()
                ranks.append(int(numeric_placing))


                # Initialize a new rating for the band if not already present
                if band_name not in current_band_ratings:
                    current_band_ratings[band_name] = Rating()
                ratings_of_competing_bands.append( [current_band_ratings[band_name]] )



            # Step 8: Update ratings using OpenSkill rate function with "Free-for-all" rule
            updated_band_ratings = rate(ratings_of_competing_bands, rank = ranks)

            # Update current_band_ratings with the updated ratings
            for i, band_name in enumerate(actual_placings.keys()):
                # TODO - this doesn't match with the bands used in ranking.
                # FIXME
                current_band_ratings[band_name] = updated_band_ratings[i][0]

        # Print leaderboard of top N bands after each contest
        N = 5  # Define the number of top bands to display

        # Sort current_band_ratings based on the updated ratings in descending order
        sorted_ratings = sorted(current_band_ratings.items(), key=lambda x: ordinal(x[1]), reverse=True)

        # Display the leaderboard of top N bands
        print(f"Leaderboard after contest: {contest['name']} on {contest['date']}")
        for band_name, rating in sorted_ratings[:N]:
            print(f"{band_name: <50}: {ordinal(rating):.3f}")

        print()
# Final current_band_ratings contain the updated OpenSkill ratings for each band
