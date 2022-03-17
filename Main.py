#other files from repo
from LocalStorage import *

#json and html handling
import json
import requests
import ast
from lxml import html

#time stuff
import datetime
from dateutil import parser

userAgent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}

class CountryPrice(dict):
    def __init__(self, country, price):
        self["country"] = country
        self["price"] = price

def GetPage(gameId: int):
    url = "https://eshop-prices.com/games/" + str(gameId) + "?currency=BRL"
    htmlpage = requests.get(url, headers=userAgent)

    tree = html.fromstring(htmlpage.content)
    return tree

def GetGameName(tree):
    gameNameQuery = '//div[@class="hero game-hero"]/div[2]//h1/text()'
    gameName = tree.xpath(gameNameQuery)
    return gameName[0]

def GetImage(tree):
    gameImageQuery = '//div[@class="hero game-hero"]/div[2]//picture/source[@type="image/jpeg"]/@srcset'
    gameImageLink = tree.xpath(gameImageQuery)
    return gameImageLink[0]

def GetLowestPrice(tree):
    countryAndPriceQuery = '//table[@class="prices-table"]/tbody/tr[1]/td[2]/text() | //table[@class="prices-table"]/tbody/tr[1]/td[4]/text() | //table[@class="prices-table"]/tbody/tr[1]/td[4]//div[@class="discounted"]/text()'
    cheapestItem: list = tree.xpath(countryAndPriceQuery)

    # Correct items received
    i=0
    while i < len(cheapestItem):
        if cheapestItem[i] == "\n":
            del cheapestItem[i]
            continue
        cheapestItem[i] = str(cheapestItem[i]).strip("\n").strip("R$") #strip useless chars
        cheapestItem[i] = str(cheapestItem[i]).replace(",",".") #change cent separator from , to .
        i += 1


    testprice = CountryPrice(cheapestItem[0], cheapestItem[1])
    return testprice

def GetAveragePrice(daysToEvaluate: int, gameId: int):
    priceList = requests.get("https://charts.eshop-prices.com/prices/" + str(gameId) +"?currency=BRL", headers=userAgent)
    priceListDecoded : list = ast.literal_eval(priceList.text)
    datetimeForEvaluation = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=daysToEvaluate)

    for entry in priceListDecoded:
        entry["date"] = parser.parse(entry["date"])
        if entry["date"] < datetimeForEvaluation:
            priceListDecoded.remove(entry)

    averagePrice: float = 0

    for entry in priceListDecoded:
        #value is received as an int, dividing by 100 correctly sets them to cents
        averagePrice += (entry["value"]/100)
    averagePrice /= len(priceListDecoded)

    return averagePrice

#def ShouldNotify
    #todo
    #return bool
    #true if cheaper than price marked on wishlist

def GetGameData(gameId, tree, daysToEvaluate):
    gameName = GetGameName(tree)
    imageBytes = GetImage(tree)
    cp = GetLowestPrice(tree)
    ap = GetAveragePrice(daysToEvaluate, gameId)

    gameData = {
        "game": gameName,
        "country": cp["country"],
        "lowest price": cp["price"],
        "average price": ap,
        "received date": str(datetime.datetime.now(datetime.timezone.utc))
    }
    
    return gameData


def Main():
    
    wishlist = GetWishlist()

    for game in wishlist:

        if (RecentDataExists(game["gameId"]) == False):
            tree = GetPage(game["gameId"])
            gameData = GetGameData(game["gameId"], tree, 365)

            CacheGameData(game["gameId"], gameData)

if __name__ == "__main__":
    Main()