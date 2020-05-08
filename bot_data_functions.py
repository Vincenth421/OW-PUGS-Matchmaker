import numpy as np
import pickle
import random


def savePlayerData():
    ''' Saves the hashmap of player data.
    '''
    with open("data.pickle", "wb") as handle:
        pickle.dump(playerData, handle, protocol=pickle.HIGHEST_PROTOCOL)


def loadPlayerData():
    ''' Loads the hashmap of player data.
    '''
    with open('data.pickle', 'rb') as handle:
        playerData = pickle.load(handle)
    return playerData


playerData = loadPlayerData()
for player in playerData:
    playerData[player]["queue"] = "none"
    playerData[player]["team"] = -1


numQueued = {"tank":0, "dps":0, "support":0}


def queueFor(role, PlayerID):
    ''' Removes the player from the queue
        Sets the player's queued role to whatever they specified.
        Updates number of players queued for each role.
    '''
    deQueue(PlayerID)
    if role in playerData[PlayerID]:
        playerData[PlayerID]["queue"] = role
        if role == "tank":
            numQueued["tank"] += 1
            return ("Queued for tank.\n")
        elif role == "damage" or role == "dps":
            numQueued["dps"] += 1
            return ("Queued for dps.\n")
        elif role == "support":
            numQueued["support"] += 1
            return ("Queued for support.\n")
        elif role == "none":
            deQueue(PlayerID)
            return ("Left the queue.\n")
    else:
        return("Invalid role.\n")


def suppQueued():
    ''' Returns the number of support players needed to fill the queue.
    '''
    if numQueued["support"] < 4:
        numNeeded = 4 - numQueued["support"]
        return str(numNeeded)
    else:
        return 0

    
def tankQueued():
    ''' Returns the number of tank players needed to fill the queue.
    '''
    if numQueued["tank"] < 4:
        numNeeded = 4 - numQueued["tank"]
        return str(numNeeded)
    else:
        return 0


def dpsQueued():
    ''' Returns the number of dps players needed to fill the queue.
    '''
    if numQueued["dps"] < 4:
        numNeeded = 4 - numQueued["dps"]
        return str(numNeeded)
    else:
        return 0


def allQueued():
    if dpsQueued() != 0:
        return False
    if tankQueued() != 0:
        return False
    if suppQueued() != 0:
        return False
    return True


def deQueue(PlayerID):
    ''' Removes the player from the queue.
        Updates number of players queued for each role.
    '''
    role = playerData[PlayerID]["queue"]
    playerData[PlayerID]["queue"] = "none"
    if role == "tank":
        numQueued["tank"] -= 1
    elif role == "damage" or role == "dps":
        numQueued["dps"] -= 1
    elif role == "support":
        numQueued["support"] -= 1
    elif role == "none":
        return "Not in queue.\n"
    return "Left the queue.\n"

    
#good work gang
def updatePlayerData(mystr, PlayerID):
    ''' Updates the hashmap of PlayerID's data.
    '''
    userData = mystr.split()
    if userData[1].isalpha():
        return False
    sr = int(userData[1])
    if sr < 0:
        return False
    if PlayerID not in playerData:
        playerData[PlayerID] = {}
    if(userData[0] == "!support"):
        playerData[PlayerID]["support"] = sr
    elif(userData[0] == "!damage" or userData[0] == "!dps"):
        playerData[PlayerID]["dps"] = sr
    elif(userData[0] == "!tank"):
        playerData[PlayerID]["tank"] = sr
    playerData[PlayerID]["queue"] = "none"
    playerData[PlayerID]["team"] = -1
    # print(playerData)
    savePlayerData()
    return True


def clearPlayerData():
    ''' Clears playerData of everything.
    '''
    playerData.clear()
    savePlayerData()
    return playerData


def getPlayerData(PlayerID):
    ''' Returns a specific player's data.
        If possible, should be formatted.
    '''
    return playerData[PlayerID]


def printPlayerData(PlayerID):
    message = ""
    for key in playerData[PlayerID].keys():
        if key == "support":
            message = message + "\nSupport: " + str(playerData[PlayerID]["support"])
        elif key == "dps":
            message = message + "\nDPS: " + str(playerData[PlayerID]["dps"])
        elif key == "tank":
            message = message + "\nTank: " + str(playerData[PlayerID]["tank"])
    if message == "":
        message = "No SR data recorded."
    return message


def printQueueData(PlayerID):
    if playerData[PlayerID]["queue"] == "none":
        message = " is not queued!"
    else:
        message = " is queued for: " + playerData[PlayerID]["queue"]
    return message


def printQueue():
    queue = ""
    for player in playerData.keys():
        if playerData[player]["queue"] != "none":
            queue = queue + player[:-5] + ": " + playerData[player]["queue"] + "\n"
    if queue == "":
        queue = "Nobody is in queue."
    return queue


def getAllPlayerData():
    ''' Returns all player's data.
        If possible, should be formatted.
    '''
    return playerData

def getTeam1(mmData):
    ''' Gets team 1.
    '''
    team1 = {}
    for player in mmData.keys():
        if mmData[player]["team"] == 1:
            team1[player] = mmData[player]["queue"]
    return team1

            
def getTeam2(mmData):
    ''' Gets team 2.
    '''
    team2 = {}
    for player in mmData.keys():
        if mmData[player]["team"] == 2:
            team2[player] = mmData[player]["queue"]
    return team2

def printTeams(mmData):
    team1 = getTeam1(mmData)
    team2 = getTeam2(mmData)
    teamA = "Team 1:\n"
    teamB = "Team 2:\n"
    for player in team1.keys():
        teamA = teamA + player + "\t\t\t\t"
        teamA = teamA + mmData[player]["queue"]
        teamA = teamA + "\n"
    for player in team2.keys():
        teamB = teamB + player + "\t\t\t\t"
        teamB = teamB + mmData[player]["queue"]
        teamB = teamB + "\n"
    message = "\n" + teamA + "\n" + teamB
    return message
     

