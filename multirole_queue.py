import numpy as np

class Node():

    def __init__(self, data):

        self.left = None
        self.right = None
        self.middle = None
        self.data = data

    def setLeft(left):
        self.left = left

    def setRight(right):
        self.right = right

    def setMiddle(mid):
        self.middle = mid

    def get():
        return self.data

    def getLeft():
        return self.left

    def getMiddle():
        return self.middle

    def getRight():
        return self.right

# playerData[names]["queue"] contains a 3 digit string, 000, 001, 010, 011, 100, 101, and 111
# each respectively hold a role, first being tank, second being dps, third being support

# main function that matchmakes players, now with multirole!
def matchmake(playerData):
    queued = {}
    for names in playerData.keys():
        roles = playerData[names]["queue"]
        if roles != "000":
            queued[names] = playerData[names]
    if queued < 12:
        #TODO: return error
    if queued > 12:
        #TODO: don't worry for now, it's gonna be hard to implement, might be impossible tbh
    
    #TODO: prolly need to store result in var, not sure what result is
    finished = singlerole(queued, 0, 0, 0, {})

    if len(finished[1]) == 12:
        #put them into teams

    #TODO: actual multirole part
    head = Node("")
    keys = finished[0].keys()
    split(finished[0], keys, head)

    #head now has tree of all possible permutations of player roles
    #now just need to make teams from all paths in the tree
    #and find which one is the most balanced out of all of them
    
    return 1

# finds all single role players, and if a role filled, goes again
def singlerole(queued, tank, dps, supp, filled):
    for names in queued.keys():
        roles = queued[names]["queue"]
        #TODO: once confirmed for a role, remove from queued
        if roles == "100":
            tank += 1
            filled[names] = queued[names]
        elif roles == "010":
            dps += 1
            filled[names] = queued[names]
        elif roles == "001":
            supp += 1
            filled[names] = queued[names]

    # check if 4 tanks single roling
    if tank == 4:
        for names in queued.keys():
            queued[names]["queue"] = "0" + queued[names]["queue"][1:]
        return singlerole(queued, -1, dps, supp, filled)

    # check if there are exactly enough multirole players as is remaining tank players
    elif tank >= 0:
        num = 0
        temp = {}
        for names in queued.keys():
            if queued[names]["queue"][0] == "1":
                temp[names] = queued[names]
                temp[names]["queue"] = "100"
                num += 1
        if num == (4-tank):
            for names in temp.keys():
                filled[names] = temp[names]
            return singlerole(queued, -1, dps, supp, filled)

    # check if 4 dps are single roling
    elif dps == 4:
        for names in queued.keys():
            queued[names]["queue"] = queued[names]["queue"][:1] + "0" + queued[names]["queue"][2:]
        return singlerole(queued, tank, -1, supp, filled)

    # check if there are exactly enough multirole players as is remaining dps players
    elif dps >= 0:
        num = 0
        temp = {}
        for names in queued.keys():
            if queued[names]["queue"][1] == "1":
                temp[names] = queued[names]
                temp[names]["queue"] = "010"
                num += 1
        if num == (4-dps):
            for names in temp.keys():
                filled[names] = temp[names]
            return singlerole(queued, tank, -1, supp, filled)

    # check if 4 supp are single roling
    elif supp == 4:
        for names in queued.keys():
            queued[names]["queue"] = queued[names]["queue"][:2] + "0"
        return singlerole(queued, tank, dps, -1, filled)

    # check if there are exactly enough multirole players as is remaining supp players
    elif supp >= 0:
        num = 0
        temp = {}
        for names in queued.keys():
            if queued[names]["queue"][2] == "1":
                temp[names] = queued[names]
                temp[names]["queue"] = "001"
                num += 1
        if num == (4-supp):
            for names in temp.keys():
                filled[names] = temp[names]
            return singlerole(queued, tank, dps, -1, filled)

    # Finished adding all single role players
    else:
        return [queued, filled]

