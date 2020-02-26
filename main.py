import random

symbols = ['♣', '♦', '♥', '♠']
numbers = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']


class Card:
    def __init__(self, _symbol, _number):
        self.symbol = _symbol
        self.number = _number

    def get(self):
        return self.symbol + ':' + self.number

    def __str__(self):
        return self.symbol + ':' + self.number

    def __gt__(self, other):
        self_number_index = numbers.index(self.number)
        other_number_index = numbers.index(other.number)

        if self_number_index > other_number_index:
            return True
        elif self_number_index < other_number_index:
            return False
        else:
            self_number_index = symbols.index(self.symbol)
            other_number_index = symbols.index(other.symbol)
            if self_number_index > other_number_index:
                return True
            elif self_number_index < other_number_index:
                return False
            else:
                raise ValueError

    def __eq__(self, other):
        if self.number == other.number and self.symbol == other.symbol:
            return True
        else:
            return False


class Deck:
    def __init__(self):
        print('Deck init')
        self.deck = []

    def get(self):
        return self.deck

    def print_all(self):
        print("length:"+str(len(self.deck)))
        for idx, i in enumerate(self.deck):
            print("--["+str(idx)+"] " + str(i))

    def shuffle(self):
        random.shuffle(self.deck)

    def fill_full(self):
        for i in symbols:
            for j in numbers:
                self.deck.append(Card(i, j))

    def add_card(self, _card):
        self.deck.append(_card)

    # 카드 한장을 뽑아 반환
    def draw_card(self, index):
        new_card = self.deck[index]
        return new_card


class Manager:
    # 플레이어 이름들의 배열을 받음
    def __init__(self, _player_names):
        self.players = []
        self.myDeck = Deck()
        self.myDeck.fill_full()
        self.myDeck.shuffle()
        for name in _player_names:
            self.players.append(Player(name))

    @staticmethod
    def greater(a, b):
        if a > b:
            return True
        else:
            return False

    # 각 플레이어에게 차례대로 카드 분배
    def card_distribute(self):

        _length = len(self.players)
        for idx, _card in enumerate(self.myDeck.deck):
            player_index = idx % _length
            self.players[player_index].myDeck.add_card(_card)

    # 모든 플레이어의 덱을 보여줌
    def show_players_deck(self):
        for player in self.players:
            print("------------------")
            print(player.name)
            player.myDeck.print_all()

    # 선(클럽3 보유자) 찾기
    def find_first(self):
        for player in self.players:
            if player.is_first():
                return player
        raise ValueError


def test_gt():

    def print_cards(a, b):
        print('---------------------------------')
        print('aCard:' + str(a) + '\t' + 'bCard:' + str(b))

        if a > b:
            print('aCard > bCard')
        else:
            print('aCard <= bCard')

    # 문양 같음, 숫자 다름
    a_card = Card(symbols[0], numbers[9])
    b_card = Card(symbols[0], numbers[3])
    print_cards(a_card, b_card)

    # 문양 다름, 숫자 다름
    a_card = Card(symbols[1], numbers[6])
    b_card = Card(symbols[2], numbers[4])
    print_cards(a_card, b_card)

    # 문양 다름, 숫자 같음
    a_card = Card(symbols[1], numbers[10])
    b_card = Card(symbols[2], numbers[10])
    print_cards(a_card, b_card)

    # 문양 같음, 숫자 같음
    a_card = Card(symbols[3], numbers[4])
    b_card = Card(symbols[3], numbers[4])
    print_cards(a_card, b_card)


class Player:
    def __init__(self, _name):
        self.name = _name
        self.myDeck = Deck()

    # 자신이 선(클럽3 보유자)인지 검사
    def is_first(self):
        _card = Card(symbols[0], numbers[0])
        return _card in self.myDeck.deck

    # 카드 내려놓기 시도
    def try_discard(self):
        self.myDeck.print_all()
        _str = input("제출할 카드 인덱스(ex: 1 2 3 4 5)를 입력: ")
        indexes = _str.split(" ")

        print("---discard---")
        for index in indexes:
            card = self.myDeck.draw_card(int(index))
            print(card)


def main():
    # test_gt()

    player_names = ["A", "B", "C", "D"]
    manager = Manager(player_names)
    manager.myDeck.shuffle()
    manager.card_distribute()

    manager.show_players_deck()
    print(manager.find_first().name)

    _player = Player("E")
    _player.myDeck.fill_full()
    _player.try_discard()


if __name__ == '__main__':
    main()
