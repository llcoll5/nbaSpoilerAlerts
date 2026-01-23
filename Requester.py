import requests

class RequestGetter:
    def __init__(self, url, headers=None):
        self.url = url
        self.headers = headers
        self.content = None
        self.send_request()

    def send_request(self):
        r = requests.get(self.url, headers=self.headers)
        try:
            r.raise_for_status()
            self.content = r.json()
        except requests.RequestException as e:
            print(f"Error: {e}")
            return {"error": str(e)}

    def get_content(self):
        return self.content


if __name__ == "__main__":
    url = "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"

    headers = {
        "Origin": "https://www.nba.com",
        "Referer": "https://www.nba.com/",
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }


    requester = RequesterGetter(url, headers)
    response = requester.get_content()
    print(response)