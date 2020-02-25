import random

symbols = ["♣","♦","♥","♠"]
numbers = ["3","4","5","6","7","8","9","10", "J", "Q", "K", "A", "2"]

class Card:
    def __init__(self, _symbol, _number):
        self.symbol = _symbol
        self.number = _number

    def Get(self):
        return self.symbol + ":" + self.number

    def __str__(self):
        return self.symbol + ":" + self.number

    def __gt__(self, other):
        selfNumberIndex = numbers.index(self.number)
        otherNumberIndex = numbers.index(other.number)

        if selfNumberIndex > otherNumberIndex:
            return  True
        elif selfNumberIndex < otherNumberIndex:
            return False
        else :
            selfSymbolIndex = symbols.index(self.symbol)
            otherSymbolIndex = symbols.index(other.symbol)
            if selfSymbolIndex > otherSymbolIndex:
                return True
            elif selfSymbolIndex < otherSymbolIndex:
                return False
            else:
                raise ValueError

class Deck:
    def __init__(self):
        print("Deck init")
        self.deck = []
        for i in symbols:
            for j in numbers:
                self.deck.append(Card(i, j))

    def Get(self):
        return self.deck

    def PrintAll(self):
        for i in self.deck:
            print(i)

    def Shuffle(self):
        random.shuffle(self.deck)

class Manager:
    def __init__(self, _playerNumber):
        self.playerNumber = _playerNumber
        self.myDeck = Deck()
        self.myDeck.Shuffle()

    def Greater(self, a, b):
        if a > b:
            return True
        else :
            return False

def TestGt():
    # 문양 같음, 숫자 다름
    aCrad = Card(symbols[0],numbers[0])
    print("aCrad" + str(aCrad))
    bCrad = Card(symbols[0], numbers[1])
    print("bCrad" + str(bCrad))

    if aCrad > bCrad:
        print("aCrad > bCrad")
    else:
        print("aCrad <= bCrad")

    # 문양 다름, 숫자 다름
    aCrad = Card(symbols[1], numbers[0])
    print("aCrad" + str(aCrad))
    bCrad = Card(symbols[0], numbers[1])
    print("bCrad" + str(bCrad))

    if aCrad > bCrad:
        print("aCrad > bCrad")
    else:
        print("aCrad <= bCrad")

    # 문양 같음, 숫자 다름
    aCrad = Card(symbols[1], numbers[0])
    print("aCrad" + str(aCrad))
    bCrad = Card(symbols[1], numbers[1])
    print("bCrad" + str(bCrad))

    if aCrad > bCrad:
        print("aCrad > bCrad")
    else:
        print("aCrad <= bCrad")

    # 문양 같음, 숫자 같음
    aCrad = Card(symbols[1], numbers[1])
    print("aCrad" + str(aCrad))
    bCrad = Card(symbols[1], numbers[1])
    print("bCrad" + str(bCrad))

    if aCrad > bCrad:
        print("aCrad > bCrad")
    else:
        print("aCrad <= bCrad")

def Main():
    manager = Manager(4)

if __name__ == '__main__':
    Main()