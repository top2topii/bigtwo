import random

symbols = ['♣', '♦', '♥', '♠']
numbers = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
real_nums = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']


class Card:
    def __init__(self, _symbol, _number):
        self.symbol = _symbol
        self.number = _number
        self.point = numbers.index(_number) * 4 + symbols.index(_symbol)

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
        return self.point > other.point

        # if self_number_index > other_number_index:
        #     return True
        # elif self_number_index < other_number_index:
        #     return False
        # else:
        #     self_symbol_index = symbols.index(self.symbol)
        #     other_symbol_index = symbols.index(other.symbol)
        #     if self_symbol_index > other_symbol_index:
        #         return True
        #     elif self_symbol_index < other_symbol_index:
        #         return False
        #     else:
        #         raise ValueError

    def __eq__(self, other):
        return self.point == other.point
        # return self.number == other.number and self.symbol == other.symbol

    def __hash__(self):
        return hash(str(self))


class Deck:
    def __init__(self):
        print('Deck init')
        self.deck = []

    def get(self):
        return self.deck

    def print_all(self):
        print("length:" + str(len(self.deck)))
        for idx, i in enumerate(self.deck):
            print("--[" + str(idx) + "] " + str(i))

    def shuffle(self):
        random.shuffle(self.deck)

    def fill_full(self):
        for i in symbols:
            for j in numbers:
                self.deck.append(Card(i, j))

    def add_card(self, _card):
        self.deck.append(_card)

    def add_cards(self, _cards):
        self.deck += _cards

    # 카드 한장을 뽑아 반환
    def draw_card(self, index):
        new_card = self.deck[index]
        return new_card

    # 덱 전부 비우기
    def remove_all(self):
        self.deck.clear()

    # replace
    def replace(self, cards):
        self.deck.clear()
        self.add_cards(cards)


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
    # 규칙0. 선이면 어떤 카드도 낼 수 있다(족보에 해당한다면)
    # 규칙1. 테이블에 있는 카드 갯수 == 제출한 카드 갯수 일것
    # 규칙2. 테이블보다 높은 패여야만 한다
    def check_submit(self, _cards):

        # 족보 검사
        if not Rule.is_in_rank(_cards):
            return False

        # 테이블에 카드가 이미 있다면
        if self.myDeck.deck:
            if not self.check_rule1(_cards):
                return False
            if not self.check_rule2(_cards):
                return False

        return True

    # 규칙1 검사
    def check_rule1(self, _cards):
        if len(self.myDeck.deck) == len(_cards):
            return True
        return False

    # 규칙2 검사
    def check_rule2(self, _cards):
        return Rule.is_high(self.myDeck.deck, _cards)


