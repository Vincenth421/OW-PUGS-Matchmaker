import numpy as np
import json
import random


def savePlayerData(playerData):
    ''' Saves the hashmap of player data.
    '''
    with open("data.json", "w") as f:
        json.dump(playerData, f, indent=4)


def loadPlayerData():
    ''' Loads the hashmap of player data.
    '''
    with open('data.json', 'r') as f:
        playerData = json.load(f)
    return playerData


playerData = loadPlayerData()
for player in playerData:
    playerData[player]["queue"] = "none"
    playerData[player]["team"] = -1

def clearQueue():
    for player in playerData:
        playerData[player]["queue"] = "none"
    savePlayerData(playerData)
clearQueue()


numQueued = {"tank":0, "dps":0, "support":0}


def queueFor(role, PlayerID):
    ''' Removes the player from the queue
        Sets the player's queued role to whatever they specified.
        Updates number of players queued for each role.
    '''
    deQueue(PlayerID)
    if role in playerData[PlayerID]:
        playerData[PlayerID]["queue"] = role
        savePlayerData(playerData)
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

# adjusts player sr based on winning team
# no adjustments if tie
# winner must be either 0, 1, or 2
# playerData is a hashtable of all players
def adjust(winner):
    playerData = loadPlayerData()
    
    if(winner == 0):
        return playerData
    
    for player in playerData.keys():
        if(playerData[player]['team'] == winner):
            role = playerData[player]['queue']
            playerData[player][role] += 100
        elif(playerData[player]['team'] != -1):
            role = playerData[player]['queue']
            playerData[player][role] -= 100
        playerData[player]['team'] = -1
        playerData[player]['queue'] = 'none'

    savePlayerData(playerData)
    return playerData


def dpsQueued():
    ''' Returns the number of dps players needed to fill the queue.
    '''
    if numQueued["dps"] < 4:
        numNeeded = 4 - numQueued["dps"]
        return str(numNeeded)
    else:
        return 0


def allQueued():
    ''' Returns true if all queue conditions are met.
    '''
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
    role = userData[0][1:]
    if userData[1].isalpha():
        return False
    sr = int(userData[1])
    if sr < 0 or sr > 5000:
        return False
    if PlayerID not in playerData:
        playerData[PlayerID] = {}
    if(role == "support" or role == "supp"):
        playerData[PlayerID]["support"] = sr
    elif(role == "damage" or role == "dps"):
        playerData[PlayerID]["dps"] = sr
    elif(role == "tank"):
        playerData[PlayerID]["tank"] = sr
    playerData[PlayerID]["queue"] = "none"
    playerData[PlayerID]["team"] = -1
    # print(playerData)
    savePlayerData(playerData)
    return True


def clearPlayerData():
    ''' Clears playerData of everything.
    '''
    playerData.clear()
    savePlayerData(playerData)
    return playerData


def getPlayerData(PlayerID):
    ''' Returns a specific player's data.
        If possible, should be formatted.
    '''
    pData = loadPlayerData()
    return pData[PlayerID]


def printPlayerData(PlayerID):
    ''' Returns a formatted string with specific user data.
    '''
    pData = getAllPlayerData()
    message = ""
    for key in pData[PlayerID].keys():
        if key == "support":
            message = message + "\nSupport: " + str(pData[PlayerID]["support"])
        elif key == "dps":
            message = message + "\nDPS: " + str(pData[PlayerID]["dps"])
        elif key == "tank":
            message = message + "\nTank: " + str(pData[PlayerID]["tank"])
    if message == "":
        message = "No SR data recorded."
    message = PlayerID[:-5] + message
    return message


def printAllPlayerData():
    ''' Returns a formatted string with all user data.
    '''
    message = ""
    for PlayerID in playerData.keys():
        message = message + printPlayerData(PlayerID) + "\n\n"
    if message == "":
        message = "No SR data recorded."
    return message


def printQueueData(PlayerID):
    ''' Returns a formatted string about a specific user's queue status.
    '''
    if playerData[PlayerID]["queue"] == "none":
        message = " is not queued!"
    else:
        message = " is queued for: " + playerData[PlayerID]["queue"]
    return message


def printQueue():
    ''' Returns a formatted string with all the users in queue.
    '''
    pData = getAllPlayerData()
    queue = ""
    for player in pData.keys():
        if pData[player]["queue"] != "none":
            queue = queue + player[:-5] + ": " + pData[player]["queue"] + "\n"
    if queue == "":
        queue = "Nobody is in queue."
    return queue


def getAllPlayerData():
    ''' Returns all player's data.
        If possible, should be formatted.
    '''
    pData = loadPlayerData()
    return pData


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


def printTeams(mmList):
    ''' Returns a formatted string containing all players for both teams.
    '''
    mmData = mmList[0]
    team1 = getTeam1(mmData)
    team2 = getTeam2(mmData)
    teamA = "Team 1: Avg = " + str(mmList[1]) + "\n"
    teamB = "Team 2: Avg = " + str(mmList[2]) + "\n"
    for player in team1.keys():
        if mmData[player]["queue"] == "support":
            teamA = teamA + mmData[player]["queue"] + "\t\t\t"
        else:
            teamA = teamA + mmData[player]["queue"] + "\t\t\t\t"
        teamA = teamA + player
        teamA = teamA + "\n"
    for player in team2.keys():
        if mmData[player]["queue"] == "support":
            teamB = teamB + mmData[player]["queue"] + "\t\t\t"
        else:
            teamB = teamB + mmData[player]["queue"] + "\t\t\t\t"
        teamB = teamB + player
        teamB = teamB + "\n"
    message = "\n" + teamA + "\n" + teamB
    return message


def getPlayerTeam(playerID):
    playerData = loadPlayerData()
    team = str(playerData[playerID]["team"])
    return team

