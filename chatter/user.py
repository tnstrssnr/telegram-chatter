#!usr/bin/python3

"""
Repräsentiert ein User-Objekt
Attribute:

    id          --  einmalige, zur Identifikation benötigte, ID
    vorname     --  Vorname des Users
    nachname    --  Nachname des Users, 'None' falls nicht vorhanden
    username    --  Username des Users, 'None' falls nicht vorhanden
"""

__author__ = 'Tina Maria Stroessner'
__license__ = 'MIT'
__version__ = 'v1.0'


class User(object):
    # represents a user
    # attributes
    #   id      --  unique identifier for the user
    #   vorname  --  first name of the user
    #   nachname   --  last name of the user

    def __init__(self, user):
        self.id = user["id"]
        self.vorname = user["first_name"]
        try:
            self.nachname = user["last_name"]
        except KeyError:
            self.nachname = None
        try:
            self.username = user["username"]
        except KeyError:
            self.username = None
