from environment import Environment

class GridWorld(Environment):
  __UP = 1
  __DOWN = 2
  __LEFT = 3
  __RIGHT = 4
  __UP_RIGHT = 5
  __DOWN_RIGHT = 6
  __UP_LEFT = 7
  __DOWN_LEFT = 8
  __NO_MOVE = 9

  __WIDTH = 10
  __HEIGHT = 7

  def __init__(self):
    pass


  def act(self, state, action):
    x, y = self.__position_of(state)
    assert 0 <= x and x < GridWorld.__WIDTH
    assert 0 <= y and y < GridWorld.__HEIGHT

    move = self.__compute_move(action)
    wind = self.__compute_wind(state)

    candidate_state = (x + move[0] + wind[0], y + move[1] + wind[1])
    next_state = self.__fit_in_world(candidate_state)
    reward = 0 if self.end_state(next_state) else -1
    return reward, next_state


  def end_state(self, state):
    x, y = self.__position_of(state)
    return (x == 7) and (y == 3)


  def reset(self):
    pass


  def available_actions(self):
    return [GridWorld.__UP, GridWorld.__DOWN, GridWorld.__LEFT, GridWorld.__RIGHT, GridWorld.__UP_RIGHT, GridWorld.__DOWN_RIGHT, GridWorld.__UP_LEFT, GridWorld.__DOWN_LEFT, GridWorld.__NO_MOVE]


  def action_to_str(self, action):
    if action == GridWorld.__UP:
      return 'UP'
    elif action == GridWorld.__DOWN:
      return 'DOWN'
    elif action == GridWorld.__RIGHT:
      return 'RIGHT'
    elif action == GridWorld.__LEFT:
      return 'LEFT'
    elif action == GridWorld.__UP_RIGHT:
      return 'UP RIGHT'
    elif action == GridWorld.__DOWN_RIGHT:
      return 'DOWN RIGHT'
    elif action == GridWorld.__UP_LEFT:
      return 'UP LEFT'
    elif action == GridWorld._DOWN_LEFT:
      return 'DOWN LEFT'
    elif action == GridWorld.__NO_MOVE:
      return 'NO MOVE'
    else:
      return 'UNKNOWN'


  def __position_of(self, state):
    return state[0], state[1]


  def __compute_move(self, action):
    if action == GridWorld.__UP:
      return (0, 1)
    elif action == GridWorld.__DOWN:
      return (0, -1)
    elif action == GridWorld.__RIGHT:
      return (1, 0)
    elif action == GridWorld.__LEFT:
      return (-1, 0)
    elif action == GridWorld.__UP_RIGHT:
      return (1, 1)
    elif action == GridWorld.__DOWN_RIGHT:
      return (1, -1)
    elif action == GridWorld.__UP_LEFT:
      return (-1, 1)
    elif action == GridWorld.__DOWN_LEFT:
      return (-1, -1)
    elif action == GridWorld.__NO_MOVE:
      return (0, 0)
    else:
      assert False


  def __compute_wind(self, state):
    x, y = self.__position_of(state)
    if 3 <= x and x <= 5:
      return (0, 1)
    elif 6 <= x and x <= 7:
      return (0, 2)
    elif x == 8:
      return (0, 1)
    else:
      return (0, 0)


  def __fit_in_world(self, state):
    x, y = self.__position_of(state)
    if x < 0:
      x = 0
    elif GridWorld.__WIDTH <= x:
      x = GridWorld.__WIDTH - 1

    if y < 0:
      y = 0
    elif GridWorld.__HEIGHT <= y:
      y = GridWorld.__HEIGHT - 1

    return (x, y)
