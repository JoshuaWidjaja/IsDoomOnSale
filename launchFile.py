import json
import urllib.parse
import urllib.request
import difflib

DEAL_URL = 'https://www.cheapshark.com/api/1.0/deals'
SPECIFIC_DEAL_URL = 'https://www.cheapshark.com/api/1.0/deals?title='
GAME_LIST_URL = 'https://www.cheapshark.com/api/1.0/games'
GAME_LOOKUP_URL = 'https://www.cheapshark.com/api/1.0/games'
GAME_STORES_URL = 'https://www.cheapshark.com/api/1.0/stores'


TEST_URL = 'https://www.cheapshark.com/api/1.0/deals?sortBy=Price'

def main():
    print('Special thanks to CheapShark for allowing the use of their API for this project')
    print('\n')
    
    #Getting JSON info using both the general deal URL and stores URL. Also initializing variables.
    gameJsonResults = GetURLInfo(DEAL_URL)
    storeJsonResults = GetURLInfo(GAME_STORES_URL)
    resultList = list()
    storeIdDict = dict()
    counter = 1
    
    #Creates a dictionary that assigns all stores in the JSON file to be mapped from StoreID:StoreName
    for stores in storeJsonResults:
        storeIdDict[stores['storeID']] = stores['storeName']
    
    #Main loop
    while (True):
        print('If you\'d like to see 60 sales going on, type ALL SALES, else')
        userInput = input('Enter title of game to check sales or Q to quit: ')
        #Quit if user enters 'Q'
        if userInput == 'Q':
            break
        #Finds the cheapest 60 sales found in the general sales JSON data.
        elif userInput == 'ALL SALES':
            resultList = GetAllSales(gameJsonResults, storeIdDict)
        #Finds games that contained entered word(s) in their title and displays up to 60 sale results based on matches.
        else:
            userInput = userInput.lower()
            specificGameJsonResults = GetURLInfo(SPECIFIC_DEAL_URL + userInput)
            for games in specificGameJsonResults:
                if userInput in games['title'].lower():
                    resultList.append([games['title'], games['normalPrice'], games['salePrice'], storeIdDict[games['storeID']]])
        if len(resultList) == 0:
            print("Could not find any sales for your searched game.")
        #Displays results line by line based on what results were found and added to ResultList.
        else:
            print("Matches Found!")
            for results in sorted(resultList, key=lambda prices: float(prices[2])):
                print(str(counter) + '. ' + results[0] + " Normal Price: " + str(results[1]) + " // Currently on sale for: " + str(results[2]) + " at location " + results[3])
                counter += 1
        #Reset variables
        print("\n")
        counter = 1
        resultList.clear()

#Used to read and obtain JSON info from entered URL.
def GetURLInfo(url:str) -> dict:
    response = None
    try:
        response = urllib.request.urlopen(url)
        jsonInfo = response.read().decode(encoding = 'utf-8')
        return json.loads(jsonInfo)

    finally:
        if response != None:
            response.close()

#Helper function that assists wheen gathering general data from cheapest 60 games.
def GetAllSales(gameJson, storeDict):
    results = list()
    counter = 1
    for games in gameJson:
        results.append([games['title'], games['normalPrice'], games['salePrice'], storeDict[games['storeID']]])
        counter += 1
    return results

if __name__ == "__main__":
    main()


#Can be used somewhere else to find similarity
    # else:
    #     splitTitle = games['title'].lower().split()              
    #     if difflib.get_close_matches(userInput, splitTitle):
    #         resultList.append([games['title'], games['normalPrice'], games['salePrice'], storeIdDict[games['storeID']]])