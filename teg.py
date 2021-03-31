import random


def intput(prompt, exception=None, errormsg="Invalid input."):
    print(prompt, end=" ")
    while True:
        userinput = input()
        if exception is not None and userinput == exception:
            return userinput.lower()
        else:
            try:
                userinput = int(userinput)
            except ValueError:
                print(errormsg)
            else:
                return userinput


class Card:
    def __init__(self, length, pts, cult, stonks, text="-", name=""):
        self.length = length
        self.points = pts
        self.culture = cult
        self.stonks = stonks
        self.text = text
        self.name = name
        self.rockets = [[] for _ in range(int(length) + 1)]  # +Orbit
        self.pos = 0

    def show(self):
        if self.culture:
            cult = " Culture, "
        else:
            cult = " Energy, "

        if self.stonks:
            stks = " Economy, "
        else:
            stks = " Diplomacy, "
        print(self.rockets)
        return print(self.length, " Length, ", self.points, " Points, ", cult, stks, self.text, ", ", self.name, sep="")


class Deck:
    def __init__(self):
        self.cards = []
        self.shown = []
        self.deck()
        self.shuffle()
        for i in range(4):
            self.draw(i)

    def deck(self):
        self.cards = []
        file = open("planetz.txt", "r")

        for line in file:
            item = line.split(";")
            name = item[0]
            stonks = 1 if item[1] == "E" else 0
            length = int(item[2]) + 1
            cult = 1 if item[3] == "C" else 0
            pts = item[4]
            text = item[5].replace("\n", "")
            self.cards.append(Card(length, pts, cult, stonks, text, name))

        file.close()
        # self.show()

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def draw(self, pindex):
        card = self.cards.pop()
        self.shown.append(card)
        card.pos = pindex

    def show_cards(self):
        for card in self.shown:
            print(card.pos, ": ",
                  card.name, "" if (len(card.name) > 7) else "\t", "\t| ",
                  "Culture" if card.culture else "Energy", "\t| ",
                  "Economy" if card.stonks else "Diplomacy", "\t| ",
                  card.points, " points" if int(card.points) > 1 else " point", sep="")
            print(">", card.text)
            print(*card.rockets)
            print('='*45)

    def show(self):
        for card in self.cards:
            card.show_stats()


def show_dice(dice):
    for dienum in range(len(dice)):
        print(dienum, ": ", dice[dienum], sep="")


