from Requester import RequestGetter

class Wikihoops(RequestGetter):
    def __init__(self, 
                 url="https://wikihoops.com/api/update?v=3.4.0&cs",
                 headers=None):
        super().__init__(url, headers)

    def get_yesterdays_games(self):
        self.games = self.get_content().get('games', [])
        self.yesterdays_games = [game for game in self.games if game.get("isToday") == False]
        return self.yesterdays_games
    
    def get_game_ratings(self):
        self.get_yesterdays_games()
        return {game["id"]: game.get("rating", {}).get("value") for game in self.yesterdays_games}

    def get_game_codes(self):
        self.get_yesterdays_games()
        return [game["gameCode"] for game in self.yesterdays_games]


if __name__ == "__main__":
    wikihoops = Wikihoops()
    print(wikihoops.get_game_ratings())