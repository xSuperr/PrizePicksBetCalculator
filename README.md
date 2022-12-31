# Prize Picks Bet Calculator
This python script takes the current bets from the Prize Picks API and compares it to predicted data
from https://sportsline.com to make a list of the top 25 most likely to hit bets.

## Supported Leagues
- [X] NBA (Points, Rebounds, Assists, Fantasy Score, Blocks, Steals, Turnovers)
- [X] NFL (Pass Yards, Rush Yards, Receiving Yards, Fantasy Score)
- [X] CFB (Pass Yards, Rush Yards, Receiving Yards, Fantasy Score, Rush TDs, Rec TDs)
- [ ] NHL

## How to use
 * Go to https://www.sportsline.com/nba/expert-projections/simulation
 * Export the data for NBA, NFL, and CFB (If a prediction doesn't exist, check back later!)
 * You will download CSV files for those leagues
 * Go to https://csvjson.com/csv2json
 * Upload the CSV files and convert them to JSON
 * Rename the downloaded JSON files into their league (lowercase)
 
 ### Example:
    CFB_Projections_12_30_2022 -> csvjson(?) -> cfb.json
    NBA_Projections_12_30_2022 -> csvjson(?) -> nba.json
    NFL_Projections_12_30_2022.json -> csvjson(?) -> nfl.json

  * Put the json files in the same folder as prizepicks.py
  * Run the python script (either as an exe or with python)
  * The top 25 bets will be logged at the bottom, with the players name, league, diffrence between
   projected and predicted points, the score type, and if its under/over the projection

## Warnings:
  * When running the script there will be a lot of warning messages, these are just Prize Picks
   leagues not existing on the prediction software, and score types not existing. Just ignore these!
  * Try not to run multiple times a day. The Prize Picks API will most likely rate limit you
  * These Bets are not 100% accurate. Simmulations make mistakes, these are just intelligent guesses
   as to what bets will hit.
