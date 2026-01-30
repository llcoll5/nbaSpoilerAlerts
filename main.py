from dotenv import load_dotenv
import os
import time

from NBA import NBA
from Wikihoops import Wikihoops
from Sender import Sender

if __name__ == "__main__":
    load_dotenv()
    username = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVERS")

    sender = Sender(username, password)
    nba = NBA()
    wikihoops = Wikihoops()

    worth_watching = []
    ratings = wikihoops.get_game_ratings()
    games_urls = nba.get_game_urls()
    for game_id, rating in ratings.items():
        if rating >= 8:
            worth_watching.append(game_id)
            print(f"Game ID: {game_id}, Rating: {rating}")
            print(f"URL: {games_urls.get(game_id, 'URL not found')}")

    if len(worth_watching) > 0:
        html = """
        <html>
            <body>
                <h2>De tots els partits jugats aquesta matinada, destaquen els següents:</h2>
                <ul>
                    {list_items}
                </ul>
            </body>
        </html>
        """

        list_items = ""
        for game_id in worth_watching:
            list_items += f"<li><a href=\"{games_urls.get(game_id, '#')}\">Partit {' VS '.join(nba.get_teams_from_game_code(game_id))}</a></li>"

        html = html.format(list_items=list_items)
        subject = f"{len(worth_watching)} Bons partits NBA d'aquesta matinada - {time.strftime('%d/%m/%Y')}"

        sender.send_email(subject, html, receiver)

        print(f"HTML enviat: {html}")
