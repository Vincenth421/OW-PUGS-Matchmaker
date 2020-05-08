import numpy as np
import pickle
import random


# [tankSR, dpsSR, suppSR, ready]
# build 2 teams of 6 

#/* Build a function that takes playerData. minimize SR diff; return the following:
#Matchmaker output:
#Team A: (avg SR)
#P1  P4
#P2	P5
#P3	P6
#Team B: (avg SR)
#P4	P7
#P5	P8
#P6	P9  */##
# prefer 0 = no preference, 1 = mt, 2 = ot, 3 = dps, 4 = support


#print(playerData["Player1"]["ready"])
# "!support 1000"
#def commandParse(string):
#    if(string)


# mystr = "!support 1000"

# userData = mystr.split()
# print(userData)

def saveTest():
    a = playerData
    savePlayerData()
    loadPlayerData()

def savePlayerData():
    with open("data.pickle", "wb") as handle:
        pickle.dump(playerData, handle, protocol=pickle.HIGHEST_PROTOCOL)

def loadPlayerData():
    with open('data.pickle', 'rb') as handle:
        playerData = pickle.load(handle)
    return playerData

playerData = loadPlayerData()

#good work gang
def updatePlayerData(mystr, PlayerID):
    userData = mystr.split()
    if PlayerID not in playerData:
        playerData[PlayerID] = {}
    if(userData[0] == "!support"):
        playerData[PlayerID]["supportSR"] = userData[1]
    elif(userData[0] == "!damage" or userData[0] == "!dps"):
        playerData[PlayerID]["dpsSR"] = userData[1]
    elif(userData[0] == "!tank"):
        playerData[PlayerID]["tankSR"] = userData[1]
    elif(userData[0] == "!ready"):
    	playerData[PlayerID]["ready"] = not playerData[PlayerID]["ready"]
    print(playerData)
    savePlayerData()

def getPlayerData(PlayerID):
    # I'd like for this to return a nice and cleanly formatted string with
    # the player data
    return playerData[PlayerID]
        
# main matchmaking function
# chooses 12 players, splits into roles, matchmakes roles, and then combines them back together
def matchmake(playerData):
    roles = split(playerData)
    
    tank = roles[0]
    dps = roles[1]
    supp = roles[2]
    
    t = matchmake(tank)
    d = matchmake(dps)
    s = matchmake(supp)
    
    return combine(t, d, s)

# ready is a bool
# playerData is a hash table of any number fo people
# splits all players into their chosen roles, then selects 4 for each role
def split(playerData):
  tank = []
  dps = []
  supp = []
  
  for name in playerData.keys():
    role = playerData[name]['queue']
    if role == 'tank':
        tank.append([name, playerData[name]['tank']])
    elif role == 'dps':
        dps.append([name, playerData[name]['dps']])
    elif role == 'support':
        supp.append([name, playerData[name]['support']])
  
    return [select(tank), select(dps), select(supp)]

# selects 4 players from a pool of any number
# role comes in as a list, returns a list of the randomly selected players
def select(role):
    selected = []
    for i in range(4):
        num = random.randint(0, len(role)-1)
        #TODO check for dupe random numbers
        selected.append(role[num])
    return selected

# given a role hash table
# add to the value bucket a new entry, Team A or B
# 6 members on A, 6 on B
# as even SR spread as possible
# Assume that role is a list of length 4
def balance(role):
    bestPair = []
    average2 = 0
    bestDifference = 5000
    totalsr = 0
    for i in range(len(role)):
        totalsr += role[i][1]

    for i in range(len(role)):
        for j in range(i, len(role)):
            avg1 = (role[i][1] + role[j][1]) / 2
            avg2 = (totalsr - role[i][1] - role[j][1]) / 2
            difference = avg1 - avg2
            if abs(difference) < abs(bestDifference):
                average2 = avg2
                bestDifference = difference
                bestPair = [avg1, role[i][0], role[j][0]]
  
    otherPair = [average2]
    for i in range(len(role)):
        if ~(role[i][0] in bestPair):
            otherPair.append(role[i][0])
  
    both = [bestPair, otherPair]
    return both

