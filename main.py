import random

symbols = ['♣', '♦', '♥', '♠']
numbers = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']


class Card:
    def __init__(self, _symbol, _number):
        self.symbol = _symbol
        self.number = _number

    def Get(self):
        return self.symbol + ':' + self.number

    def __str__(self):
        return self.symbol + ':' + self.number

    def __gt__(self, other):
        selfNumberIndex = numbers.index(self.number)
        otherNumberIndex = numbers.index(other.number)

        if selfNumberIndex > otherNumberIndex:
            return True
        elif selfNumberIndex < otherNumberIndex:
            return False
        else:
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
        print('Deck init')
        self.deck = []

    def Get(self):
        return self.deck

    def PrintAll(self):
        for i in self.deck:
            print(i)

    def Shuffle(self):
        random.shuffle(self.deck)

    def FullFill(self):
        for i in symbols:
            for j in numbers:
                self.deck.append(Card(i, j))

    def AddCard(self, aCard):
        self.deck.append(aCard)


class Manager:
    def __init__(self, _playerNumber):
        self.playerNumber = _playerNumber
        self.myDeck = Deck()
        self.myDeck.FullFill()
        self.myDeck.Shuffle()

    @staticmethod
    def Greater(a, b):
        if a > b:
            return True
        else:
            return False


def TestGt():

    def PrintCards(a, b):
        print('---------------------------------')
        print('aCard:' + str(a) + '\t' + 'bCard:' + str(b))

        if a > b:
            print('aCard > bCard')
        else:
            print('aCard <= bCard')

    # 문양 같음, 숫자 다름
    aCard = Card(symbols[0], numbers[9])
    bCard = Card(symbols[0], numbers[3])
    PrintCards(aCard, bCard)

    # 문양 다름, 숫자 다름
    aCard = Card(symbols[1], numbers[6])
    bCard = Card(symbols[2], numbers[4])
    PrintCards(aCard, bCard)

    # 문양 다름, 숫자 같음
    aCard = Card(symbols[1], numbers[10])
    bCard = Card(symbols[2], numbers[10])
    PrintCards(aCard, bCard)

    # 문양 같음, 숫자 같음
    aCard = Card(symbols[3], numbers[4])
    bCard = Card(symbols[3], numbers[4])
    PrintCards(aCard, bCard)


def Main():
    manager = Manager(4)
    TestGt()


if __name__ == '__main__':
    Main()
