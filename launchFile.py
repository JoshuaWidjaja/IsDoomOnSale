import json
import urllib.parse
import urllib.request
import difflib

DEAL_URL = 'https://www.cheapshark.com/api/1.0/deals'
SPECIFIC_DEAL_URL = 'https://www.cheapshark.com/api/1.0/deals?id'
GAME_LIST_URL = 'https://www.cheapshark.com/api/1.0/games'
GAME_LOOKUP_URL = 'https://www.cheapshark.com/api/1.0/games'
GAME_STORES_URL = 'https://www.cheapshark.com/api/1.0/stores'


TEST_URL = 'https://www.cheapshark.com/api/1.0/deals?sortBy=Price'

def main():
    print('Special thanks to CheapShark for allowing the use of their API for this project')
    print('\n')
    
    gameJsonResults = GetURLInfo(DEAL_URL)
    storeJsonResults = GetURLInfo(GAME_STORES_URL)
    resultList = list()
    storeIdDict = dict()
    counter = 1
    for stores in storeJsonResults:
        storeIdDict[stores['storeID']] = stores['storeName']
    #print(storeIdDict)

    while (True):
        print('If you\'d like to see all sales going on, type ALL SALES, else')
        userInput = input('Enter title of game to check sales or Q to quit: ')
        if userInput == 'Q':
            break
        elif userInput == 'ALL SALES':
            resultList = GetAllSales(gameJsonResults, storeIdDict)
        else:
            userInput = userInput.lower()
            for games in gameJsonResults:
                if userInput in games['title'].lower():
                    resultList.append([games['title'], games['normalPrice'], games['salePrice'], storeIdDict[games['storeID']]])
                else:
                    splitTitle = games['title'].lower().split()              
                    if difflib.get_close_matches(userInput, splitTitle):
                        resultList.append([games['title'], games['normalPrice'], games['salePrice'], storeIdDict[games['storeID']]])
        
        if len(resultList) == 0:
            print("Could not find any sales for your searched game.")
        else:
            print("Matches Found!")
            for results in sorted(resultList, key=lambda prices: float(prices[2])):
                print(str(counter) + '. ' + results[0] + " Normal Price: " + str(results[1]) + " // Currently on sale for: " + str(results[2]) + " at location " + results[3])
                counter += 1
        
        print("\n")
        counter = 1
        resultList.clear()

def GetURLInfo(url:str) -> dict:
    response = None
    try:
        response = urllib.request.urlopen(url)
        jsonInfo = response.read().decode(encoding = 'utf-8')
        return json.loads(jsonInfo)

    finally:
        if response != None:
            response.close()

def GetAllSales(gameJson, storeDict):
    results = list()
    counter = 1
    for games in gameJson:
        results.append([games['title'], games['normalPrice'], games['salePrice'], storeDict[games['storeID']]])
        counter += 1
    return results

if __name__ == "__main__":
    main()