class Rule:
    # 2장의 카드 리스트를 받는다
    @staticmethod
    def check_pair(_cards):

        if not len(_cards) == 2:
            raise ValueError

        if not _cards[0].check_same_number(_cards[1]):
            return False
        return True

    # 3장의 카드 리스트를 받는다
    @staticmethod
    def check_triple(_cards):

        if not len(_cards) == 3:
            raise ValueError

        if not _cards[0].check_same_number(_cards[1]):
            return False
        if not _cards[1].check_same_number(_cards[2]):
            return False
        return True

    # 5장의 카드 리스트를 받는다
    @staticmethod
    def check_five_cards(cards):

        if not len(cards) == 5:
            raise ValueError

        if Rule.check_straight(cards): return True
        if Rule.check_flush(cards): return True
        if Rule.check_fullhouse(cards): return True
        if Rule.check_fourcards(cards): return True

        return False

    # 스트레이트 검사
    @staticmethod
    def check_straight(_cards):
        _list = []
        for _card in _cards:
            i = real_nums.index(_card.number)
            _list.append(i)
        _list.sort()

        if Rule.check_mountain(_list):
            return True

        for idx, j in enumerate(_list):
            if idx == len(_list) - 1:
                break

            if not j + 1 == _list[idx + 1]:
                return False
        return True

    @staticmethod
    def check_mountain(indexes):
        if indexes == [real_nums.index('A'), real_nums.index('10'),
                       real_nums.index('J'), real_nums.index('Q'), real_nums.index('K')]:
            return True
        return False

    @staticmethod
    def check_flush(_cards):
        for _card in _cards:
            if not _card.symbol == _cards[0].symbol:
                return False
        return True

    @staticmethod
    def count_same_number(_cards):
        mydic = {}
        for _card in _cards:
            key = _card.number
            if key in mydic:
                mydic[key] += 1
            else:
                mydic[key] = 1

        # mydic 의 갯수는 2개 각각의 값이 2,3
        length = len(mydic)
        list_values = list(mydic.values())
        list_values.sort()

        return list_values

    @staticmethod
    def check_fullhouse(_cards):
        list_values = Rule.count_same_number(_cards)
        if len(list_values) == 2 and list_values == [2, 3]:
            return True

        return False

    @staticmethod
    def check_fourcards(_cards):
        list_values = Rule.count_same_number(_cards)
        if len(list_values) == 2 and list_values == [1, 4]:
            return True

        return False

    # 족보에 해당하는 지 검사
    @staticmethod
    def is_in_rank(cards):
        length = len(cards)

        if length == 1:
            return True
        elif length == 2:
            return Rule.check_pair(cards)
        elif length == 3:
            return Rule.check_triple(cards)
        elif length == 5:
            return Rule.check_five_cards(cards)
        else:
            return False

    # sort 된 cards를 받는다.
    @staticmethod
    def is_high_straight(cards_a, cards_b):

        a_score = (numbers.index(cards_a[0].number) + 1) * 10000 \
            + numbers.index(cards_a[1].number) * 100 + symbols.index(cards_a[0].symbol)
        b_score = (numbers.index(cards_b[0].number) + 1) * 10000 \
            + numbers.index(cards_b[1].number) * 100 + symbols.index(cards_b[0].symbol)

        return a_score < b_score

    # sort 된 cards를 받는다.
    @staticmethod
    def is_high_flush(cards_a, cards_b):

        # 문양만 가지고 먼저 확인한다.
        # 문양이 같다면 숫자를 비교
        if cards_a[0].symbol < cards_b[0].symbol:
            return True
        elif cards_a[0].symbol == cards_b[0].symbol:
            return cards_a[0].number < cards_b[0].number

        return False

    @staticmethod
    def is_high_as_rank(rank, cards_a, cards_b):

        if rank == 1 or rank == 5:   # straight / straight flush
            return Rule.is_high_straight(cards_a, cards_b)
        elif rank == 2:     # flush
            return Rule.is_high_flush(cards_a, cards_b)
        elif rank < 5:  # fullhouse / fourcards
            return get_same_card_num(cards_a) < get_same_card_num(cards_b)

    # rule2 에 해당하기에 같은 카드 검사를 거친후 온다.
    # 1/2/3/5 제출 장수에 따라 대응하자.
    @staticmethod
    def is_high(cards_a, cards_b):
        length = len(cards_a)
        cards_a.sort(key=lambda x: x.point, reverse=True)
        cards_b.sort(key=lambda x: x.point, reverse=True)

        # 한장씩 높은 순서대로 비교
        # TODO: 높은 카드 순서대로 비교
        # 1/2/3 일 경우
        if length < 5:
            if cards_a[0] < cards_b[0]:
                return True
            return False

        # fullhouse 나 fourcards 일 경우는 비교순서를 3장 또는 4장에서 먼저 해야됨됨
        # length = len(cards_b)

        # 5장일 경우 족보의 종류를 rank 로 구분한다.
        # straight, flush, fullhouse, fourcards, straight flush
        # rank   1,     2,         3,         4,              5
        rank_a = Rule.get_rank(cards_a)
        rank_b = Rule.get_rank(cards_b)
        if rank_b > rank_a:
            return True
        elif rank_a == rank_b:
            return Rule.is_high_as_rank(rank_a, cards_a, cards_b)
        else:
            return False

    @staticmethod
    def get_rank(cards):
        rank = 0
        if Rule.check_straight(cards):
            rank = 1
        if Rule.check_flush(cards):
            if Rule.check_straight(cards):
                rank = 5
            else:
                rank = 2
        if Rule.check_fullhouse(cards):
            rank = 3
        if Rule.check_fourcards(cards):
            rank = 4
        return rank


# 가장 많이 중복된 숫자를 돌려준다.
# fullhouse 경우 3장의 숫자를 알려주고
# fourcards 경우 4장의 숫자를 알려준다.
def get_same_card_num(cards):
    most_same = 0
    mydic = {}
    for card in cards:
        key = card.number
        if key in mydic:
            mydic[key] += 1
        else:
            mydic[key] = 1

    res = sorted(mydic.items(), key=lambda x: x[1], reverse=True)
    return res[0][0]


# num 숫자를 가진 카드중 가장 높은 카드 한장을 구한다.
def get_highest_card(cards, num):

    # 제일 낮은 카드로 초기화
    highest_card = Card(symbols[0], numbers[0])

    for card in cards:
        if card.number == num and highest_card.point < card.point:
            highest_card = card

    return highest_card


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


