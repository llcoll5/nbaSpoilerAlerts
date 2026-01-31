from dotenv import load_dotenv
import os
import time

from NBA import NBA
from Wikihoops import Wikihoops
from Sender import Sender

def receiver_list(receivers_str):
    return [email.strip() for email in receivers_str.split(",")]

def send_email_games(sender, games, games_urls, receiver, nba):
    subject = f"{len(games)} Bons partits NBA d'aquesta matinada - {time.strftime('%d/%m/%Y')}"
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
    for game_id in games:
        list_items += f"<li><a href=\"{games_urls.get(game_id, '#')}\">Partit {' VS '.join(nba.get_teams_from_game_code(game_id))}</a></li>"

    html = html.format(list_items=list_items)
    try:
        sender.send_email(subject, html, receiver)
    except Exception as e:
        print(f"Error enviant l'email a {receiver}: {e}")

def main():
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
        for receiver in receiver_list(receivers):
            send_email_games(sender, worth_watching, games_urls, receiver, nba)

if __name__ == "__main__":
    load_dotenv()
    username = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receivers = os.getenv("EMAIL_RECEIVERS")

    main()