# list.insert(0, thing-to-insert)
# to prepend things to a list ^^^

# combines the different roles into a team
# average sr is first element in both team A and team B
# good work team
def combine(tank, dps, supp):
    dReverse = False
    sReverse = False
    tankDiff = tank[0][0] - tank[1][0]
    dpsDiff = dps[0][0] - dps[1][0]
    suppDiff = supp[0][0] - supp[1][0]
    average1 = tank[0][0]
    average2 = tank[1][0]
    A = [tank[0][1], tank[0][2]]
    B = [tank[1][1], tank[1][2]]
  
    # brute force calculation of combined sr average
    bestDiff = tankDiff + dpsDiff + suppDiff
    if abs(tankDiff - dpsDiff + suppDiff) < abs(bestDiff):
        bestDiff = tankDiff - dpsDiff + suppDiff
        dReverse = True
    if abs(tankDiff + dpsDiff - suppDiff) < abs(bestDiff):
        bestDiff = tankDiff + dpsDiff - suppDiff
        sReverse = True
    if abs(tankDiff - dpsDiff - suppDiff) < abs(bestDiff):
        bestDiff = tankDiff - dpsDiff - suppDiff
        dReverse = True
        sReverse = True
    
    # add to team A or B depending on above calculations
    if dReverse:
        A.append(dps[1][1])
        A.append(dps[1][2])
        B.append(dps[0][1])
        B.append(dps[0][2])
        average1 += dps[1][0]
        average2 += dps[0][0]
    else:
        A.append(dps[0][1])
        A.append(dps[0][2])
        B.append(dps[1][1])
        B.append(dps[1][2])
        average1 += dps[0][0]
        average2 += dps[1][0]
    
    if sReverse:
        A.append(supp[1][1])
        A.append(supp[1][2])
        B.append(supp[0][1])
        B.append(supp[0][2])
        average1 += supp[1][0]
        average2 += supp[0][0]
    else:
        A.append(supp[0][1])
        A.append(supp[0][2])
        B.append(supp[1][1])
        B.append(supp[1][2])
        average1 += supp[0][0]
        average2 += supp[1][0]
    
    # cameron's code, if buggy blame him
    A.insert(0, average1/3)
    B.insert(0, average2/3)
        
    return [A, B]

def main():
    allPlayerData = {
'usr1':   {'dps': '3944', 'support': '1698', 'tank': '3682', 'queue': 'support'},
'usr2':   {'dps': '2970', 'support': '2282', 'tank': '1653', 'queue': 'support'},
'usr3':   {'dps': '3439', 'support': '3516', 'tank': '1677', 'queue': 'support'},
'usr4':   {'dps': '3606', 'support': '2407', 'tank': '3533', 'queue': 'support'},
'usr5':   {'dps': '2072', 'support': '1778', 'tank': '3733', 'queue': 'tank'},
'usr6':   {'dps': '2524', 'support': '1944', 'tank': '3710', 'queue': 'tank'},
'usr7':   {'dps': '3073', 'support': '3827', 'tank': '3335', 'queue': 'tank'},
'usr8':   {'dps': '3037', 'support': '2442', 'tank': '3254', 'queue': 'tank'},
'usr9':   {'dps': '3817', 'support': '2766', 'tank': '3894', 'queue': 'dps'},
'usr10':  {'dps': '2254', 'support': '2285', 'tank': '3639', 'queue': 'dps'},
'usr11':  {'dps': '1776', 'support': '1502', 'tank': '3808', 'queue': 'dps'},
'usr12':  {'dps': '1776', 'support': '3902', 'tank': '2488', 'queue': 'dps'}
}
    print(matchmake(allPlayerData))

main()

  
