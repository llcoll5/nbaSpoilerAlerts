from NBA import NBA
from Wikihoops import Wikihoops

if __name__ == "__main__":
    nba = NBA()
    wikihoops = Wikihoops()

    print(nba.get_game_codes())
    print(wikihoops.get_game_ratings())