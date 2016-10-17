#!usr/bin/python3

"""
Eine Unterklasse von TelegramBot, die die Funktionalität um eine einfache Spracherkennung erweitert.
Objekte dieser Klasse können auf verschiedene Wörter/Sätze  reagieren und senden entsprechende Antworten an den Chat
"""

import random
import time
from datetime import datetime

from chatter.telegramBot import TelegramBot
from beispiel_implementation.texte import BEGRUESSUNG, VERABSCHIEDUNG, IDENTITAET, GEFUEHLS_ZUSTAND
from beispiel_implementation import config

__author__ = 'Tina Maria Stroessner'
__license__ = 'MIT'
__version__ = 'v1.0'


class DojoBot(TelegramBot):

    # Liste speichert mehrere Antworten, die aufeinanderfolgend gesendet werden sollen
    antworten = []

    # Funktion aktivieren
    # enthält den main-loop des Bots. Die Methode setzt zunächst das online-Attribut. Danach wird alle 5sek
    # nach Updates gefragt. Auf jede erhaltene Nachricht wird konsekutiv die Methode reagiere() aufgerufen.

    def aktivieren(self):
        self.gehe_online()
        print("Bot ist aktiviert")

        while self.online:
            nachrichten = self.hole_updates()

            for nachricht in nachrichten:
                self.reagiere(nachricht)

            time.sleep(5)

        print("Bot wird deaktiviert")

    # Funktion reagiere()
    # Funktion steuert, wie der Bot auf eine Nachricht reagiert.
    # Parameter:
    #   nachricht   --  Nachricht-Objekt, die NAchricht auf die reagiert werden soll

    def reagiere(self, nachricht):
        name = nachricht.sender.vorname
        chat = nachricht.chat.id

        begruessung_benutzt = [wort for wort in nachricht.inhalt.split() if wort in BEGRUESSUNG]
        verabschiedung_benutzt = [wort for wort in nachricht.inhalt.split() if wort in VERABSCHIEDUNG]

        if not len(DojoBot.antworten) == 0 and chat == DojoBot.antworten[0][1]:

            if DojoBot.antworten[0][0] == " wer?":
                DojoBot.antworten[0][0] = nachricht.inhalt + " wer?"

            self.sende_nachricht(DojoBot.antworten[0][0], DojoBot.antworten[0][1])
            del DojoBot.antworten[0]

        elif len(begruessung_benutzt) > 0:
            antwort = random.choice(BEGRUESSUNG) + ", " + name
            self.sende_nachricht(antwort, chat)
                
        elif len(verabschiedung_benutzt) > 0:
            antwort = random.choice(VERABSCHIEDUNG) + ", " + name
            self.sende_nachricht(antwort, chat)
            self.gehe_offline()

        elif nachricht.inhalt == "klopf klopf":
            self.sende_nachricht("Wer ist da?", chat)
            DojoBot.antworten.append([" wer?", chat])
            DojoBot.antworten.append(["Hahaha😂", chat])

        elif nachricht.inhalt in IDENTITAET:
            self.sende_nachricht("Ich heiße " + self.name + ". Ich bin ein Bot. Hilf mir dabei neue Sachen zu lernen.",
                                 chat)

        elif "uhr" in nachricht.inhalt:
            self.sende_nachricht("Es ist " + str(datetime.now().strftime("%H:%M") + " Uhr"), chat)

        elif nachricht.inhalt == "/start":
            self.sende_nachricht("Ich bin ein Bot. Chatte mit mir!", chat)

        # # # # # # # # # # # # # # # # # # # #
        # Schreibe hier deinen Code, um dem Bot noch mehr Wörter beizubringen

        elif nachricht.inhalt == "wie geht es dir?":
            self.sende_nachricht(random.choice(GEFUEHLS_ZUSTAND), chat)

        elif "warum" in nachricht.inhalt:
            self.sende_nachricht("Darum", chat)

        # # # # # # # # # # # # # # # # # # # #

        else:
            self.sende_nachricht("Du nuschelst", chat)

boty = DojoBot(config.OAUTH)
boty.aktivieren()
