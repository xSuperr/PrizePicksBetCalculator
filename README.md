# Prize Picks Bet Calculator
This python script takes the current bets from the Prize Picks API and compares it to predicted data
from https://sportsline.com to make a list of the top 50 most likely to hit bets.

## Supported Leagues
- [X] NBA (Points, Rebounds, Assists, Fantasy Score, Blocks, Steals, Turnovers)
- [X] NFL (Pass Yards, Rush Yards, Receiving Yards, Fantasy Score)
- [X] CFB (Pass Yards, Rush Yards, Fantasy Score, Rush TDs, Rec TDs)
- [X] NHL (Shots On Goal, Points, Goals, Assists, Goalie Saves, Blocked Shots)

## How to use
 * Install the below packages
 * Run the script

## Packages:
 - [X] requests (To send a https request to the Prize Picks API)
 - [X] json (Built-In, For handling the API response and prediction file loading)
 - [X] tabulate (To build a table of the results for appearance) (TODO: Replace with pandas tables)
 - [X] fake_headers (To generate fake headers to stop 403 responses)
 - [X] pandas (To extract the tables from the prediction websites)
 - [X] lxml (Pandas dependency)

## Warnings:
  * When running the script there will be a lot of warning messages, these are just Prize Picks
   leagues not existing on the prediction software, and score types not existing. Just ignore these!
  * Try not to run multiple times a day. The Prize Picks API will most likely rate limit you (Unless you use a proxy)
  * These Bets are not 100% accurate. Simmulations make mistakes, these are just intelligent guesses
   as to what bets will hit.
  * You may run into a 403 error, this normally due to your IP being flagged, or bad headers