def test_straight():
    rule = Rule()

    cards = [Card('♣', 'K'), Card('♣', 'Q'), Card('♣', '10'), Card('♣', 'A'), Card('♣', 'J')]
    print("case1:" + str(rule.check_straight(cards)))

    cards = [Card('♣', 'A'), Card('♣', '2'), Card('♣', '5'), Card('♣', '3'), Card('♣', '4')]
    print("case2:" + str(rule.check_straight(cards)))

    cards = [Card('♣', '8'), Card('♣', 'Q'), Card('♣', '10'), Card('♣', 'A'), Card('♣', 'J')]
    print("case3:" + str(rule.check_straight(cards)))

    cards = [Card('♣', '2'), Card('♣', '5'), Card('♣', '3'), Card('♣', '4'), Card('♣', '6')]
    print("case4:" + str(rule.check_straight(cards)))

    cards = [Card('♣', 'K'), Card('♣', 'K'), Card('♣', '10'), Card('♣', 'K'), Card('♣', 'J')]
    print("case5:" + str(rule.check_straight(cards)))


def test_flush():
    rule = Rule()

    print("Flush Test---------------------------------")
    cards = [Card('♣', 'K'), Card('♣', 'K'), Card('♦', 'K'), Card('♣', 'A'), Card('♣', 'A')]
    print("case1:" + str(rule.check_flush(cards)))

    cards = [Card('♣', 'A'), Card('♣', '2'), Card('♣', '5'), Card('♣', '3'), Card('♣', '4')]
    print("case2:" + str(rule.check_flush(cards)))

    cards = [Card('♣', '8'), Card('♣', 'Q'), Card('♣', '8'), Card('♦', 'Q'), Card('♣', 'Q')]
    print("case3:" + str(rule.check_flush(cards)))

    cards = [Card('♦', '8'), Card('♦', 'Q'), Card('♦', '8'), Card('♦', 'Q'), Card('♦', 'Q')]
    print("case4:" + str(rule.check_flush(cards)))


def test_fullhouse():
    rule = Rule()

    print("Fullhouse Test---------------------------------")
    cards = [Card('♣', 'K'), Card('♣', 'K'), Card('♣', 'K'), Card('♣', 'A'), Card('♣', 'A')]
    print("case1:" + str(rule.check_fullhouse(cards)))

    cards = [Card('♣', 'A'), Card('♣', '2'), Card('♣', '5'), Card('♣', '3'), Card('♣', '4')]
    print("case2:" + str(rule.check_fullhouse(cards)))

    cards = [Card('♣', 'Q'), Card('♣', 'Q'), Card('♣', '8'), Card('♣', 'Q'), Card('♣', 'Q')]
    print("case3:" + str(rule.check_fullhouse(cards)))

    cards = [Card('♣', '8'), Card('♣', 'Q'), Card('♣', '8'), Card('♣', 'Q'), Card('♣', 'Q')]
    print("case4:" + str(rule.check_fullhouse(cards)))


def test_fourcards():
    rule = Rule()

    print("Fullhouse Test---------------------------------")
    cards = [Card('♣', 'K'), Card('♣', 'K'), Card('♣', 'K'), Card('♣', 'A'), Card('♣', 'A')]
    print("case1:" + str(rule.check_fourcards(cards)))

    cards = [Card('♣', 'A'), Card('♣', '2'), Card('♣', '5'), Card('♣', '3'), Card('♣', '4')]
    print("case2:" + str(rule.check_fourcards(cards)))

    cards = [Card('♣', 'Q'), Card('♣', 'Q'), Card('♣', '8'), Card('♣', 'Q'), Card('♣', 'Q')]
    print("case3:" + str(rule.check_fourcards(cards)))

    cards = [Card('♣', '8'), Card('♣', 'Q'), Card('♣', '8'), Card('♣', 'Q'), Card('♣', 'Q')]
    print("case4:" + str(rule.check_fourcards(cards)))


def test_card_sort():
    deck = Deck()
    cards = [Card('♣', 'A'), Card('♣', '2'), Card('♣', '5'), Card('♣', '3'), Card('♣', '4')]

    deck.add_cards(cards)
    deck.deck.sort(key=lambda x: x.point)
    deck.print_all()

    deck.remove_all()
    cards = [Card('♣', '8'), Card('♦', 'Q'), Card('♦', '8'), Card('♣', 'Q'), Card('♥', 'Q')]

    deck.add_cards(cards)
    deck.deck.sort(key=lambda x: x.point)
    deck.print_all()


