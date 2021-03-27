import random


def intput(prompt, errormsg="Invalid input."):
    print(prompt + " ")
    while True:
        userinput = input()
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
        self.rockets = [["Player"] for _ in range(int(length) + 1)]  # +Orbit
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

    def draw(self, index):
        card = self.cards.pop()
        self.shown.append(card)
        card.pos = index

    def show_cards(self):
        for card in self.shown:
            print("=== Position:\t", card.pos)
            print("=== Name:\t\t", card.name)
            print("=== Resource:\t", "Culture" if card.culture else "Energy")
            print("=== Track:\t\t", "Economy" if card.stonks else "Diplomacy")
            print("=== Points:\t\t", card.points)
            print(card.text)
            print(*card.rockets)
            print()

    def show(self):
        for card in self.cards:
            card.show()


class Player:
    ship = ["Drewkaiden", "Jakks", None, None]

    def __init__(self):
        self.level = 1
        self.cult = 10
        self.energy = 2
        self.pts = 0
        self.ships = 2
        self.dice = 4

    def show(self):
        print("Level:", self.level, "Ships:", self.ships, "Dice:", self.dice, "Energy:", self.energy,
              "Culture:", self.cult, "Points:", self.pts)

    def levelup(self, cultpay):
        if self.level % 2:
            self.dice += 1
        else:
            self.ships += 1
        self.level += 1
        if cultpay:
            self.cult -= self.level
        else:
            self.energy -= self.level
        self.show()

    def dice_throw(self):
        rerolled = False
        action = {
            1: "Colonization",
            2: "Rocket",
            3: "Energy",
            4: "Culture",
            5: "Economy",
            6: "Diplomacy"
        }
        actions = []
        for i in action:
            actions.append(action.get(i))

        def show_dice():
            for dienum in range(len(dice)):
                print(dienum, ": ", dice[dienum], sep="")

        dice = [] * self.dice
        while True:
            if rerolled:
                for ice in range(len(dice)):
                    if dice[ice] == "rerolled":
                        throw = random.randint(1, 6)
                        dice[ice] = action.get(throw)
            else:
                for die in range(self.dice):
                    throw = random.randint(1, 6)
                    dice.append(action.get(throw))

            print("You have thrown:")
            show_dice()

            if rerolled:
                break
            else:
                while True:
                    reroll = intput("How many do you wish to reroll?")
                    if reroll > self.dice:
                        print("You don't have that many dice!")
                    elif reroll < 0:
                        print("Cannot reroll less than 0 dice!")
                    else:
                        break
                if reroll == self.dice:
                    pass
                elif reroll > 0:
                    for i in range(reroll):
                        while True:
                            nroll = intput("Which die do you wish to reroll?")
                            if nroll > len(dice) - 1 or nroll < 0:
                                print("Such die does not exist!")
                            elif dice[nroll] == "rerolled":
                                print("You have already rerolled this die!")
                            else:
                                dice[nroll] = "rerolled"
                                break
                elif reroll == 0:
                    break
                rerolled = True

        convert = input("Do you wish to use the convertor? (two dice to set one)\n")
        if convert:
            show_dice()
            for inst in range(1, 4):
                num = {
                    1: "first",
                    2: "second",
                    3: "third"
                }
                while True:
                    discard = intput("Select the number of the " + num.get(inst) + " die you wish to convert: ")
                    if discard > len(dice) - 1 or discard < 0:
                        print("Such die does not exist!")
                    elif dice[discard] == "converted":
                        print("You have already converted this die!")
                    else:
                        dice[discard] = "converted"
                        break
            while True:
                print(dice)
                newdie = input("Which action would you want to set? ")
                if newdie in actions:
                    for i in range(self.dice - 1, -1, -1):
                        if dice[i] == 'converted':
                            del dice[i]
                    dice.append(newdie)
                    break
        while True:
            show_dice()
            use = intput("Which die do you want to use? ")

            if use >= len(dice):
                print("Invalid input.")

            else:
                if dice[use] == "Colonization":
                    colony = input(
                        "Do you want to activate one of your cards [A] or upgrade your empire? [U]\n").lower()
                    if colony == 'u':
                        if self.cult > self.level:
                            if self.energy > self.level:
                                cultpay = input("Do you want to upgrade using Culture [C] or Energy [E]\n?").lower()
                                self.levelup(1 if cultpay == 'c' else 0)
                            else:
                                self.levelup(1)
                        else:
                            print("jj")
                    # Colonization

                if dice[use] == "Rocket":
                    print(*self.ship)
                    while True:
                        flywith = intput("Which rocket do you want to use?")
                        if flywith < len(self.ship):
                            if self.ship[flywith] is not None:
                                gcheck = 0
                                d.show_cards()
                                while True:
                                    fly = intput("Which galaxy do you want to fly to?")
                                    if fly < len(d.shown):
                                        while True:
                                            orbit = input(
                                                "Do you want to fly to the Orbit [O] or to the Surface [S]?\n")
                                            if (any("Player" in sublist for sublist in
                                                    d.shown[fly].rockets[1:])
                                                    if orbit == "O" else "Player"
                                                    in d.shown[fly].rockets[0]):
                                                print("You have already occupied this galaxy!")
                                                gcheck = 1
                                                break
                                            else:
                                                if self.ship[flywith] == d.shown[fly].name:
                                                    print(
                                                        "You cannot fly between the orbit and the surface!")
                                                else:
                                                    d.shown[fly].rockets[0 if orbit == "S" else 1].append(
                                                        "Player")
                                                    self.ship[flywith] = d.shown[fly].name
                                                    break
                                    if not gcheck:
                                        break
                                break
                            else:
                                print("This ship is not available.")
                        else:
                            print("You do not have that ship.")

                if dice[use] == "Energy" or "Culture":
                    is_economy = True if dice[use] == "Energy" else False
                    for shiploc in self.ship:
                        for galaxy in d.shown:
                            if shiploc == galaxy.name and is_economy and galaxy.culture == 0:
                                self.energy += 1
                            elif not is_economy and shiploc == galaxy.name and galaxy.culture == 1:
                                self.cult += 1
                        if shiploc == "Galaxy":
                            self.energy += 1
                    self.show()

                if dice[use] == "Diplomacy" or "Economy":  # choose one galaxy lol
                    print("hi")
                    is_economy = True if dice[use] == "Economy" else False
                    for shiploc in self.ship:
                        for galaxy in d.shown:
                            # print(galaxy.name, shiploc, ": ", shiploc == galaxy.name and e==1 and
                            # galaxy.stonks==1)
                            if shiploc == galaxy.name and is_economy and galaxy.stonks:
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
                    self.show()
                del dice[use]


