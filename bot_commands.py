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
    selectedPlayers = select(playerData)
    roles = split(selectedPlayers)
    
    tank = roles[0]
    dps = roles[1]
    supp = roles[2]
    
    t = matchmake(tank)
    d = matchmake(dps)
    s = matchmake(supp)
    
    return combine(t, d, s)

# selects 12 players from a pool of any number
def select(playerData):
    list = []
    selected = {}
    
    for i in playerData.keys:
        list.append(playerData[i])

    for i in range(12):
        num = random.randint(0, len(list)-1)
        #TODO check for dupe random numbers
        selected[list[num]] = playerData[list[num]].get()

    return selected
        
# ready is a bool
# playerData is a hash table of 12 people
# splits all players into their chosen roles
def split(playerData):
  tank = []
  dps = []
  supp = []
  
  for name in playerData.keys: 
    if playerData[name]['ready']:
      if playerData[name]['tankSR'] != -1:
      	tank.append([name, playerData[name]['tankSR']])
      if playerData[name]['dpsSR'] != -1:
      	dps.append([name, playerData[name]['dpsSR']])
      if playerData[name]['suppSR'] != -1:
      	supp.append([name, playerData[name]['suppSR']])
  
  return [tank, dps, supp]

# given a role hash table
# add to the value bucket a new entry, Team A or B
# 6 members on A, 6 on B
# as even SR spread as possible
# Assume that role is a list of length 4
def balance(role):
    totalsr = 0
    for i in range(len(role)):
        totalsr += role[i][1]

    bestPair = []
    average2 = 0
    bestDifference = 5000
  
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
    
  
  
