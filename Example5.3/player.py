import numpy as np
import random
from copy import deepcopy

class Player:
  def __init__(self):
    self.__hand = None
    self.__policy_with_ace = np.zeros((10, 10, 2))
    self.__policy_without_ace = np.zeros((10, 10, 2))
    self.__rewards_with_ace = [[[[] for i in range(2)] for j in range(10)] for k in range(10)]
    self.__rewards_without_ace = [[[[] for i in range(2)] for j in range(10)] for k in range(10)]
    self.__sequence = None


  def give_card(self, card):
    self.__hand.add_card(card)


  def select_action(self, dealer_card):
    hand_total = self.hand_total()
    if hand_total <= 11:
      return 1

    if len(self.__sequence) == 0:
      # Select random action to satisfy exploring all possible states
      action = random.choice([0, 1])
    else:
      dealer_number = min(10, dealer_card.number())
      dealer_index = dealer_number - 1
      hand_index = hand_total - 12
      action = 0
      if self.__hand.has_available_ace():
        action = np.argmax(self.__policy_with_ace[dealer_index][hand_index])
      else:
        action = np.argmax(self.__policy_without_ace[dealer_index][hand_index])
    self.__sequence.append((deepcopy(self.__hand), dealer_card, action))
    assert action == 0 or action == 1
    return action


  def give_reward(self, reward):
    self.update_policy(reward)


  def update_policy(self, reward):
    for hand, dealer_card, action in self.__sequence:
      dealer_number = min(10, dealer_card.number())
      dealer_index = dealer_number - 1
      hand_index = hand.total() - 12
      if hand.has_available_ace():
        self.__rewards_with_ace[dealer_index][hand_index][action].append(reward)
        avg = np.average(self.__rewards_with_ace[dealer_index][hand_index][action])
        self.__policy_with_ace[dealer_index][hand_index][action] = avg
      else:
        self.__rewards_without_ace[dealer_index][hand_index][action].append(reward)
        avg = np.average(self.__rewards_without_ace[dealer_index][hand_index][action])
        self.__policy_without_ace[dealer_index][hand_index][action] = avg


  def is_busted(self):
    return self.__hand.is_busted()


  def current_policy(self):
    return self.__policy_with_ace, self.__policy_without_ace


  def new_hand(self, hand):
    self.__hand = hand
    self.__sequence = []


  def hand(self):
    return self.__hand


  def hand_total(self):
    return self.__hand.total()
