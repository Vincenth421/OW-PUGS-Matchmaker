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
        if roles != 0
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

    return 1

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

    # Finished adding all single role players
    else:
        return [queued, filled]

def splitRoles(queued, keys, tree):
    if len(keys) == 0
        return tree
    key = keys[0]
    roles = queued[key]["queue"]
    if #first digit is 1:
        tank = queued[key]
        tank["queue"] = "100"
        tree.setLeft(tank)
        splitRoles[keys[1:], tree.getLeft())
    if #second digit is 1:
        dps = queued[key]
        dps["queue"] = "010"
        tree.setMiddle(dps)
        splitRoles[keys[1:], tree.getMiddle())
    if #third digit is 1:
        supp = queued[key]
        supp["queue"] = "001"
        tree.setRight(supp)
        splitRoles[keys[1:], tree.getRight())
