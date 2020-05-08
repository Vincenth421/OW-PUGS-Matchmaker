import numpy as np
import pickle

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
for player in playerData:
    playerData[player]["queue"] = "none"
    playerData[player]["team"] = "none"

numQueued = {"tank":0, "damage":0, "support":0}


def queueFor(role, PlayerID):
    deQueue(PlayerID)
    if role in playerData[PlayerID]:
        playerData[PlayerID]["queue"] = role
        if role == "tank":
            numQueued["tank"] += 1
            return ("Queued for tank.\n")
        elif role == "damage" or role == "dps":
            numQueued["damage"] += 1
            return ("Queued for dps.\n")
        elif role == "support":
            numQueued["support"] += 1
            return ("Queued for support.\n")
        elif role == "none":
            deQueue(PlayerID)
            return ("Left the queue.\n")
        else:
            return("Invalid role.\n")
    else:
        return("Please input your SR for that role!\n")

    

def suppQueued():
    if numQueued["support"] < 4:
        numNeeded = 4 - numQueued["support"]
        return str(numNeeded)
    else:
        return 0
    
def tankQueued():
    if numQueued["tank"] < 4:
        numNeeded = 4 - numQueued["tank"]
        return str(numNeeded)
    else:
        return 0

def dpsQueued():
    if numQueued["damage"] < 4:
        numNeeded = 4 - numQueued["damage"]
        return str(numNeeded)
    else:
        return 0

def deQueue(PlayerID):
    role = playerData[PlayerID]["queue"]
    playerData[PlayerID]["queue"] = "none"
    if role == "tank":
        numQueued["tank"] -= 1
    elif role == "damage" or role == "dps":
        numQueued["damage"] -= 1
    elif role == "support":
        numQueued["support"] -= 1
    
    
#good work gang
def updatePlayerData(mystr, PlayerID):
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
    playerData[PlayerID]["team"] = "none"
    print(playerData)
    savePlayerData()
    return True


def clearPlayerData():
    playerData.clear()
    savePlayerData()
    return playerData


def getPlayerData(PlayerID):
    # I'd like for this to return a nice and cleanly formatted string with
    # the player data
    return playerData[PlayerID]

def getAllPlayerData():
    return playerData
