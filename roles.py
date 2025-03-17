from collections import Counter
from time import sleep
import player_functionality
import handige_functies

werewolves_choices = []
saved_by_doctor = []

def villager(text_number):
    if text_number == 1:
        handige_functies.story_print_vraag_bestand("Dorpelingen_tekst", "-----------------", 1)
    elif text_number == 2:
        choice = handige_functies.story_print_vraag_bestand("Dorpelingen_tekst", "-----------------", 2)
        if choice == 1:
            handige_functies.story_print_bestand("Dorpelingen_tekst", "-----------------", 3)
        elif choice == 2:
            handige_functies.story_print_bestand("Dorpelingen_tekst", "-----------------", 4)
        else:
            handige_functies.story_print("Je wachtte te lang\n Maar toen...\n")
        handige_functies.story_print_bestand("Dorpelingen_tekst", "-----------------", 5)
    else:
        choice = handige_functies.story_print_vraag_bestand("Dorpelingen_tekst", "-----------------", 6)
        if choice == 1:
            choice2 = handige_functies.story_print_vraag_bestand("Dorpelingen_tekst", "-----------------", 7)
            if choice2 == "1":
                print("Je pakt een emmer water en je helpt mee het vuur te blussen.")
            elif choice2 == "2":
                print("Terwijl de anderen het vuur blussen, kijk jij rond je. En dan zie je voetsporen.")
            else:
                print("Je denkt te lang na, en het vuur wordt steeds groter")
        elif choice == 2:
            handige_functies.story_print_bestand("Dorpelingen_tekst", "-----------------", 8)
        else:
            print("Je dacht te lang na, en miste je kans te helpen...")
        sleep(2)
        print("Dan wordt je wakker, en besef je dat het een droom was.")


def werewolves():
    global werewolves_choices
    print("Hallo weerwolf!")
    sleep(2)
    for player in player_functionality.players:
        if player.role == "Weerwolf":
            print(f"{player.name} is een weerwolf.")
    sleep(2)
    print("Wie wil jij opeten?")
    dead_chosen = False
    while not dead_chosen:
        choice = input(">>")
        if player_functionality.speler_naam_is_rol(choice, "Weerwolf"):
            werewolves_choices.append(choice)
            print("Dat is ook een weerwolf.")
        elif player_functionality.bestaat_speler(choice):
            dead_chosen = True
            werewolves_choices.append(choice)
        else:
            print("Die speler bestaat niet, of is al dood.")


def police():
    print("Hallo politie!")
    sleep(1)
    print("Jij mag van 1 persoon weten of die een weerwolf is.")
    chosen = False
    while not chosen:
        choice = input(">>")
        if player_functionality.bestaat_speler(choice):
            if player_functionality.speler_naam_is_rol(choice, "Weerwolf"):
                print("Dat is een weerwolf.")
            else:
                print("Dat is geen weerwolf.")
            chosen = True
        else:
            print("Die speler bestaat niet, of is al dood.")


def doctor():
    global saved_by_doctor
    print("Hallo dokter!")
    sleep(1)
    print("Jij mag een iemand kiezen, en deze kan niet worden gedood door een weerwolf deze ronde.")
    chosen = False
    while not chosen:
        choice = input(">>")
        if player_functionality.bestaat_speler(choice):
            saved_by_doctor.append(choice)
            chosen = True
        elif player_functionality.speler_naam_is_rol(choice, "Dokter"):
            print("Dat is ook een dokter")
        else:
            print("Die speler bestaat niet, of is al dood.")


def who_is_dead():
    save_saved_person()
    # Last, see who's dead
    if not werewolves_choices: # If nobody is dead
        return
    counter = Counter(werewolves_choices) # Count the votes
    max_count = max(counter.values()) # Max values
    # Who is most chosen?
    for choice in counter.keys():
        if counter[choice] != max_count:
            del werewolves_choices[werewolves_choices.index(choice)]
            del counter[choice]
    if len(werewolves_choices) == 1:
        return werewolves_choices[0]
    else:
        return werewolves_choices[len(werewolves_choices) - 1]


def save_saved_person():
    global saved_by_doctor
    # First, check who's saved by doctor
    if len(saved_by_doctor) == 1:
        saved_by_doctor = saved_by_doctor[0]
    else:
        saved_by_doctor = saved_by_doctor[len(saved_by_doctor) - 1]
    # Then, delete that person from the choices of the werewolves
    for i in range(len(werewolves_choices)):
        if werewolves_choices[i] == saved_by_doctor:
            del werewolves_choices[i]


if __name__ == "__main__":
    saved_by_doctor = ["Hello"]
    werewolves_choices = ["Jan", "Jan", "Pieter", "Pieter"]
    print(who_is_dead())