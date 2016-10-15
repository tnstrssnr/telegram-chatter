#!usr/bin/python3

"""
Repräsentiert ein Nachrichten-Objekt.
Attribute:

    id          --  einmalige, zur Identifikation benötigte, Nachrichten-ID
    sender      --  der Sender der Nachricht (User-Objekt)
    datum       --  Datum/Uhrzeit an dem die NAchricht gesendet wurde (UNIX-Zeitformat)
    chat        --  Chat, an den die Nachricht gesandt worden ist (Chat-Objekt)
    antwort     --  Originalnachricht, falls die Nachricht eine Antwort war, sonst 'None'
    inhalt      --  Der Inhalt der Nachricht
"""

from chatter.chat import Chat
from chatter.user import User

__author__ = 'Tina Maria Stroessner'
__license__ = 'MIT'
__version__ = 'v1.0'


class Nachricht(object):

    def __init__(self, msg):
        self.id = msg["message_id"]
        self.sender = User(msg["from"])
        self.datum = msg["date"]
        self.chat = Chat(msg["chat"])
        try:
            self.antwort = Nachricht(msg["reply_to_message"])
        except KeyError:
            self.antwort = None

        try:
            self.inhalt = msg["text"].strip().lower()
        except KeyError:
            self.inhalt = None
