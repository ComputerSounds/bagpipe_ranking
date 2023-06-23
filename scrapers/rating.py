
# Step 1: Import necessary modules and classes
from trueskill import Rating, quality, rate
import save_restore
import re
import operator


# Step 2: Initialize band ratings
band_ratings = {}

games_results_by_year = save_restore.import_from_json('test_dump')

# Step 3: Iterate over the years in games_results_by_year
for year in sorted(games_results_by_year.keys()):
    year_results = games_results_by_year[year]

    # Step 4: Sort contests within the year based on dates
    sorted_contests = sorted(year_results.values(), key=lambda x: x['date'])

    # Step 5: Iterate over contests in chronological order
    for contest in sorted_contests:
        contest_results = contest['results']

        # Step 6: Iterate over divisions in contest results
        for division in contest_results.keys():
            placings = contest_results[division]['placings']

            # Step 7: Prepare ratings and placings for TrueSkill rate function
            ratings = []
            ranks = []
            for band_name, placing in placings.items():
                if band_name not in band_ratings:
                    band_ratings[band_name] = Rating()  # Initialize a new rating for the band if not already present
                ratings.append( (band_ratings[band_name],) )

                # Strip off code like "EP" and "PP"
                numeric_placing = re.search(r'\d+', placing).group()
                ranks.append(int(numeric_placing))

            # Step 8: Update ratings using TrueSkill rate function with "Free-for-all" rule
            rated_ratings = rate(ratings, ranks)

            # Update band_ratings with the updated ratings
            for i, band_name in enumerate(placings.keys()):
                band_ratings[band_name] = rated_ratings[i]

        # Print leaderboard of top N bands after each contest
        N = 5  # Define the number of top bands to display

        # Sort band_ratings based on the updated ratings in descending order
        sorted_ratings = sorted(band_ratings.items(), key=operator.itemgetter(1), reverse=True)

        # Display the leaderboard of top N bands
        print(f"Leaderboard after contest: {contest['date']}")
        for band_name, rating in sorted_ratings[:N]:
            print(f"{band_name}: {rating.expose()}")
        print()
# Final band_ratings contain the updated TrueSkill ratings for each band