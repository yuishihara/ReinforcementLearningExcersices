def available_suites():
  return [ "Spade", "Heart", "Diamond", "Club" ]


def available_numbers():
  return [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 ]


class Card:
  def __init__(self, suite, number):
    if suite not in available_suites():
      raise "Suite: " + str(suite) + " is not valid!"

    if number not in available_numbers():
      raise "Number: " + str(number) + " is not valid!"

    self.__suite = suite
    self.__number = number


  def __str__(self):
    return "suite: " + str(self.suite()) + ", number: " + str(self.number())


  def suite(self):
    return self.__suite


  def number(self):
    return self.__number


  def is_ace(self):
    return self.__number == 1