class Player:
    def __init__(self):
        self.ship = ["Galaxy", "Galaxy", "Galaxy"]
        self.name = "Player"
        self.level = 1
        self.cult = 10
        self.energy = 2
        self.pts = 0
        self.ships = 2
        self.die_count = 4
        self.in_galaxy = 2
        self.dice = [" "] * self.die_count
        self.rerolled = 0

    def show_stats(self):
        print("Level:", self.level, "| Ships:", self.ships, "| Dice:", self.die_count, "| Energy:", self.energy,
              "| Culture:", self.cult, "| Points:", self.pts)

    def show_rockets(self):
        for i in range(len(self.ship)):
            print(i, ": ", self.ship[i], sep="")

    def energy_add(self, source):
        self.energy += 1
        print("\t+1 Energy from", source + ".")

    def energy_sub(self):
        pass

    def cult_add(self, source):
        self.cult += 1
        print("\t+1 Culture from", source + ".")

    def cult_sub(self):
        pass

    def die_add(self):
        pass

    def ship_add(self):
        pass

    def pts_add(self):
        pass

    def ship_move(self, rocket, planet):
        planet_name = deck.shown[planet].name
        if planet_name in self.ship[rocket]:
            print("You cannot fly between the orbit and the surface.")
            return False
        if any(self.name in slot for slot in deck.shown[planet].rockets[1:]):
            if self.name in deck.shown[planet].rockets[0]:
                print("You have already occupied this planet.")
                return False
            else:
                pos = 0
        else:
            if self.name in deck.shown[planet].rockets[0]:
                pos = 1
            else:
                orbit = input("Do you want to fly to the [O]rbit or the [S]urface? ")
                orbit.lower()
                pos = 0 if orbit == "s" else 1

        self.ship_remove(rocket)

        # TODO: Add prompt to activate effect upon landing on the surface

        deck.shown[planet].rockets[pos].append(self.name)
        self.ship[rocket] = planet_name + " (" + ("S" if pos == 0 else "O") + ")"
        deck.show_cards()
        print("Flown to the", planet_name, "surface." if pos == 0 else "orbit.")
        return True

    def ship_remove(self, rocket):
        # Horrible, but it works
        if self.ship[rocket] != "Galaxy":
            for i in range(len(deck.shown)):
                if deck.shown[i].name in self.ship[rocket]:
                    for j in range(len(deck.shown[i].rockets)):
                        for k in range(len(deck.shown[i].rockets[j])):
                            try:
                                deck.shown[i].rockets[0 if self.ship[rocket].split(' ')[1] == '(S)' else 1:][k] \
                                    .remove(self.name)
                            except ValueError:
                                pass

    def ship_return(self, rocket, do_print=True):
        if self.ship[rocket] == "Galaxy":
            print("The rocket is already in your Galaxy.")
            return False
        origin = self.ship[rocket].split(' ')[0]
        self.ship_remove(rocket)
        self.ship[rocket] = "Galaxy"
        if do_print:
            print("Returned to your Galaxy from " + origin + ".", sep="")
        return True

    def levelup(self, cultpay):
        self.level += 1
        print("[!] Level up!", sep="", end=" ")
        if self.level % 2 == 0:
            self.die_count += 1
            print("Gained 1 die.", end=" ")
        else:
            self.ships += 1
            print("Gained 1 ship.", end=" ")
        if cultpay:
            self.cult -= self.level
            print("Spent", self.level, "Culture.")
        else:
            self.energy -= self.level
            print("Spent", self.level, "Energy.")
        self.show_stats()

    def dice_roll(self):
        for i in range(self.die_count):
            throw = random.randint(0, 5)
            self.dice[i] = action.get(throw)
        print("You have thrown:")
        show_dice(self.dice)

    def die_reroll(self):
        reroll = 1
        if self.rerolled == 0:
            self.rerolled = 1
            while True:
                reroll = intput("How many dice do you wish to reroll?")
                if reroll > self.die_count:
                    print("You don't have that many dice.")
                elif reroll < 1:
                    print("Cannot reroll less than 1 die.")
                else:
                    break
        if reroll == self.die_count:
            self.dice = ["rerolled"] * self.die_count
        elif reroll > 0:
            for i in range(reroll):
                numstr = (" " + ordinal.get(i) + " ") if reroll > 1 else " "
                while True:
                    nroll = intput("Select the number of the" + numstr + "die you wish to reroll:")
                    if nroll > len(self.dice) - 1 or nroll < 0:
                        print("Such die does not exist!")
                    elif self.dice[nroll] == "rerolled":
                        print("You have already chosen this die!")
                    else:
                        self.dice[nroll] = "rerolled"
                        break
        for i in range(self.die_count):
            if self.dice[i] == "rerolled":
                throw = random.randint(0, 5)
                self.dice[i] = action.get(throw)
        self.energy -= 1
        print("You have thrown:")
        show_dice(self.dice)
        self.show_stats()

    def die_convert(self):
        show_dice(self.dice)
        for i in range(3):
            while True:
                discard = intput("Select the number of the " + ordinal.get(i) + " die you wish to convert:")
                if discard > len(self.dice) - 1 or discard < 0:
                    print("Such die does not exist!")
                elif self.dice[discard] == "converted":
                    print("You have already converted this die!")
                else:
                    self.dice[discard] = "converted"
                    break
        while True:
            for i in range(len(action)):
                print(i, ": ", action[i], sep="")
            while True:
                newdie = intput("Which action do you want to set?")
                if newdie > len(action) or newdie < 0:
                    print("Out of range!")
                else:
                    break
            for i in range(self.die_count - 1, -1, -1):
                if self.dice[i] == 'converted':
                    del self.dice[i]
            self.dice.append(action[newdie])
            break
        show_dice(p.dice)

    def die_use(self):
        show_dice(self.dice)
        use = intput("Which die do you want to use?")

        if use >= len(self.dice):
            print("Invalid input.")

        else:
            #
            # Colonization
            #
            if self.dice[use] == action[0]:
                colony = input("Do you want to [A]ctivate one of your cards or [U]pgrade your empire? ").lower()
                if colony == 'u':
                    if self.cult > self.level:
                        if self.energy > self.level:
                            cultpay = input("Do you want to upgrade using [C]ulture or [E]nergy? ").lower()
                            self.levelup(1 if cultpay == 'c' else 0)
                        else:
                            self.levelup(1)
                    elif self.energy > self.level:
                        self.levelup(0)
                    else:
                        print("jj")
                # Colonization

            #
            # Rocket
            #
            if self.dice[use] == action[1]:
                while True:
                    self.show_rockets()
                    rocket_id = intput("Which rocket do you want to use?")
                    if rocket_id < len(self.ship):
                        if self.ship[rocket_id] is not None:
                            deck.show_cards()
                            print('[G]alaxy:', end=" ")
                            for rocket in self.ship:
                                if rocket == "Galaxy":
                                    print(self.name, end=" ")
                            print()
                            moved = False
                            planet = intput("Which planet do you want to fly to?", exception="g")
                            if planet == "g":
                                moved = self.ship_return(rocket_id)
                            elif planet < len(deck.shown):
                                moved = self.ship_move(rocket_id, planet)
                            if moved:
                                break
                        else:
                            print("This ship is not available.")
                    else:
                        print("You do not have that ship.")

            #
            # Energy && Culture
            #
            if self.dice[use] == action[2] or self.dice[use] == action[3]:
                is_energy = True if self.dice[use] == "Energy" else False
                for shiploc in self.ship:
                    for galaxy in deck.shown:
                        if galaxy.name in shiploc:
                            if is_energy and galaxy.culture == 0:
                                self.energy_add(galaxy.name)
                            elif not is_energy and galaxy.culture == 1:
                                self.cult_add(galaxy.name)
                    if is_energy and shiploc == "Galaxy":
                        self.energy_add("your Galaxy")
                self.show_stats()

            #
            # Economy && Diplomacy
            #
            if self.dice[use] == action[4] or self.dice[use] == action[5]:  # choose one galaxy lol
                is_economy = True if self.dice[use] == action[4] else False
                for shiploc in self.ship:
                    for galaxy in deck.shown:
                        # print(galaxy.name, shiploc, ": ", shiploc == galaxy.name and e==1 and
                        # galaxy.stonks==1)
                        if galaxy.name in shiploc and is_economy and galaxy.stonks:
                            yeah = 0
                            for loc in galaxy.rockets:
                                if loc != 0 and "Player" in loc:
                                    loc.remove("Player")
                                    print("removed")
                                    yeah = 1
                                    print("y: ", yeah)
                                if yeah:
                                    loc.append("Player")
                                    print("appended")
                                    yeah = 0
                                    print("y: ", yeah)
                                print("Player" in loc)
                        # elif(not e and shiploc == galaxy.name and galaxy.cult == 0): self.cult+=1
                    # if(shiploc == "Galaxy"): self.energy+=1
                self.show_stats()
            del self.dice[use]

    def die_throw(self):
        self.die_reroll()
        self.die_convert()
        self.die_use()

    def start_turn(self):
        self.dice_roll()

    def end_turn(self):
        self.dice = []


action = {
    0: "Colonization",
    1: "Rocket",
    2: "Energy",
    3: "Culture",
    4: "Economy",
    5: "Diplomacy"
}

ordinal = {
    0: "first",
    1: "second",
    2: "third",
    3: "fourth"
}

if __name__ == "__main__":
    p = Player()
    deck = Deck()
    converted = False

    p.show_stats()
    p.dice_roll()
    while True:  # So far there is only one player, so deal with this
        while True:
            move = input("S — Stats; P — Planets; D — Dice; R – Rockets; "
                         "RR — Reroll dice; C — Convert dice; U — Use dice; E — End turn\n")
            move = move.lower()
            if move == 's':
                p.show_stats()
            elif move == 'p':
                deck.show_cards()
            elif move == 'd':
                show_dice(p.dice)
            elif move == 'r':
                p.show_rockets()
            elif move == 'rr':
                p.die_reroll()
            elif move == 'c':
                if not converted:
                    p.die_convert()
                    converted = True
                else:
                    print("You have already converted this turn.")
            elif move == 'u':
                p.die_use()
            elif move == 'e':
                p.end_turn()
                break
            else:
                print("Invalid input.")
