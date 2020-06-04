import numpy as np

# playerData[names]["queue"] contains a 3 digit string, 000, 001, 010, 011, 100, 101, and 111
# each respectively hold a role, first being tank, second being dps, third being support

# main function that matchmakes players, now with multirole!
def matchmake(playerData):
    queued = {}
    for names in playerData.keys():
        roles = playerData[names]["queue"]
        if roles != 0
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

