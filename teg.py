import random


def intput(prompt, errormsg="Invalid input."):
    print(prompt, end=" ")
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

    def draw(self, pindex):
        card = self.cards.pop()
        self.shown.append(card)
        card.pos = pindex

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
            card.show_stats()


def show_dice(dice):
    for dienum in range(len(dice)):
        print(dienum, ": ", dice[dienum], sep="")


class Player:
    ship = ["Drewkaiden", "Jakks", None, None]

    def __init__(self):
        self.level = 1
        self.cult = 10
        self.energy = 2
        self.pts = 0
        self.ships = 2
        self.die_count = 4
        self.dice = [] * self.die_count
        self.deck = Deck()
        for die in range(self.die_count):
            throw = random.randint(1, 6)
            self.dice.append(action.get(throw))

    def show_stats(self):
        print("Level:", self.level, "| Ships:", self.ships, "| Dice:", self.die_count, "| Energy:", self.energy,
              "| Culture:", self.cult, "| Points:", self.pts)

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

    def die_reroll(self):
        rerolled = False
        # self.dice = [] * self.die_count

        while True:
            if rerolled:
                for i in range(self.die_count):
                    if self.dice[i] == "rerolled":
                        throw = random.randint(0, 5)
                        self.dice[i] = action.get(throw)
            else:
                for i in range(self.die_count):
                    throw = random.randint(0, 5)
                    self.dice[i] = action.get(throw)

            print("You have thrown:")
            show_dice(self.dice)

            if rerolled:
                break
            else:
                while True:
                    reroll = intput("How many do you wish to reroll?")
                    if reroll > self.die_count:
                        print("You don't have that many dice!")
                    elif reroll < 0:
                        print("Cannot reroll less than 0 dice!")
                    else:
                        break
                if reroll == self.die_count:
                    self.dice = ["rerolled"] * self.die_count
                elif reroll > 0:
                    for i in range(reroll):
                        while True:
                            num = {
                                0: "first",
                                1: "second",
                                2: "third",
                                3: "fourth"
                            }
                            nroll = intput("Select the number of the " + num.get(i) + " die you wish to reroll: ")
                            if nroll > len(self.dice) - 1 or nroll < 0:
                                print("Such die does not exist!")
                            elif self.dice[nroll] == "rerolled":
                                print("You have already rerolled this die!")
                            else:
                                self.dice[nroll] = "rerolled"
                                break
                elif reroll == 0:
                    break
                rerolled = True

    def die_convert(self):
        convert = input("Do you wish to use the convertor? (two dice to set one) ")
        if convert:
            show_dice(self.dice)
            for inst in range(1, 4):
                num = {
                    1: "first",
                    2: "second",
                    3: "third"
                }
                while True:
                    discard = intput("Select the number of the " + num.get(inst) + " die you wish to convert: ")
                    if discard > len(self.dice) - 1 or discard < 0:
                        print("Such die does not exist!")
                    elif self.dice[discard] == "converted":
                        print("You have already converted this die!")
                    else:
                        self.dice[discard] = "converted"
                        break
            while True:
                print(self.dice)
                for i in range(len(action)):
                    print(i, ": ", action[i], sep="")
                while True:
                    newdie = intput("Which action do you want to set? ")
                    if newdie > len(action) or newdie < 0:
                        print("Out of range!")
                    else:
                        break
                for i in range(self.die_count-1, -1, -1):
                    if self.dice[i] == 'converted':
                        del self.dice[i]
                self.dice.append(action[newdie])
                break

    def die_use(self):
        while True:
            show_dice(self.dice)
            use = intput("Which die do you want to use? ")

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
                    print(*self.ship)
                    while True:
                        rocket_id = intput("Which rocket do you want to use?")
                        if rocket_id < len(self.ship):
                            if self.ship[rocket_id] is not None:
                                self.deck.show_cards()
                                while True:
                                    fly = intput("Which galaxy do you want to fly to?")
                                    if fly < len(self.deck.shown):
                                        if any("Player" in sublist for sublist in self.deck.shown[fly].rockets):
                                            print("You have already occupied this galaxy!")
                                            break
                                        else:
                                            orbit = input("Do you want to fly to the [O]rbit or to the [S]urface?")
                                            if self.ship[rocket_id] == self.deck.shown[fly].name:
                                                print("You cannot fly between the orbit and the surface.")
                                            else:
                                                self.deck.shown[fly].rockets[0 if orbit == "S" else 1].append("Player")
                                                self.ship[rocket_id] = self.deck.shown[fly].name
                                                break
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
                        for galaxy in self.deck.shown:
                            if shiploc == galaxy.name:
                                if is_energy and galaxy.culture == 0:
                                    self.energy += 1
                                    print("\t+1 Energy for", galaxy.name)
                                elif not is_energy and galaxy.culture == 1:
                                    self.cult += 1
                                    print("\t+1 Culture for", galaxy.name)
                        if shiploc == "Galaxy":
                            self.energy += 1
                    self.show_stats()

                #
                # Economy && Diplomacy
                #
                if self.dice[use] == action[4] or self.dice[use] == action[5]:  # choose one galaxy lol
                    is_economy = True if self.dice[use] == action[4] else False
                    for shiploc in self.ship:
                        for galaxy in self.deck.shown:
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
                    self.show_stats()
                del self.dice[use]

    def die_throw(self):
        self.die_reroll()
        self.die_convert()
        self.die_use()


action = {
    0: "Colonization",
    1: "Rocket",
    2: "Energy",
    3: "Culture",
    4: "Economy",
    5: "Diplomacy"
}
# if __name__ == "__main__":
# d = Deck()
# d.show()
# d.showCards()
g = Card(0, 0, 0, 0)
p = Player()
p.show_stats()
# p.rockettest()
# p.a()
# p.a()
p.die_throw()
for _ in range(5):
    p.levelup(1)
    # p.show()
