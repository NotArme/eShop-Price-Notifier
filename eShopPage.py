#other files from repo
from Main import allGames
from LocalStorage import *

#json and html handling
import requests
import ast
from lxml import html

#time stuff
import datetime
from dateutil import parser

def CreateSession():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-user': '?1'}
    s = requests.Session()
    s.headers = headers
    return s

class SessionInstance():
    def __init__(self, session):
        self.s = session

activeSession = SessionInstance(CreateSession()).s


class CountryPrice(dict):
    def __init__(self, country, price):
        self["country"] = country
        self["price"] = price

def GetPage(gameId: int, session: requests.Session):
    url = "https://eshop-prices.com/games/" + str(gameId) + "?currency=BRL"
    htmlpage = session.get(url)

    tree = html.fromstring(htmlpage.content)
    return tree, htmlpage

def GetGameName(tree):
    gameNameQuery = '//div[@class="hero game-hero"]/div[2]//h1/text()'
    gameName = tree.xpath(gameNameQuery)
    return gameName[0]

#probably not useful actually, found a better method
def GetGameImageFromTree(tree):
    gameImageQuery = '//div[@class="hero game-hero"]/div[2]//picture/source[@type="image/jpeg"]/@srcset'
    gameImageLink = tree.xpath(gameImageQuery)
    return gameImageLink[0]

def GetGameImageLink(gameId):
    return f"https://images.eshop-prices.com/games/{gameId}/120w.jpeg"

def GetLowestPrice(tree):
    countryAndPriceQuery = '//table[@class="prices-table"]/tbody/tr[1]/td[2]/text() | //table[@class="prices-table"]/tbody/tr[1]/td[4]/text() | //table[@class="prices-table"]/tbody/tr[1]/td[4]//div[@class="discounted"]/text()'
    cheapestItem: list = tree.xpath(countryAndPriceQuery)

    # Correct items received
    i=0
    countryFound = False
    while i < len(cheapestItem):
        if cheapestItem[i] == "\n":
            del cheapestItem[i]
            continue
        cheapestItem[i] = str(cheapestItem[i]).strip("\n") #strip useless chars
        if countryFound: #price always comes after country on array, no use checking for it before finding the country
            cheapestItem[i] = RemoveNonNumericals(str(cheapestItem[i]))
            cheapestItem[i] = str(int(cheapestItem[i])/100) #adding back separator
        countryFound = True
        i += 1

    if len(cheapestItem) < 2:
        return CountryPrice("Not Found", "00.00")
    testprice = CountryPrice(cheapestItem[0], cheapestItem[1])
    return testprice

def GetPriceHistory(daysToEvaluate: int, gameId: int, session: requests.Session):
    priceList = session.get("https://charts.eshop-prices.com/prices/" + str(gameId) +"?currency=BRL")
    if priceList.status_code != 200:
        return {}
    priceListDecoded : list = ast.literal_eval(priceList.text)
    if len(priceListDecoded) == 0:
        return {}
    datetimeForEvaluation = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=daysToEvaluate)

    for entry in priceListDecoded:
        entry["date"] = parser.parse(entry["date"])
        if entry["date"] < datetimeForEvaluation:
            priceListDecoded.remove(entry)
    
    return priceListDecoded

def GetAveragePrice(priceHistory):
    if len(priceHistory) == 0:
        return 00.00

    averagePrice: float = 0

    for entry in priceHistory:
        #value is received as an int, dividing by 100 correctly sets them to brazilian cents
        averagePrice += (entry["value"]/100)
    averagePrice /= len(priceHistory)

    return averagePrice

#def ShouldNotify
    #todo
    #return bool
    #true if cheaper than price marked on wishlist

def GetGameData(gameId, daysToEvaluate, sleep = False):
    if (RecentDataExists(gameId) != False):
        return LoadGameData(gameId)
    if sleep:
        sleep(1) #sleeping a bit to avoid getting blocked for too many requests
    tree, resp = GetPage(gameId, activeSession)
    if resp.status_code != 200:
        cp = CountryPrice("not found", 000.00)
    else:
        cp = GetLowestPrice(tree)

    ph = GetPriceHistory(daysToEvaluate, gameId, activeSession)
    ap = GetAveragePrice(ph)
    #todo: hdimage

    gameData = {
        "game": allGames[gameId ],
        "country": cp["country"],
        "lowest price": cp["price"],
        "average price": ap,
        "received date": str(datetime.datetime.now(datetime.timezone.utc)),
        "price history": ph
    }

    CacheGameData(gameId, gameData)
    
    return gameData

def LoadWishlist(wishlist):
    for game in wishlist:
        
            
            gameData = GetGameData(game["gameId"], 365)

            CacheGameData(game["gameId"], gameData)


def RemoveNonNumericals(string: str) -> str:
    result = ''
    for char in string:
        if char in '1234567890':
            result += char
    return result