"""
    def a(self):
        print(*self.ship)
        '''print(d.shown[1].rockets[0])
        print("Player" in d.shown[1].rockets[0])
        print(any("Player" in sublist for sublist in d.shown[1].rockets))'''
        while True:
            flywith = intput("Which rocket do you want to use?")
            if flywith < len(self.ship):
                if self.ship[flywith] is not None:
                    gcheck = 0
                    d.show_cards()
                    while True:
                        fly = intput("Which galaxy do you want to fly to?")
                        if fly < len(d.shown):
                            while True:
                                orbit = input("Do you want to fly to the Orbit [O] or to the Surface [S]?\n")
                                if (any("Player" in sublist for sublist in
                                        d.shown[fly].rockets[1:]) if orbit == "O" else "Player"
                                                                                       in d.shown[fly].rockets[0]):
                                    print("You have already occupied this galaxy!")
                                    gcheck = 1
                                    break
                                else:
                                    if self.ship[flywith] == d.shown[fly].name:
                                        print("You cannot fly between the orbit and the surface!")
                                    else:
                                        d.shown[fly].rockets[0 if orbit == "S" else 1].append("Player")
                                        self.ship[flywith] = d.shown[fly].name
                                        break
                            if not gcheck:
                                break
                    break
                else:
                    print("This ship is not available.")
            else:
                print("You do not have that ship.")
"""

# if __name__ == "__main__":
d = Deck()
# d.show()
# d.showCards()
g = Card(0, 0, 0, 0)
p = Player()
p.show()
# p.rockettest()
# p.a()
# p.a()
p.dice_throw()
for _ in range(5):
    p.levelup(1)
    # p.show()
