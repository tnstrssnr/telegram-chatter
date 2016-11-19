#!usr/bin/python3

"""
Die Klasse TelegramBot ist zuständig für die Kommunikation mit dem Telegram-Server. Ein Objekt dieser Klasse
kann verwendet werden, um Nachrichten-Objekte zu senden und zu empfangen.
Attribute:

    oauth       --  Autorisierungstoken des Bot-Accounts zur Durchführung eines HTTP-Requests
    id          --  einmalige, zur Identifikation benötigte, ID des Bots
    name        --  Name des Bots
    username    --  Username des Bots
    online      --  Boolean-Wert, der anzeigt, ob der Bot momentan läuft
"""

import json
import urllib.parse
import urllib.request
import urllib.error
import requests

from chatter.message import Nachricht
from chatter.user import User

__author__ = 'Tina Maria Stroessner'
__license__ = 'MIT'
__version__ = 'v1.0'

# statische String-Variablen zur Erzeugung der HTTP URIs
SITE = "https://api.telegram.org/bot"
GET_ME = "/GetMe"
GET_UPDATES = "/GetUpdates"
SEND_MESSAGE = "/sendmessage?"
SEND_PHOTO = "/sendPhoto"
GET_ADMINS = "/getChatAdministrators?"

# wird beim Aufruf der hole_updates()-methode gesetzt, sorgt dafür, dass keine alten Nachrichten zurückgegeben werden
offset = 0


class TelegramBot(object):

    # Konstruktor, zur Erzeugung eines TelegramBot-Objekts
    # Parameter:
    #   oauth   --  Autorisierungstoken des Bot-Accounts zur Durchführung eines HTTP-Requests
    #   Bemerkung: alle anderen Attribute werden direkt vom Telegram-Server übernommen und automatisch initialisiert
    #
    # Rückgabewert:
    #   TelegramBot-Objekt

    def __init__(self, oauth):
        self.oauth = oauth

        url = SITE + self.oauth + GET_ME
        with urllib.request.urlopen(url) as url:
            response = url.read()
        data = json.loads(response.decode('utf-8'))

        self.id = data["result"]["id"]
        self.name = data["result"]["first_name"]
        self.username = data["result"]["username"]
        self.online = False

    # Funktion get_update
    # führt ein HTTP-GET Request aus und parst die erhaltenen JSON-Daten in Nachrichten-Objekte
    #
    # Rückgabewert:
    # 	Eine Liste von Nachrichten-Objekten, die alle erhaltenen Nachrichten, seit der letzten Abfrage, enthält

    def hole_updates(self):
        global offset
        url = SITE + self.oauth + GET_UPDATES + "?offset=" + str(offset)
        with urllib.request.urlopen(url) as url:
            response = url.read()
        data = json.loads(response.decode('utf-8'))

        message_queue = []

        for res in data["result"]:
            try:
                message_queue.append(Nachricht(res["message"]))
            except KeyError:
                pass

        if not len(message_queue) == 0:
            offset = data["result"][-1]["update_id"] + 1

        return message_queue

    # Funktion gehe_online
    # setzt self.online auf 'True', ruft einmalig die Funktion hole_updates() auf und verwirft den Rückgabewert,
    # um zu verhindern, dass beim Start des Programms auf alte Nachrichten reagiert wird

    def gehe_online(self):
        self.online = True
        self.hole_updates()

    # Funktiob gehe_offline
    # setzt self.online auf 'False'
    def gehe_offline(self):
        self.online = False

    # Funktion sende_nachricht
    # sendet eine Nachricht an den spezifizierten Chat
    # Parameter:
    #
    #   text        --  der Text, der gesendet werden soll
    #   chat_id     --  ID des Chats, an den die Nachricht gesendet werden soll
    #   antwort_id  --  Nachrichten-ID der Nachricht, auf die direkt geantwortet werden soll
    #                   [optional, default-Wert ist None]
    #
    # Rückgabewert:
    #   das gesendete Nachrichten-Objekt

    def sende_nachricht(self, text, chat_id, antwort_id=None, markdown=False):
        t = urllib.parse.quote_plus(text)
        t = t.replace(".", "%2E")
        t = t.replace("-", "%2D")
        t = t.replace("_", "%5F")

        if antwort_id is not None:
            t += "&reply_to_message_id=" + str(antwort_id)

        try:
            send_url = SITE + self.oauth + SEND_MESSAGE + "chat_id=" + str(chat_id) + "&text=" + t
            if markdown:
                send_url = send_url + "&parse_mode=Markdown"
            with urllib.request.urlopen(send_url) as url:
                sent_message = url.read()
            return json.loads(sent_message.decode('utf-8'))
        except urllib.error.HTTPError:
            print("Nachricht konnte nicht gesendet werden. Es ist ein HTTPError aufgetreten.")

    # Funktion sende_bild
    # sendet eine Bild-Datei an den spezifierten Chat
    #
    # Parameter:
    #   bild    --  Pfad zu der Bild-Datei
    #   chat_id --  ID des Chats, an den das Bild gesendet werden soll
    def sende_bild(self, bild, chat_id):
        send_url = SITE + self.oauth + SEND_PHOTO
        data = {'chat_id': chat_id}
        files = {'photo': open(bild, 'rb')}
        r = requests.post(send_url, data=data, files=files)

    # Funktion gib_Admins
    # gibt eine Liste mit allen Admins desChats zurück. Bei Felher (z.B. Abfrage in einem privaten Chat) wird der Wert -1 zurückgegeben
    #
    # Parameter:
    #   chat_id --  die ID des Chats, der abgefragt werden soll
    #
    # Rückgabewert:
    #   Liste aller Administratoren des Chats (User-Objekte)
    #   -1 falls ein Fehler aufetreten ist
    def gib_Admins(self, chat_id):
        try:
            send_url = SITE + self.oauth + GET_ADMINS + "chat_id=" + chat_id
            with urllib.request.urlopen(send_url) as url:
                result = url.read()
            data = json.loads(result.decode('utf-8'))

        except:
            print("Nachricht konnte nicht gesendet werden. Es ist ein HTTPError aufgetreten.")
            return -1

        admins = []
        for admin in data["result"]:
            admins.append(User(admin["user"]))

        return admins
