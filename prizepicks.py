import requests
import json
import os
import math
import pandas as pd
from tabulate import tabulate
from fake_headers import Headers


# Sort key for sorting diffrences from highest to lowest
def sort_key(t):
    return t[3]


# PrizePicks api request for current projections
headers = Headers(
    # Generate fake headers
    headers=False
).generate()

session = requests.Session()
response = session.get('https://api.prizepicks.com/projections', headers=headers)

if response.status_code != 200:
    print("Failed to make the HTTPs Request, Code: " + str(response.status_code) + ", Maybe try running again?")
else:
    j = response.json()

    # Match names with player ids and league
    nameMap = j['included']
    names = list()
    for data in nameMap:
        if data['type'] == 'new_player':
            names.append([data['id'], data['attributes']['name'], data['attributes']['league']])

    # Match projected score and score type with player id
    scoreMap = j['data']
    scores = list()

    for data in scoreMap:
        if data['type'] == 'projection':
            scores.append([data['relationships']['new_player']['data']['id'], data['attributes']['line_score'],
                           data['attributes']['stat_type']])

    # Match names with projected score, score type and league using ids
    results = list()
    for data in names:
        i = data[0]
        for nData in scores:
            nI = nData[0]
            if i == nI:
                results.append([data[1], nData[1], nData[2], data[2]])

    # Delete old prediction json files and extract the tables from the websites html
    os.remove('nba.json')
    os.remove('nfl.json')
    os.remove('cfb.json')
    os.remove('nhl.json')

    nbaTable = requests.get('https://www.sportsline.com/nba/expert-projections/simulation/', headers=headers).content
    df_list = pd.read_html(nbaTable)
    df = df_list[0]
    df.to_json("nba.json", orient="records", date_format="epoch", double_precision=10,
               force_ascii=True, date_unit="ms", default_handler=None)

    nflTable = requests.get('https://www.sportsline.com/nfl/expert-projections/simulation/', headers=headers).content
    df_list = pd.read_html(nflTable)
    df = df_list[0]
    df.to_json("nfl.json", orient="records", date_format="epoch", double_precision=10,
               force_ascii=True, date_unit="ms", default_handler=None)

    cfbTable = requests.get('https://www.sportsline.com/college-football/expert-projections/simulation/',
                            headers=headers).content
    df_list = pd.read_html(cfbTable)
    df = df_list[0]
    df.to_json("cfb.json", orient="records", date_format="epoch", double_precision=10,
               force_ascii=True, date_unit="ms", default_handler=None)

    nhlTable = requests.get('https://www.sportsline.com/nhl/expert-projections/simulation/', headers=headers).content
    df_list = pd.read_html(nhlTable)
    df = df_list[0]
    df.to_json("nhl.json", orient="records", date_format="epoch", double_precision=10,
               force_ascii=True, date_unit="ms", default_handler=None)

    # Load predicted NBA data
    f = open('nba.json')
    nba = json.load(f)

    predictedNBA = list()

    for data in nba:
        predictedNBA.append(
            [data['PLAYER'], data['FP'], data['PTS'], data['AST'], data['TRB'], data['BK'], data['ST'], data['TO'],
             data['FT']])

    # Load predicted NHL data
    f = open('nhl.json')
    nhl = json.load(f)

    predictedNHL = list()

    for data in nhl:
        predictedNHL.append(
            [data['PLAYER'], data['SOG'], data['WINS'], data['GOALS'], data['SAVES'], data['ASSISTS'],
             data['BLOCKED SHOTS']])

    # Load predicted NFL data
    f = open('nfl.json')
    nfl = json.load(f)

    predictedNFL = list()

    for data in nfl:
        # TODO: Rest of the data
        predictedNFL.append([data['PLAYER'], data['FP'], data['PASSYD'], data['RUSHYD'], data['RECYD']])

    f = open('cfb.json')
    cfb = json.load(f)

    predictedCFB = list()

    for data in cfb:
        # TODO: Rest of the data
        predictedCFB.append(
            [data['PLAYER'], data['FP'], data['PASSYD'], data['RUSHYD'], data['RUSHTD'], data['RECYD'],
             data['RECTD']])

    # Create a list of players with their projected score, predicted score, the difference, the league, the score
    # type and if its under or over
    diffrences = list()
    for data in results:
        name = data[0]
        projected = data[1]
        score_type = data[2]
        league = data[3]

        if league == 'NBA':
            for nData in predictedNBA:
                if nData[0] == name:
                    predicted = None
                    if score_type == 'Points':
                        predicted = float(nData[2])
                    if score_type == 'Rebs+Asts':
                        p = float(nData[3])
                        r = float(nData[4])
                        if not math.isnan(p) and not math.isnan(r):
                            predicted = p + r
                    if score_type == 'Fantasy Score':
                        predicted = float(nData[1])
                    if score_type == 'Pts+Rebs+Asts':
                        p = float(nData[2])
                        r = float(nData[3])
                        a = float(nData[4])
                        if not math.isnan(p) and not math.isnan(r) and not math.isnan(a):
                            predicted = p + r + a
                    if score_type == 'Pts+Asts':
                        p = float(nData[2])
                        r = float(nData[3])
                        if not math.isnan(p) and not math.isnan(r):
                            predicted = p + r
                    if score_type == 'Pts+Rebs':
                        p = float(nData[2])
                        r = float(nData[3])
                        if not math.isnan(p) and not math.isnan(r):
                            predicted = p + r
                    if score_type == 'Rebounds':
                        predicted = float(nData[3])
                    if score_type == 'Assists':
                        predicted = float(nData[4])
                    if score_type == 'Blks+Stls':
                        p = float(nData[5])
                        r = float(nData[6])
                        if not math.isnan(p) and not math.isnan(r):
                            predicted = p + r
                    if score_type == 'Turnovers':
                        predicted = float(nData[7])
                    if score_type == 'Free Throws Made':
                        predicted = float(nData[8])
                    if score_type == 'Steals':
                        predicted = float(nData[6])
                    if score_type == 'Blocked Shots':
                        predicted = float(nData[5])

                    if predicted is None:
                        print("Score type for Type: " + score_type + " in NBA could not be found!")
                    elif predicted == "":
                        print(
                            "Predicted data for Type: " + score_type + " Player:" + name + " in NBA could not be found!")
                    else:
                        if projected >= predicted:
                            diffrence = projected - predicted
                            diffrences.append([name, projected, predicted, diffrence, league, score_type, 'Under'])
                        else:
                            diffrence = predicted - projected
                            diffrences.append([name, projected, predicted, diffrence, league, score_type, 'Over'])

        elif league == 'NFL':
            for nData in predictedNFL:
                if nData[0] == name:
                    predicted = None
                    if score_type == 'Fantasy Score':
                        predicted = float(nData[1])
                    if score_type == 'Pass Yards':
                        predicted = float(nData[2])
                    if score_type == 'Rush Yards':
                        predicted = float(nData[3])
                    if score_type == 'Receiving Yards':
                        predicted = float(nData[4])
                    if score_type == 'Rush+Rec Yds':
                        p = float(nData[3])
                        r = float(nData[4])
                        if not math.isnan(p) and not math.isnan(r):
                            predicted = p + r
                    if score_type == 'Pass+Rush Yds':
                        p = float(nData[2])
                        r = float(nData[3])
                        if not math.isnan(p) and not math.isnan(r):
                            predicted = p + r

                    if predicted is None:
                        print("Score type for Type: " + score_type + " in NFL could not be found!")
                    elif math.isnan(predicted):
                        print(
                            "Predicted data for Type: " + score_type + " Player:" + name + " in NFL could not be found!")
                    else:
                        if projected >= predicted:
                            diffrence = projected - predicted
                            diffrences.append([name, projected, predicted, diffrence, league, score_type, 'Under'])
                        else:
                            diffrence = predicted - projected
                            diffrences.append([name, projected, predicted, diffrence, league, score_type, 'Over'])

        elif league == 'CFB':
            for nData in predictedCFB:
                if nData[0] == name:
                    predicted = None
                    if score_type == 'Fantasy Score':
                        predicted = float(nData[1])
                    if score_type == 'Rush Yards':
                        predicted = float(nData[3])
                    # if score_type == 'Receiving Yards':
                    # predicted = float(nData[5])
                    # if score_type == 'Rush+Rec Yds':
                    # predicted = float(nData[3]) + float(nData[5])
                    if score_type == 'Pass+Rush Yds':
                        p = float(nData[2])
                        r = float(nData[3])
                        if not math.isnan(p) and not math.isnan(r):
                            predicted = p+r
                    if score_type == 'Rush TDs':
                        predicted = float(nData[4])
                    if score_type == 'Rec TDs':
                        predicted = float(nData[6])
                    if score_type == 'Pass Yards':
                        predicted = float(nData[2])

                    if predicted is None:
                        print("Score type for Type: " + score_type + " in CFB could not be found!")
                    elif math.isnan(predicted):
                        print(
                            "Predicted data for Type: " + score_type + " Player:" + name + " in CFB could not be found!")
                    else:
                        if projected >= predicted:
                            diffrence = projected - predicted
                            diffrences.append([name, projected, predicted, diffrence, league, score_type, 'Under'])
                        else:
                            diffrence = predicted - projected
                            diffrences.append([name, projected, predicted, diffrence, league, score_type, 'Over'])

        elif league == 'NHL':
            for nData in predictedNHL:
                if nData[0] == name:
                    predicted = None
                    if score_type == 'Shots On Goal':
                        predicted = float(nData[1])
                    if score_type == 'Points':
                        predicted = float(nData[2])
                    if score_type == 'Goals':
                        predicted = float(nData[3])
                    if score_type == 'Assists':
                        predicted = float(nData[5])
                    if score_type == 'Goalie Saves':
                        predicted = float(nData[4])
                    if score_type == 'Blocked Shots':
                        predicted = float(nData[6])

                    if predicted is None:
                        print("Score type for Type: " + score_type + " in NHL could not be found!")
                    elif math.isnan(predicted):
                        print(
                            "Predicted data for Type: " + score_type + " Player:" + name + " in NHL could not be found!")
                    else:
                        if projected >= predicted:
                            diffrence = projected - predicted
                            diffrences.append([name, projected, predicted, diffrence, league, score_type, 'Under'])
                        else:
                            diffrence = predicted - projected
                            diffrences.append([name, projected, predicted, diffrence, league, score_type, 'Over'])

        else:
            print("League: " + league + " not found!")

    # Sort diffrences from highest to lowest
    diffrences.sort(key=sort_key, reverse=True)

    # Create table
    d = diffrences[0:50]

    d.insert(0, ["Player Name", "Proj", "Pred", "Diff", "Game", "Statistic Type", "O/U"])

    print(tabulate(d, headers='firstrow', tablefmt='fancy_grid'))
