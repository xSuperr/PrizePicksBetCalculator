import requests
import json
from tabulate import tabulate

# Sort key for sorting diffrences from highest to lowest
def sort_key(data):
    return data[3]

# PrizePicks api request for current projections
params = (
)

headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"

}
session = requests.Session()
response = session.get('https://api.prizepicks.com/projections', data=params, headers=headers)

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
        scores.append([data['relationships']['new_player']['data']['id'], data['attributes']['line_score'], data['attributes']['stat_type']])
        

# Match names with projected score, score type and league using ids
results = list()
for data in names:
    i = data[0]
    for nData in scores:
        nI = nData[0]
        if i == nI:
            results.append([data[1], nData[1], nData[2], data[2]])
            
# Load predicted NBA data            
f = open('nba.json')
nba = json.load(f)

predictedNBA = list()

for data in nba:
    predictedNBA.append([data['PLAYER'], data['FP'], data['PTS'], data['AST'], data['TRB'], data['BK'], data['ST'], data['TO'], data['FT']])
    
# Load predicted NHL data            
#f = open('nhl.json')
#nhl = json.load(f)

#predictedNHL = list()

#for data in nhl:
    #predictedNHL.append([data['PLAYER'], data['SOG'], data['WINS'], data['GOALS'], data['SAVES']])
    
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
    predictedCFB.append([data['PLAYER'], data['FP'], data['PASSYD'], data['RUSHYD'], data['RUSHTD'], data['RECYD'], data['RECTD']])
    
# Create a list of players with their projected score, predicted score, the difference, the league, the score type and if its under or over
diffrences = list()
for data in results:
    name = data[0]
    projected = data[1]
    score_type = data[2]
    league = data[3]
    
    # TODO: NHL
    if league == 'NBA':
        for nData in predictedNBA:
            if nData[0] == name:
                predicted = None
                if score_type == 'Points':
                    predicted = nData[2]
                if score_type == 'Rebs+Asts':
                    predicted = nData[3] + nData[4]
                if score_type == 'Fantasy Score':
                    predicted = nData[1]
                if score_type == 'Pts+Rebs+Asts':
                    predicted = nData[2] + nData[3] + nData[4]
                if score_type == 'Pts+Asts':
                    predicted = nData[2] + nData[4]
                if score_type == 'Pts+Rebs':
                    predicted = nData[2] + nData[3]
                if score_type == 'Rebounds':
                    predicted = nData[3]
                if score_type == 'Assists':
                    predicted = nData[4]
                if score_type == 'Blks+Stls':
                    predicted = nData[5] + nData[6]
                if score_type == 'Turnovers':
                    predicted = nData[7]
                    
                if predicted == None:
                    print("Score type for Type: "+score_type+" in NBA could not be found!")
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
                    predicted = nData[1]
                if score_type == 'Pass Yards':
                    predicted = nData[2]
                if score_type == 'Rush Yards':
                    predicted = nData[3]
                if score_type == 'Receiving Yards':
                    predicted = nData[4]
                if score_type == 'Rush+Rec Yds':
                    predicted = nData[3] + nData[4]
                if score_type == 'Pass+Rush Yds':
                    predicted = nData[2] + nData[3]
                
                if predicted == None:
                    print("Score type for Type: "+score_type+" in NFL could not be found!")
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
                    predicted = nData[1]
                if score_type == 'Rush Yards':
                    predicted = nData[3]
                if score_type == 'Receiving Yards':
                    predicted = nData[5]
                if score_type == 'Rush+Rec Yds':
                    predicted = nData[3] + nData[5]
                if score_type == 'Pass+Rush Yds':
                    predicted = nData[2] + nData[3]
                if score_type == 'Rush TDs':
                    predicted = nData[4]
                if score_type == 'Rec TDs':
                    predicted = nData[6]
                if score_type == 'Pass Yards':
                    predicted = nData[2]
                    
                if predicted == None:
                    print("Score type for Type: "+score_type+" in CFB could not be found!")
                else:
                    if projected >= predicted:
                        diffrence = projected - predicted
                        diffrences.append([name, projected, predicted, diffrence, league, score_type, 'Under'])
                    else:
                        diffrence = predicted - projected
                        diffrences.append([name, projected, predicted, diffrence, league, score_type, 'Over'])
    
    else:
        print("League: "+league+" not found!")

# Sort diffrences from highest to lowest
diffrences.sort(key=sort_key, reverse=True)

# Create table
first40 = diffrences[0:50]
first40.insert(0, ["Name", "Proj", "Pred", "Diff", "LG", "Type", "O/U"])
print(tabulate(first40, headers='firstrow', tablefmt='fancy_grid'))
