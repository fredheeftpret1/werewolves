from player_functionality import Speler, players, players_dictionary, players_names, bestaat_speler
from roles import *
from collections import Counter
import save

night_number = 0
game_has_ended = False
who_voted_on_who = {}


def check_end():
    global game_has_ended
    werewolves_alive = any(obj.role == "Weerwolf" for obj in players)
    villagers_alive = any(obj.role != "Weerwolf" for obj in players)
    if werewolves_alive and villagers_alive:
        game_has_ended = False
        return "Er zijn nog weerwolven en dorpsbewoners over."
    elif werewolves_alive and not villagers_alive:
        game_has_ended = True
        return "Er zijn alleen nog weerwolven over."
    elif not werewolves_alive and villagers_alive:
        game_has_ended = True
        return "Er zijn alleen nog dorpsbewoners over."


def night():
    global night_number, players_names
    night_number += 1
    already_been = []
    sleep(2)
    print("\n" * 100)
    while len(players_names) != len(already_been):
        active_player = input("NACHT: Wie is dit?")
        if active_player in already_been:
            print("Jij bent al geweest.")
            continue
        if not bestaat_speler(active_player):
            print("Die speler bestaat niet of is al dood.")
            continue
        for player in players:
            if player.name == active_player:
                player.use_role()
                already_been.append(player.name)
        sleep(2)
        print("\n" * 100)
    dead_person = who_is_dead()
    if dead_person is None:
        print("Niemand is dood!")
    else:
        print(f"Ik vind het niet leuk te zeggen, maar {dead_person} is dood.")
    for player in players:
        if player.name == dead_person:
            del players[players.index(player)]
            del players_names[players_names.index(player.name)]


def vote():
    already_been = []
    voted_persons = []
    while len(already_been) != len(players_names):
        voted = False
        active_player = input("STEMMEN: Wie is dit?")
        if active_player in already_been:
            print("Jij bent al geweest.")
            continue
        if not bestaat_speler(active_player):
            print("Die speler bestaat niet of is al dood.")
            continue
        while not voted:
            print("Wie denk jij dat de weerwolf is?")
            vote_choice = input(">>")
            if not bestaat_speler(vote_choice):
                print("Die speler bestaat niet of is al dood.")
                continue
            else:
                voted_persons.append(vote_choice)
                voted = True
                who_voted_on_who[active_player] = vote_choice
        already_been.append(active_player)
        sleep(2)
        print("\n" * 100)
    who_is_outvoted(voted_persons)
    for player, votes in who_voted_on_who.items():
        print(f"{player} voted on {votes}.")


def who_is_outvoted(voted_persons):
    counter = Counter(voted_persons)
    max_count = max(counter.values())
    for person in voted_persons:
        if counter[person] != max_count:
            del voted_persons[voted_persons.index(person)]
    if len(voted_persons) == 1:
        outvoted_person = voted_persons[0]
    else:
        outvoted_person = None
    if outvoted_person:
        print("Jullie hebben het meest gestemd op:", outvoted_person)
        del players[players_names.index(outvoted_person)]
        del players_names[players_names.index(outvoted_person)]
    else:
        print("Er was gelijkspel, en niemand gaat dood!😊")


def intro():
    with open("intro.txt", "r") as file:
        intro = file.read()
    print(intro)
    input("Zijn jullie klaar om te spelen?")


if __name__ == "__main__":
    intro()
    Speler.add_players()
    while not game_has_ended:
        night()
        vote()
        print(winmanier := check_end())
    for player in players_dictionary:
        print(f"{player} was een {players_dictionary[player]}")
    save.slaag_op("opslaag_tekst.txt",
                  players_names,
                  night_number,
                  winmanier, # NOQA
                  players_dictionary)
