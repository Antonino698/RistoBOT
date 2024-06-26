"""
add runtime command
"""
import json
from typing import Final
import requests
from telegram.ext import Application
from src.lib.config import BOT_CONFIG

TOKEN: Final = BOT_CONFIG['__TOKEN']

URL = "https://api.telegram.org/bot"+TOKEN+"/setMyCommands?commands="+str(json.dumps([
        {"command":"start","description":"avvia il bot"},
        {"command":"prenota","description":"prenota un tavolo"},
        {"command":"le_mie_prenotazioni","description":"visualizza/disdici prenotazione"},
        {"command":"menu","description":"visualizza il menu"},
        {"command":"eventi","description":"visualizza gli special nights events"},
        {"command":"info","description":"visualizza le informazioni del ristorante"}
    ]))

req = requests.get(URL, timeout=30)

async def add_commands(app: Application) -> None:
    """
    add runtime command
    """
    cmd = [
        ("start","avvia il bot"),
        ("prenota","prenota un tavolo"),
        ("le_mie_prenotazioni", "visualizza/disdici prenotazione"),
        ("menu","visualizza il menu"),
        ("eventi", "visualizza gli special nights events"),
        ("info", "visualizza le informazioni del ristorante")
        ]
    return cmd, app
