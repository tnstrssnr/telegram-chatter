#!/usr/bin/python3

"""
Repräsentiert ein Chat-Objekt.
Attribute:

    id        --      einmalige, zur Identifikation benötigte, Chat-ID
    typ       --      Art des Chats, entweder "private", "group", "supergroup" oder "channel"
    titel     --      Titel von Gruppen, Suppergruppen und Kanälen, 'None' falls kein Titel vorhanden
"""

__author__ = 'Tina Maria Stroessner'
__license__ = 'MIT'
__version__ = 'v1.0'


class Chat(object):

    def __init__(self, chat):
        self.id = chat["id"]
        self.typ = chat["type"]

        try:
            self.titel = chat["title"]
        except KeyError:
            self.titel = None
