class Hand:
  def __init__(self, cards):
    assert len(cards) == 2
    self.__cards = cards


  def __str__(self):
    string = 'total: ' + str(self.total()) + ' '
    for card in self.cards():
      string += str(card)
      string += ' '
    return string


  def add_card(self, card):
    self.__cards.append(card)


  def cards(self):
    return self.__cards


  def has_available_ace(self):
    aces = [ card for card in self.__cards if card.is_ace() ]
    if len(aces) == 0:
      return False

    other_than_ace = [ card for card in self.__cards if not card.is_ace() ]
    total_sum_other_than_ace = self.sum_cards(other_than_ace)

    return total_sum_other_than_ace <= (11 - len(aces))


  def total(self):
    return self.sum_cards(self.__cards)


  def is_busted(self):
    return 21 < self.total()


  def sum_cards(self, cards):
    aces = [ card for card in cards if card.is_ace() ]
    other_than_ace = [ card for card in cards if not card.is_ace() ]

    total = 0
    for card in other_than_ace:
      number = card.number()
      if 10 <= number and number <= 13:
        total += 10
      else:
        total += number

    for card in aces:
      number = card.number()
      if (total + 11) <= 21:
        total += 11
      else:
        total += number

    return total
