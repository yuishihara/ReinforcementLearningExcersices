class Dealer:
  def __init__(self):
    self.__hand = None


  def select_action(self):
    if self.hand_total() < 17:
      return 1
    else:
      return 0


  def give_card(self, card):
    self.__hand.add_card(card)


  def revealed_card(self):
    cards = self.__hand.cards()
    return cards[0]


  def is_busted(self):
    return self.__hand.is_busted()


  def new_hand(self, hand):
    self.__hand = hand


  def hand(self):
    return self.__hand


  def hand_total(self):
    return self.__hand.total()
