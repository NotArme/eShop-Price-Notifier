#file to dump methods pertaining to local storage
#mainly used as a cache so requests are'nt used more than is actually needed

import os

from dateutil import parser
import datetime
import json

def CheckForDataFolder():
    if os.path.exists("./gameData"):
        return
    os.makedirs("./gameData")

def RecentDataExists(id):
    if os.path.exists(f"./gameData/{id}.json"):
        with open(f"./gameData/{id}.json", "r") as gameFile:
            game = json.load(gameFile)
            datetimeForEvaluation = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=23)
            if parser.parse(game["received date"]) > datetimeForEvaluation:
                gameFile.close()
                return True
            #current data is old, should re download
            gameFile.close()
    return False

def CacheGameData(gId, gData):
    CheckForDataFolder()
    with open(f"gameData/{gId}.json", "w+") as jsonfile:
        json.dump(gData, jsonfile)
        jsonfile.close()

def GetWishlist():
    if os.path.exists("./gameData/wishlist.json"):
        with open("./gameData/wishlist.json", "r+") as wishlistFile:
            wishlist = json.load(wishlistFile)
            wishlistFile.close()
    #else:
        #todo
    return wishlist