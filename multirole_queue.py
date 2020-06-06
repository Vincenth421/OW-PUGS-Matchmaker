import numpy as np

# playerData[names]["queue"] contains a 3 digit string, 000, 001, 010, 011, 100, 101, and 111
# each respectively hold a role, first being tank, second being dps, third being support

# main function that matchmakes players, now with multirole!
def matchmake(playerData):
    queued = {}
    for names in playerData.keys():
        roles = playerData[names]["queue"]
        if roles != "000"
            queued[names] = playerData[names]
    if queued < 12:
        #TODO: return error
    if queued > 12:
        #TODO: don't worry for now, it's gonna be hard to implement, might be impossible tbh
    
    #TODO: prolly need to store result in var, not sure what result is
    finished = singlerole(queued, 0, 0, 0, {})

    #TODO: actual multirole part
    return finished

# finds all single role players, and if a role filled, goes again
def singlerole(queued, tank, dps, supp, filled):
    for names in queued.keys():
        roles = queued[names]["queue"]
        if roles == "100":
            tank += 1
            filled[names] = queued[names]
        elif roles == "010":
            dps += 1
            filled[names] = queued[names]
        elif roles == "001":
            supp += 1
            filled[names] = queued[names]

    #TODO: MAIN ISSUE!!! TODO: how to store players and roles to return, tied to TODOs below

    if tank == 4:
        #TODO change first digit to 0
        for names in queued.keys():
            #queued[names]["queue"] -= 100
        return singlerole(queued, 0, dps, supp, filled)

    elif dps == 4:
        #TODO: change second digit to 0
        for names in queued.keys():
            #queued[names]["queue"] -= 10
        return singlerole(queued, tank, 0, supp, filled)

    elif supp == 4:
        # TODO: change third digit to 0
        for names in queued.keys():
            #queued[names]["queue"] -= 1
        return singlerole(queued, tank, dps, 0, filled)
        
    elif len(filled) == 12:
        #TODO: ur done, go play
        return 1

    else:
        #TODO: ur not done, go multirole
        return 0

    
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
    
