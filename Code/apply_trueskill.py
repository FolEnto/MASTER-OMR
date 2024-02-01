from trueskill import *

def play_match(ID, result, teams, Team1, Team2):
    r1 = teams[Team1[ID]]
    r2 = teams[Team2[ID]]
    #print(Team1[ID] + " vs " + Team2[ID])
    if result == "Error 1":
        new_r1, new_r2 = rate_1vs1(r1, r2)
        #print(Team1[ID] + " wins")
    elif result == "Error 2":
        new_r2, new_r1 = rate_1vs1(r2, r1)
        #print(Team2[ID] + " wins")
    else :
        new_r1, new_r2 = rate_1vs1(r1, r2, drawn=True)
        #print("draw")

    teams[Team1[ID]] = new_r1
    teams[Team2[ID]] = new_r2

def evaluate_teams_weights():
    #normalize the weignts betwwen 0 and 2
    teams = evaluate_teams()
    min = 100
    max = 0
    for id in teams.keys():
        if teams[id].mu < min:
            min = teams[id].mu
        if teams[id].mu > max:
            max = teams[id].mu
    for id in teams.keys():
        value = teams[id].mu
        teams[id] = 1.9 * (value - min) / (max-min) + 0.1

    return teams


def evaluate_teams():
    inserteddot = Rating()
    deletedmeasure = Rating()
    headedit = Rating()
    insarticulation = Rating()
    accidentdel = Rating()
    deletedtuplet = Rating()
    editarticulation = Rating()
    extracontentedit = Rating()
    accidentins = Rating()
    pitchnameedit = Rating()
    crescendooffset = Rating()

    teams = {'inserteddot': inserteddot,
             'deletedmeasure': deletedmeasure,
             'headedit': headedit,
             'insarticulation': insarticulation,
             'accidentdel': accidentdel,
             'deletedtuplet': deletedtuplet,
             'editarticulation': editarticulation,
             'extracontentedit': extracontentedit,
             'accidentins': accidentins,
             'pitchnameedit': pitchnameedit,
             'crescendooffset': crescendooffset
             }

    Team1 = []
    Team2 = []
    with open("versus", "r") as f :
        lines = f.readlines()
        for line in lines:
            team1, team2 = line.replace("\n", "").split(" vs ")
            #print(team1, team2)
            Team1.append(team1)
            Team2.append(team2)

    import csv
    with open('match_results.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for idx, x in enumerate(reader) :
            if idx != 0 :
                for matchID, result in enumerate(x[1:]) :
                    play_match(matchID, result, teams, Team1, Team2)

    return teams