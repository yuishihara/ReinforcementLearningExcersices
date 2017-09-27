import numpy as np


def policy(current_state, action):
  return 0.25


def is_end_state(state):
  x, y = index_of(state)
  if x == 0 and y == 0:
    return True
  elif x == 3 and y == 3:
    return True
  else:
    return False


def probability(current_state, action, next_state):
  index_x, index_y = index_after_move(current_state, action)
  next_x, next_y = index_of(next_state)

  if index_x == next_x and index_y == next_y:
    return 1
  else:
    return 0


def reward(current_state, action, next_state):
  index_x, index_y = index_after_move(current_state, action)
  next_x, next_y = index_of(next_state)

  if index_x == next_x and index_y == next_y:
    return -1
  else:
    return 0


def index_after_move(state, action):
  index_x, index_y = index_of(state)

  if action == 'up':
    index_y -= 1
  if action == 'down':
    index_y += 1
  if action == 'left':
    index_x -= 1
  if action == 'right':
    index_x += 1

  index_x = fit_index_in_map(index_x)
  index_y = fit_index_in_map(index_y)

  return index_x, index_y


def index_of(state):
  index_x = state % 4
  index_y = state / 4
  return index_x, index_y


def fit_index_in_map(index):
  if index < 0:
    return 0
  elif 3 < index:
    return 3
  return index


def value_iteration(states, value_func):
  actions = ['up', 'down', 'left', 'right']
  delta = 0
  new_value_func = np.copy(value_func)
  for current_state in states:
    current_x, current_y = index_of(current_state)
    value = value_func[current_x][current_y]

    new_value = 0
    for action in actions:
      expected_reward = 0.0
      for next_state in states:
        next_x, next_y = index_of(next_state)
        expected_reward += probability(current_state, action, next_state) \
            * (reward(current_state, action, next_state) + value_func[next_x][next_y])

      new_value += policy(current_state, action) * expected_reward

    if not is_end_state(current_state):
      new_value_func[current_x][current_y] = new_value
    delta = max(delta, np.absolute(value - delta))

  return new_value_func


def main():
  value_func = np.zeros((4, 4))
  states = range(16)

  for i in range(1000):
    value_func = value_iteration(states, value_func)

  print value_func


if __name__=='__main__':
  main()
