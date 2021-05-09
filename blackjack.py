from utils import *

# initiate
base_point = 21
deal_lbase = 17
lowest_bet = 5
yes = ['y', 'yes']
no = ['n', 'no']
ndeck = 6


init_players = int(input('enter total players : '))
players = np.array([Player(input('enter name - %d : '%(i + 1))) for i in range(init_players)])

# game begins
card_box = {
    'heart' : (['A', 'J', 'Q', 'K'] + ['%d'%i for i in range(2, 11)]) * ndeck, 
    'diamond' : (['A', 'J', 'Q', 'K'] + ['%d'%i for i in range(2, 11)]) * ndeck, 
    'club' : (['A', 'J', 'Q', 'K'] + ['%d'%i for i in range(2, 11)]) * ndeck, 
    'spade' : (['A', 'J', 'Q', 'K'] + ['%d'%i for i in range(2, 11)]) * ndeck
}
card_cnt = 0
shuffle_point = np.random.randint((ndeck * 52) // 2, ndeck * 52)

while True:
    # starting round
    total_players = len(players)
    bjs = [False for i in range(total_players)]
    left_over = [None for i in range(total_players)]
    win_state = ['l' for i in range(total_players)]
    
    # dealer's cards and points
    # print(card_box)
    print('dealer is picking two cards...')
    card_box, card_cnt, shuffle_point = card_inc(card_box, 2, card_cnt, shuffle_point, ndeck)
    dealer_cards = [pick_a_card(card_box, True), pick_a_card(card_box, True)]
    dealer_point = calc_points([dealer_cards[0]])
    
    # showing the current points and card of the dealer
    print('-----------------------------------------------------------')
    print('------------dealer 1st card : [', dealer_cards[0], ']   total points : ', dealer_point)
    print('-----------------------------------------------------------\n')
    wait()
    
    for i in range(total_players):
        print(' ****************** PLAYER - %s ****************'%players[i].name)
        # setting initial bet
        players[i].set_bet(lowest_bet)
        wait(.5)
    
    for i in range(total_players):
        print(' ****************** PLAYER - %s ****************'%players[i].name)
        # start session
        print('player is picking two cards...')
        card_box, card_cnt, shuffle_point = card_inc(card_box, 2, card_cnt, shuffle_point, ndeck)
        players[i].new_session(card_box)
        # print(card_box)
        players[i].show_state()
        bjs[i] = players[i].check_blackjack(base_point)
        wait()
    
    for i in range(total_players):
        # showing the current points and card of the dealer
        print('-----------------------------------------------------------')
        print('------------dealer 1st card : [', dealer_cards[0], ']   total points : ', dealer_point)
        print('-----------------------------------------------------------\n')
        wait()
        
        print(' ****************** PLAYER - %s ****************'%players[i].name)
        players[i].show_state()
        if bjs[i]:
            left_over[i] = players[i].points
        else:
            while True:
                # stop betting ?
                hit_stand = input('do you want to hit ? (y / n)')
                if hit_stand.lower() in yes:
                    # add bet
                    if players[i].money > 0:
                        dec = input('present bet : %d\t fund : %d\t\t want to add bet ? (y / n)'%(players[i].bet, players[i].money))
                        if dec.lower() in yes:
                            players[i].add_bet()
                            print('bet raised to : %d'%players[i].bet)
                    
                    wait(.5)
                    # new card
                    print('player is picking a new card...')
                    card_box, card_cnt, shuffle_point = card_inc(card_box, 1, card_cnt, shuffle_point, ndeck)
                    players[i].hit(card_box)
                    if players[i].points > base_point:
                        left_over[i] = players[i].points
                        break
                elif hit_stand.lower() in no:
                    left_over[i] = players[i].points
                    break
                else:
                    print('invalid input !!  valid is "y" or "n"')
        # print(card_box)
    
    bjs = np.array(bjs)
    win_state = np.array(win_state)
    left_over = np.array(left_over)
#     print(bjs, win_state, left_over)
    
    # win or lose
    # showing the current points and card of the dealer
    dealer_point = calc_points(dealer_cards)
    print('dealer cards : ', dealer_cards, '\t\t total points : ', dealer_point)
    wait()
    
    # dealer has blackjack
    if dealer_point == base_point:
        win_state[bjs] = 'd'
    else:
        # straight win for blackjacks
        win_state[bjs] = 'w'
        
        # dealer will pick
        while True:
            
            if dealer_point >= deal_lbase:
                break
            else:
                print('dealer is picking a new card...')
                dealer_cards += [pick_a_card(card_box, True)]
                dealer_point = calc_points(dealer_cards)
                print('dealer cards : ', dealer_cards, '\t\t total points : ', dealer_point)
                wait()
        
        # checking the situations of winning or losing
        # print(bjs, win_state, left_over)
        # print(((left_over > dealer_point) & (left_over <= base_point)), left_over <= base_point, (left_over == dealer_point))
        if dealer_point > base_point:
            win_state[left_over <= base_point] = 'w'
        else:
            win_state[((left_over > dealer_point) & (left_over <= base_point)) & ~bjs] = 'w'
            win_state[(left_over == dealer_point) & ~bjs] = 'd'
    # print(win_state)
    # settling the money
    for i in range(total_players):
        players[i].update_money(win_state[i])
        if win_state[i] == 'w':
            wstate, gstate = 'wins', 'gains'
        elif win_state[i] == 'd':
            wstate, gstate = 'draws', 'gets back'
        else:
            wstate, gstate = 'loses', 'loses'
        print('"%s" %s, %s bet of %d, current fund: %d'%(players[i].name, wstate, gstate, players[i].bet if not bjs[i] else 1.5 * players[i].bet, players[i].money))
    
    bankrupt = np.array([players[i].money for i in range(total_players)]) < lowest_bet
    wait()
    if bankrupt.sum() > 0:
        print('\\\\\\\\\players ', [players[i].name for i in np.where(bankrupt)[0]], ' eliminated ////////////')
        players = np.delete(players, np.where(bankrupt)[0])
        if len(players) == 0:
            break
        wait()
    
print('###################################################################################')
print('################################## GAME OVER ######################################')