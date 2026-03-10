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
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8">
        <title>Partits destacats NBA</title>
      </head>
      <body style="margin:0;padding:0;background-color:#f2f2f2;font-family:Arial, Helvetica, sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="padding:20px;">
          <tr>
            <td align="center">
              <!-- CONTENEDOR -->
              <table width="600" cellpadding="0" cellspacing="0" border="0" style="background:#ffffff;border-radius:8px;overflow:hidden;">
                <!-- HEADER -->
                <tr>
                  <td align="center" style="background:#1d428a;color:white;padding:20px;">
                    <h1 style="margin:0;font-size:22px;">🏀 Partits destacats NBA</h1>
                  </td>
                </tr>
                <!-- INTRO -->
                <tr>
                  <td style="padding:20px;font-size:14px;color:#333;"> De tots els partits jugats aquesta matinada, destaquen els següents: </td>
                </tr>
                <!-- LLISTA PARTITS -->
                <tr>
                  <td style="padding:0 20px 20px 20px;">
                    <table width="100%" cellpadding="0" cellspacing="0" border="0">
                        {list_items}
                    </table>
                  </td>
                </tr>
                <!-- FOOTER -->
                <tr>
                  <td align="center" style="background:#fafafa;padding:15px;font-size:11px;color:#888;"> Notificació automàtica de partits interessants NBA </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </body>
    </html>
"""

    list_items = []
    for game_id in games:
        game_html = f"""
                  <!-- PARTIT -->
                  <tr>
                    <td style="border:1px solid #e5e5e5;border-radius:6px;padding:14px;">
                      <table width="100%" cellpadding="0" cellspacing="0" border="0">
                        <tr>
                          <td style="font-size:16px;font-weight:bold;color:#333;">🏀 {' vs '.join(nba.get_teams_from_game_code(game_id))} </td>
                          <td align="right">
                            <a href=\"{games_urls.get(game_id, '#')}\" style="background:#1d428a;color:white;text-decoration:none;padding:8px 14px;border-radius:4px;font-size:13px;font-weight:bold;"> Veure partit </a>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
        """
        list_items.append(game_html)

    joiner = """
                  <tr>
                    <td height="10"></td>
                  </tr>
    """
    list_items = joiner.(list_items)
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
