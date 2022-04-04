#file to dump methods pertaining to local storage
#mainly used as a cache so requests are'nt used more than is actually needed

import os

from dateutil import parser
import datetime
import json
import requests

import pickle
from time import sleep


def SaveImage(url, gameId):
    img = requests.get(url)
    if img.status_code == 200:
        img_data =  img.content
        with open(f'gameData/{gameId}.jpg', 'wb') as writer:
            writer.write(img_data)
        print(" --- Image downloaded", end=" ")
    else:
        if img.status_code == 429:
            ra = img.headers["Retry-After"]
            print(f"too many requests while getting image for ID {gameId}, sleeping for {ra} seconds...")
            sleep(float(ra))
            print("Retrying", end=' ')
            SaveImage(url, gameId)
            return
        print(f"\ncould not get image for Id {gameId} --- Response: {img.status_code}", end=" ")

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

def CacheGameList(gamedict):
    CheckForDataFolder()
    with open(f"gameData/.gamedb.json", "w+") as jsonfile:
        json.dump(gamedict, jsonfile)
        jsonfile.close()

def LoadGameList():
    CheckForDataFolder()
    if os.path.exists("./gameData/.gamedb.json"):
        with open("./gameData/.gamedb.json", "r+") as gameListFile:
            gamedb = json.load(gameListFile)
            gameListFile.close()
            return gamedb
    else:
        return {}

def CacheIgnoreList(ignoreList):
    CheckForDataFolder()
    with open(f"gameData/.404list", "wb") as ignoreListFile:
        pickle.dump(ignoreList, ignoreListFile)
        ignoreListFile.close()

def LoadIgnoreList():
    CheckForDataFolder()
    if os.path.exists("./gameData/.404list"):
        with open(f"gameData/.404list", "rb") as ignoreListFile:
            list = pickle.load(ignoreListFile)
            ignoreListFile.close
            return list
    return []

def CacheWishlist(wishlist):
    CheckForDataFolder()
    with open(f"gameData/.wishlist", "wb") as wishlistFile:
        pickle.dump(wishlist, wishlistFile)
        wishlistFile.close()

def LoadWishlist():
    if os.path.exists("./gameData/.wishlist"):
        with open("./gameData/.wishlist", "rb") as wishlistFile:
            wishlist: list = pickle.load(wishlistFile)
            return wishlist
    else:
        return []