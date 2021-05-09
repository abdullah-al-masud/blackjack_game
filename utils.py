import time
import numpy as np


def wait(t = 2):
    time.sleep(t)

def pick_a_card(cards, remove = True, manual = False):
    
    if manual:
        return input('name a card to pick:')
    else:
        suit_pick = list(cards.keys())[np.random.randint(0, 100) % len(cards)]
        card_pick = cards[suit_pick][np.random.randint(0, 100) % len(cards[suit_pick])]
        if remove:
            del cards[suit_pick][cards[suit_pick].index(card_pick)]
            if len(cards[suit_pick]) == 0:
                del cards[suit_pick]
        return suit_pick + '_' + card_pick

# blackjack
def calc_points(cards, base_val = 21):
    card_values = {'A' : 11, 'J' : 10, 'Q' : 10, 'K' : 10, '2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9, '10' : 10}
    points = 0
    A_present = False
    for i in range(len(cards)):
        points += card_values[cards[i].split('_')[-1]]
        if cards[i].split('_')[-1] == 'A':
            A_present = True
    if points > base_val and A_present:
        points -= 10
    return points


def card_inc(card_box, n, cnt, shuffle_point, ndeck):
    if cnt + n >= shuffle_point:
        card_box = {
            'heart' : (['A', 'J', 'Q', 'K'] + ['%d'%i for i in range(2, 11)]) * ndeck, 
            'diamond' : (['A', 'J', 'Q', 'K'] + ['%d'%i for i in range(2, 11)]) * ndeck, 
            'club' : (['A', 'J', 'Q', 'K'] + ['%d'%i for i in range(2, 11)]) * ndeck, 
            'spade' : (['A', 'J', 'Q', 'K'] + ['%d'%i for i in range(2, 11)]) * ndeck
        }
        shuffle_point = np.random.randint((ndeck * 52) // 4, (ndeck * 52 * 3) // 4)
        cnt = n
    else:
        cnt += n
    return card_box, cnt, shuffle_point


class Player:
    pl_cnt = 0
    
    def __init__(self, name=''):
        self.money = 500
        Player.pl_cnt += 1
        self.name = name if name.replace(' ', '') != '' else 'Player-%d'%Player.pl_cnt
    
    def new_session(self, card_box):
        self.bj_state = False
        self.cards = [pick_a_card(card_box, True), pick_a_card(card_box, True)]
        self.points = calc_points(self.cards)
        
    def set_bet(self, lowest_bet):
        self.bet = int(input('fund : %d,   enter the initial bet : '%self.money))
        while True:
            if self.bet < lowest_bet:
                self.bet = int(input('invalid !!   lowest required bed is : %d, enter the bet again : '%lowest_bet))
                continue
            if self.bet > self.money:
                self.bet = int(input('invalid !!   fund : %d, enter the bet again : '%self.money))
            else:
                self.money -= self.bet
                break
    
    def add_bet(self):
        bet = int(input('fund : %d,   enter the additional bet : '%self.money))
        while True:
            if bet > self.money:
                bet = int(input('invalid !!   fund : %d, enter the bet again : '%self.money))
            else:
                self.bet += bet
                self.money -= bet
                break
    
    def show_state(self):
        print('your cards : ', self.cards, '\t\t total points : ', self.points)
    
    def check_blackjack(self, base_point):
        if self.points == base_point:
            self.bj_state = True
            print('!!!!!!!! BLACKJACK !!!!!!!!!!')
        return self.bj_state
    
    def hit(self, card_box):
        self.cards += [pick_a_card(card_box, True)]
        self.points = calc_points(self.cards)
        self.show_state()
    
    def update_money(self, win_flag):
        if win_flag == 'w':
            if self.bj_state:
                self.money += (1.5 + 1) * self.bet
            else:
                self.money += self.bet * 2
        elif win_flag == 'd':
            self.money += self.bet
        if self.money <= 0:
            self.money = 0

