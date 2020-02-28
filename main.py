import random

symbols = ['♣', '♦', '♥', '♠']
numbers = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']


class Card:
    def __init__(self, _symbol, _number):
        self.symbol = _symbol
        self.number = _number

    def get(self):
        return self.symbol + ':' + self.number

    # 자신과 other 숫자가 같은가?
    def check_same_number(self, other):
        if self.number == other.number:
            return True
        return False

    def check_same_symbol(self, other):
        if self.symbol == other.symbol:
            return True
        return False

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
        return self.number == other.number and self.symbol == other.symbol

    def __hash__(self):
        return hash(str(self))


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

    # 덱 전부 비우기
    def remove_all(self):
        self.deck.clear()


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


def check_duplicate(listOfElems):
    # Check if given list contains any duplicates
    for elem in listOfElems:
        if listOfElems.count(elem) > 1:
            return True
    return False


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

    # 바른 인덱스들을 입력받을 때까지 loop
    def get_right_cards(self):
        _cards = []
        is_success = True

        while True:
            _cards.clear()
            _str = input("제출할 카드 인덱스(ex: 1 2 3 4 5)를 입력: ")
            indexes = _str.split(" ")

            for index in indexes:
                # int 타입 변환 실패 시 처음으로, 인덱스 범위를 벗어나도 처음으로
                try:
                    i = int(index)
                    _card = self.myDeck.deck[i]
                except (ValueError, IndexError) as e:
                    print("잘못된 인덱스 입니다. 에러: " + str(e))
                    is_success = False
                    break
                _cards.append(_card)

            if not is_success:
                is_success = True
                continue

            # 중복 입력 검사
            if check_duplicate(_cards):
                print("중복된 카드를 선택할 수 없습니다.")
                continue

            return _cards

    # 카드 내려놓기 시도
    def try_discard(self):
        self.myDeck.print_all()

        # 내려놓을 카드들 보여주기
        _cards = self.get_right_cards()
        _deck = Deck()
        for c in _cards:
            _deck.add_card(c)
        _deck.print_all()


class Table:
    def __init__(self):
        self.myDeck = Deck()

    # 카드 리스트를 받아 낼수 있는지 검사
    # 규칙1. 테이블에 있는 카드 갯수 == 제출한 카드 갯수 일것
    # 규칙2. 테이블보다 높은 패여야만 한다
    def check_submit(self, _cards):
        # 족보 검사

        # 테이블에 카드가 이미 있다면
        if self.myDeck:
            if not self.check_rule1(_cards):
                return False
            if not self.check_rule2(_cards):
                return False

        return True

    # 규칙1 검사
    def check_rule1(self, _cards):
        if self.myDeck.deck.count() == _cards.count():
            return True
        return False

    # 규칙2 검사
    def check_rule2(self, _cards):
        for _card in _cards:
            return True
        return True


class Rule:
    # 2장의 카드 리스트를 받는다
    def check_pair(self, _cards):

        if not len(_cards) == 2:
            raise ValueError

        if not _cards[0].check_same_number(_cards[1]):
            return False
        return True

    # 3장의 카드 리스트를 받는다
    def check_triple(self, _cards):

        if not len(_cards) == 3:
            raise ValueError

        if not _cards[0].check_same_number(_cards[1]):
            return False
        if not _cards[1].check_same_number(_cards[2]):
            return False
        return True

    # 5장의 카드 리스트를 받는다
    def check_five_cards(self, _cards):

        if not len(_cards) == 5:
            raise ValueError

        if not _cards[0].check_same_number(_cards[1]):
            return False
        if not _cards[1].check_same_number(_cards[2]):
            return False
        return True


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