#TODO: might need to return head pointer instead of nothing, not sure
def splitRoles(queued, keys, tree):
    if len(keys) == 0
        return
    key = keys[0]
    roles = queued[key]["queue"]
    # if is queued for tank, then single it out and add it to tree
    if roles[0] == "1":
        tank = queued[key]
        tank["queue"] = "100"
        tree.setLeft(tank)
        splitRoles(queued, keys[1:], tree.getLeft())
    # if is queued for dps, then single it out and add it to tree
    if roles[1] == "1":
        dps = queued[key]
        dps["queue"] = "010"
        tree.setMiddle(dps)
        splitRoles(queued, keys[1:], tree.getMiddle())
    # if is queued for supp, then single it out and add it to tree
    if roles[2] == "1":
        supp = queued[key]
        supp["queue"] = "001"
        tree.setRight(supp)
        splitRoles(queued, keys[1:], tree.getRight())
    return
    
# PSEUDOCODE BELOW:                   
def valid_queued_players(queued):
    # Need >= 12 people queued
    num_tanks = 0
    num_dps = 0
    num_supp = 0
    singled_queued = {}
    result = []

    result = singlerole(queued, num_tanks, num_dps, num_supp, singled_queued)
    #singlerole returns [queued, filled]
    result[0] = queued
    result[1] = singled_queued

    #count all single queued people
    for role in singled_queued:
        if role == tank:
            num_tanks = num_tanks + 1
        if role == dps:
            num_dps = num_dps + 1
        if role == supp:
            num_supp = num_supp + 1

    for roles in queued:
        if role == tank-dps or tank-supp or dps-supp:
            num_doubles = num_doubles + 1
        if role == fill:
            num_fills = num_fills + 1
    
    if num_fills > num_doubles:
        return 1

    #count all double queued people
    for role in queued:
        if role == tank-supp:
            num_tanks = num_tanks + 0.5
            num_supp = num_supp + 0.5
        if role == tank-dps:
            num_tanks = num_tanks + 0.5
            num_dps = num_dps + 0.5
        if role == supp-dps:
            num_supp = num_supp + 0.5
            num_dps = num_dps + 0.5
        if role == fill:
            num_tanks = num_tanks + 0.34
            num_supp = num_supp + 0.34
            num_dps = num_dps + 0.34


    if num_tanks >= 4 and num_dps >= 4 and num_supp >= 4:
        return(1)
    else:
        return(0)
    
    
                   
def main():
    allPlayerData = {
'usr1':   {'dps': 3944, 'support': 1698, 'tank': 3682, 'queue': 'support', 'team': -1},
'usr2':   {'dps': 2970, 'support': 2282, 'tank': 1653, 'queue': 'support', 'team': -1},
'usr3':   {'dps': 3439, 'support': 3516, 'tank': 1677, 'queue': 'support', 'team': -1},
'usr4':   {'dps': 3606, 'support': 2407, 'tank': 3533, 'queue': 'support', 'team': -1},
'usr5':   {'dps': 2072, 'support': 1778, 'tank': 3733, 'queue': 'tank', 'team': -1},
'usr6':   {'dps': 2524, 'support': 1944, 'tank': 3710, 'queue': 'tank', 'team': -1},
'usr7':   {'dps': 3073, 'support': 3827, 'tank': 3335, 'queue': 'tank', 'team': -1},
'usr8':   {'dps': 3037, 'support': 2442, 'tank': 3254, 'queue': 'tank', 'team': -1},
'usr9':   {'dps': 3817, 'support': 2766, 'tank': 3894, 'queue': 'dps', 'team': -1},
'usr10':  {'dps': 2254, 'support': 2285, 'tank': 3639, 'queue': 'dps', 'team': -1},
'usr11':  {'dps': 1776, 'support': 1502, 'tank': 3808, 'queue': 'dps', 'team': -1},
'usr12':  {'dps': 1776, 'support': 3902, 'tank': 2488, 'queue': 'dps', 'team': -1}
}
                   
                   
