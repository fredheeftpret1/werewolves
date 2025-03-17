import random
from roles import *

# Variabelen
players = []
players_names = []
roles = ["Dorpeling", "Weerwolf", "Politie", "Dokter",
         "Dorpeling", "Weerwolf", "Dorpeling", "Dokter",
         "Dorpeling", "Weerwolf", "Dorpeling", "Dokter"]
max_players = 12
min_players = 4
num_of_players = 0
players_chosen = False
players_dictionary = {}


def choosing_players():
    global num_of_players
    try:
        num_of_players = int(input(">> "))
        if num_of_players < min_players or num_of_players > max_players:
            print(f"Dit spel is voor {min_players} tot {max_players} spelers.")
            return True # Players are not chosen
        return False # If players are chosen
    except ValueError:
        print("Voer een getal in.") # Players are not chosen
        return False


class Speler:
    def __init__(self, name, role):
        self.name = name
        players_names.append(name)
        self.role = role
        print(f"Welkom bij het spel, {self.name}!")
        players_dictionary[name] = role


    def use_role(self):
        match self.role:
            case "Dorpeling":
                villager(random.randint(1, 3))
            case "Weerwolf":
                werewolves()
            case "Politie":
                police()
            case "Dokter":
                doctor()
            case _:
                print("Didn't recognize role")

    @classmethod
    def add_players(cls):
        global players_chosen
        global num_of_players
        global roles
        global players
        print("Met hoeveel wil je spelen?")
        while not choosing_players():
            pass
        roles = roles[:num_of_players]
        random.shuffle(roles)
        for i in range(num_of_players):
            player_chosen = False
            while not player_chosen:
                print("Wat is je naam?")
                name = input(">>")
                if not bestaat_speler(name):
                    players.append(Speler(name, roles[i]))
                    player_chosen = True
                else:
                    print(f"Speler {name} bestaat al.")


def bestaat_speler(name):
    return any(obj.name == name for obj in players)


def speler_naam_is_rol(name, role):
    return any(obj.name == name and obj.role == role for obj in players)


if __name__ == "__main__":
    Speler.add_players()
