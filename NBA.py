from Requester import RequestGetter

class NBA(RequestGetter):
    def __init__(self, 
                 url="https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json",
                 headers={
                    "Origin": "https://www.nba.com",
                    "Referer": "https://www.nba.com/",
                    "User-Agent": "Mozilla/5.0",
                    "Accept": "application/json"
                }):
        super().__init__(url, headers)

    def get_games(self):
        self.games = self.get_content().get("scoreboard", {}).get("games", [])
        return self.games
    

    def get_game_codes(self):
        self.get_games()
        return [game["gameCode"].replace("/", "") for game in self.games]

    def get_date_from_game_code(self, game_code):
        return game_code.split("/")[0]

    def get_teams_from_game_code(self, game_code):
        teams = game_code.split("/")[1]
        first_team, second_team = teams[:3], teams[3:]
        return [first_team, second_team]

    def get_game_urls(self):
        self.get_games()
        self.game_urls = {}
        for game in self.games:
            game_code = game["gameCode"].replace("/", "")
            gameid = game.get("gameId")
            teams = self.get_teams_from_game_code(game["gameCode"])
            slug = f"{teams[0].lower()}-vs-{teams[1].lower()}-{gameid}"
            game["url"] = f"https://www.nba.com/game/{slug}"
            self.game_urls[game_code] = game["url"]
        return self.game_urls

if __name__ == "__main__":
    nba = NBA()
    for game, url in nba.get_game_urls().items():
        print(f"Game: {game}, URL: {url}")