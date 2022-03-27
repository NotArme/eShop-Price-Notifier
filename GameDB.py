from time import sleep
import eShopPage
import LocalStorage

def UpdateLocalGameDB(attemptsToTry):
    batchSize = 10

    #initialazing some stuff
    gameTitles: dict[str, str] = {}
    currentGameId = 1
    badResponseStreak = 0
    tryCount = 0
    batchCount = 0

    #get current cache
    gameTitles = LocalStorage.LoadGameList()

    #web scrape loop
    while badResponseStreak < 5 and tryCount < attemptsToTry:
        print(f"\nTrying Id {currentGameId} ----- ", end=' ')
        if gameTitles.get(str(currentGameId), f"{currentGameId}_not_found") != f"{currentGameId}_not_found":
            print(f"Id {currentGameId}: found on cache", end= " ")
            badResponseStreak = 0
            currentGameId += 1
            continue
        tryCount += 1
        pageTree, pageResponse = eShopPage.GetPage(currentGameId)
        if pageResponse.status_code != 200:
            if pageResponse.status_code == 429:
                ra = pageResponse.headers["Retry-After"]
                print(f"too many requests on reached on ID {currentGameId}, sleeping for {ra} seconds...")
                sleep(float(ra))
                print("Retrying", end=' ')
                continue
            print(f"Id {currentGameId}: unexpected response: {pageResponse.status_code}", end=' ')
            badResponseStreak += 1
            currentGameId += 1
            continue
        else:
            badResponseStreak = 0
            gameTitles[currentGameId] = eShopPage.GetGameName(pageTree)
            print(f"Id {currentGameId}: Downloaded Title: {gameTitles[currentGameId]}", end=' ')
            imglink = eShopPage.GetGameImageLink(currentGameId)
            LocalStorage.SaveImage(imglink, currentGameId)
            batchCount += 1
            currentGameId += 1
        if batchCount >= batchSize:
            batchCount = 0
            print("\ncacheing past downloads...\n")
            LocalStorage.CacheGameList(gameTitles)
    
    print("\ncacheing past downloads...\n")
    LocalStorage.CacheGameList(gameTitles)
    print("\n\nProcess Completed :)")

UpdateLocalGameDB(1000)