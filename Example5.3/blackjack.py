from deck import Deck
from dealer import Dealer
from player import Player
from hand import Hand
import matplotlib.pyplot as plt
import numpy as np


def play_one_game(black_jack_deck, dealer, player):
  player_hand = make_hand(black_jack_deck)
  player.new_hand(player_hand)

  dealer_hand = make_hand(black_jack_deck)
  dealer.new_hand(dealer_hand)

  revealed_card = dealer.revealed_card()

  while not player.is_busted() and player.select_action(revealed_card) == 1:
    new_card = black_jack_deck.draw_top()
    player.give_card(new_card)

  if player.is_busted():
    return -1

  while not dealer.is_busted() and dealer.select_action() == 1:
    new_card = black_jack_deck.draw_top()
    dealer.give_card(new_card)

  if dealer.is_busted():
    return 1
  if player.hand_total() == dealer.hand_total():
    return 0
  if player.hand_total() < dealer.hand_total():
    return -1
  if player.hand_total() > dealer.hand_total():
    return 1


def make_hand(black_jack_deck):
  cards = [ black_jack_deck.draw_top() for i in range(2) ]
  return Hand(cards)


def print_average_rewards(policy):
  dealer_possible_hands = 10
  for dealer_index in range(dealer_possible_hands):
    string = 'dealer ' + str(dealer_index + 1) + " "
    for hand_number in range(12, 22):
      hand_index = hand_number - 12
      stick = policy[dealer_index][hand_index][0]
      hit = policy[dealer_index][hand_index][1]
      string += '{0:.2f}.'.format(hit) + '/' + '{0:.2f}.'.format(stick) + ' '
    print(string)


def print_optimal_actions(policy):
  dealer_possible_hands = 10
  for dealer_index in range(dealer_possible_hands):
    string = 'dealer ' + str(dealer_index + 1) + " "
    for hand_number in range(12, 22):
      hand_index = hand_number - 12
      action = 'hit' if np.argmax(policy[dealer_index][hand_index]) == 1 else 'stick'
      string += action + ' '
    print(string)


def compute_border(policy):
  dealer_possible_hands = 10
  border = np.zeros(dealer_possible_hands)
  for dealer_index in range(dealer_possible_hands):
    for hand_number in range(12, 22):
      hand_index = hand_number - 12
      if np.argmax(policy[dealer_index][hand_index]) == 0:
        border[dealer_index] = hand_number - 1
        break
  return border


def plot_border(border, rows, columns, index, title):
  plt.subplot(rows, columns, index)
  plt.plot(border, drawstyle='steps-post')
  x_range = [i for i in range(10)]
  x_labels = [i for i in range(1, 11)]
  plt.xticks(x_range, x_labels)
  plt.title(title)
  plt.axis([0, 9, 11, 22])


def main():
  max_loops = 1000000
  trials = 0
  dealer = Dealer()
  player = Player()
  black_jack_deck = Deck()

  while trials < max_loops:
    reward = play_one_game(black_jack_deck, dealer, player)
    black_jack_deck.reset()
    player.give_reward(reward)
    trials += 1

    if trials % 100000 == 0:
      policy_with_ace, policy_without_ace = player.current_policy()

      print('trials : ' + str(trials))
      print('with ace h/s')
      print_average_rewards(policy_with_ace)
      print_optimal_actions(policy_with_ace)

      print('without ace h/s')
      print_average_rewards(policy_without_ace)
      print_optimal_actions(policy_without_ace)

  policy_with_ace, policy_without_ace = player.current_policy()
  with_ace = compute_border(policy_with_ace)
  without_ace = compute_border(policy_without_ace)

  rows = 2
  columns = 1
  index = 1
  for border, title in [(with_ace, "with ace"), (without_ace, "without ace")]:
    plot_border(border, rows, columns, index, title)
    index += 1

  plt.show()

if __name__=="__main__":
  main()