def test_is_high_straight():
    deck = Deck()
    rule = Rule()

    cards_a = [Card('♣', 'A'), Card('♣', '2'), Card('♥', '5'), Card('♣', '3'), Card('♣', '4')]
    cards_b = [Card('♥', 'A'), Card('♥', '2'), Card('♣', '5'), Card('♥', '3'), Card('♥', '4')]

    deck.add_cards(cards_a)
    deck.print_all()
    deck.remove_all()

    deck.add_cards(cards_b)
    deck.print_all()
    deck.remove_all()

    result = rule.is_high_straight(cards_a, cards_b)
    print(result)

    cards_c = [Card('♣', 'A'), Card('♣', '2'), Card('♥', '5'), Card('♣', '3'), Card('♣', '4')]
    cards_d = [Card('♥', '6'), Card('♥', '2'), Card('♣', '5'), Card('♥', '3'), Card('♥', '4')]

    deck.add_cards(cards_c)
    deck.print_all()
    deck.remove_all()

    deck.add_cards(cards_d)
    deck.print_all()
    deck.remove_all()

    result = rule.is_high_straight(cards_c, cards_d)
    print(result)

    cards_c = [Card('♣', '6'), Card('♣', '2'), Card('♥', '5'), Card('♣', '3'), Card('♣', '4')]
    cards_d = [Card('♥', 'A'), Card('♥', 'J'), Card('♣', 'Q'), Card('♥', 'K'), Card('♥', '10')]

    deck.add_cards(cards_c)
    deck.print_all()
    deck.remove_all()

    deck.add_cards(cards_d)
    deck.print_all()
    deck.remove_all()

    result = rule.is_high_straight(cards_c, cards_d)
    print(result)


def test_get_same_card_num():
    deck = Deck()
    rule = Rule()

    cards_a = [Card('♣', 'A'), Card('♣', '5'), Card('♦', '5'), Card('♦', 'A'), Card('♥', '5')]
    result = get_same_card_num(cards_a)
    deck.add_cards(cards_a)
    deck.print_all()
    print(get_highest_card(cards_a, result))

    cards_a = [Card('♣', '8'), Card('♣', '5'), Card('♥', '5'), Card('♠', '5'), Card('♦', '5')]
    result = get_same_card_num(cards_a)
    deck.remove_all()
    deck.add_cards(cards_a)
    deck.print_all()
    print(result)
    print(get_highest_card(cards_a, result))

    cards_a = [Card('♣', '8'), Card('♥', '8')]
    result = get_same_card_num(cards_a)
    deck.remove_all()
    deck.add_cards(cards_a)
    deck.print_all()
    print(result)
    print(get_highest_card(cards_a, result))

    cards_a = [Card('♣', 'J'), Card('♥', 'J'), Card('♦', 'J')]
    result = get_same_card_num(cards_a)
    deck.remove_all()
    deck.add_cards(cards_a)
    deck.print_all()
    print(result)
    print(get_highest_card(cards_a, result))


# 테이블에 제출할 수 있는지 검사
def test_check_submit():
    deck = Deck()
    t = Table()
    cards_a = [Card('♣', '8')]
    cards_b = [Card('♦', '8')]
    t.myDeck.deck = cards_a
    deck.add_cards(cards_b)

    result = t.check_submit(cards_b)
    t.myDeck.print_all()
    deck.print_all()
    print(result)

    cards_a = [Card('♣', '8'), Card('♦', '8')]
    cards_b = [Card('♠', '8'), Card('♥', '8')]
    t.myDeck.deck = cards_a
    deck.remove_all()
    deck.add_cards(cards_b)

    result = t.check_submit(cards_b)
    t.myDeck.print_all()
    deck.print_all()
    print(result)

    cards_a = [Card('♣', 'K'), Card('♣', 'Q'), Card('♣', '10'), Card('♣', 'A'), Card('♣', 'J')]
    cards_b = [Card('♣', '2'), Card('♣', '5'), Card('♣', '3'), Card('♣', '4'), Card('♣', '6')]
    t.myDeck.replace(cards_a)
    deck.replace(cards_b)

    result = t.check_submit(cards_b)
    print(Rule.get_rank(cards_a))
    t.myDeck.print_all()
    print(Rule.get_rank(cards_b))
    deck.print_all()
    print(result)

    cards_a = [Card('♣', 'K'), Card('♣', 'Q'), Card('♣', '10'), Card('♣', 'A'), Card('♣', 'J')]
    cards_b = [Card('♣', 'K'), Card('♣', 'K'), Card('♦', 'K'), Card('♣', 'A'), Card('♣', 'A')]
    t.myDeck.replace(cards_a)
    deck.replace(cards_b)

    result = t.check_submit(cards_b)
    print(Rule.get_rank(cards_a))
    t.myDeck.print_all()
    print(Rule.get_rank(cards_b))
    deck.print_all()
    print(result)


def main():
    # test_gt()
    # test_straight()
    # test_fullhouse()
    # test_flush()
    # test_fourcards()

    # player_names = ["A", "B", "C", "D"]
    # manager = Manager(player_names)
    # manager.myDeck.shuffle()
    # manager.card_distribute()
    #
    # manager.show_players_deck()
    # print(manager.find_first().name)
    #
    # _player = Player("E")
    # _player.myDeck.fill_full()
    # _player.try_discard()
    # test_card_sort()
    # test_is_high_straight()
    # test_get_same_card_num()
    test_check_submit()
    # pass


if __name__ == '__main__':
    main()
