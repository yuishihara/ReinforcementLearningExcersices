import card
from card import Card
from random import shuffle
from collections import deque

class Deck:
  def __init__(self):
    self.__cards = self.build_deck()
    self.__top_index = 0
    assert len(self.__cards) == 52


  def draw_top(self):
    card = self.__cards[self.__top_index]
    self.__top_index += 1
    return card


  def reset(self):
    self.__top_index = 0
    shuffle(self.__cards)


  def build_deck(self):
    deck = []
    for suite in card.available_suites():
      for number in card.available_numbers():
        deck.append(Card(suite, number))

    shuffle(deck)
    return deck


  def print_deck(self):
    print("deck size: " + str(len(self.__cards)))
    for card in self.__cards:
      print(card)
