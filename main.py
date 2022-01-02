import urllib3, requests, json, os
from tqdm import tqdm
from dotenv import load_dotenv

# get opendota api key from .env file
load_dotenv('.ENV')
KEY = os.getenv('KEY')

#create http object for api requests
http = urllib3.PoolManager()

def jsonprint(j):
    print(json.dumps(j, indent=4, sort_keys=True))

def getMatchIDs(steamID):
    p = http.request("GET", "https://api.opendota.com/api/players/" + str(steamID) + "/matches?api_key=" + str(KEY))
    matchData = json.loads(p.data)
    matchIdList = []
    for match in matchData:
        matchIdList.append(match["match_id"])
    return matchIdList

def hasItem(matchId, itemName, steamId):
    m = http.request("GET", "https://api.opendota.com/api/matches/" + str(matchId) + "?api_key=" + str(KEY))
    matchData = json.loads(m.data)
    if "players" in matchData:
        for player in matchData["players"]:
            if player["account_id"] == int(steamId):
                if player["purchase"] == None:
                    return -1
                else:
                    if itemName in player["purchase"]:
                        return player["win"]
                    else:
                        return -1

def winrateWithItem(itemName, IDList, steamId):
    gamesWithItem = 0
    winsWithItem = 0
    for ID in tqdm(IDList):
        matchResult = hasItem(ID, itemName, steamId)
        if matchResult == 1:
            winsWithItem = winsWithItem + 1
            gamesWithItem = gamesWithItem + 1
        elif matchResult == 0:
            gamesWithItem = gamesWithItem + 1
    if gamesWithItem == 0:
        return 0
    else: 
        return winsWithItem / gamesWithItem


def main():
    steamId = input("Enter the user's steam32 account ID: ")

    itemName = input("Enter the name of the item to check: ")

    # get a list of all match IDs containing player
    IDList = getMatchIDs(steamId)

    # count how many wins with item
    print(winrateWithItem(itemName, IDList, steamId))

if __name__ == "__main__":
    main()



