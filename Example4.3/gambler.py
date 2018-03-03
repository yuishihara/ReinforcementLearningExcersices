import numpy as np
import matplotlib.pyplot as plt


def reward(prev_state, next_state):
  if 100 <= next_state:
    return 1.0
  else:
    return 0.0


def compute_value(state, action, state_values, transition_probability):
  gamma = 1.0
  pnext = state + action
  nnext = state - action
  assert 0 <= nnext and pnext <= 100

  return transition_probability * (reward(state, pnext) + gamma * state_values[pnext]) \
      + (1.0 - transition_probability) * (reward(state, nnext) + gamma * state_values[nnext])


def value_iteration(transition_probability):
  state_values = np.zeros(101)
  threshold = 1e-20
  max_sweep = 32
  sweep = 0

  while True:
    delta = 0.0
    for state in range(len(state_values)):
      if state == 0 or state == 100:
        continue
      max_state_value = 0.0
      for action in range(min(state, 100 - state)):
        action = action + 1
        # print("state: " + str(state) + " action: " + str(action))
        state_value = compute_value(state, action, state_values, transition_probability)
        if max_state_value < state_value:
          max_state_value = state_value
      prev_value = state_values[state]
      state_values[state] = max_state_value
      delta = max(abs(prev_value - max_state_value), delta)
    sweep = sweep + 1
    if max_sweep < sweep:
      break
  return state_values


def compute_policy(state_values, transition_probability):
  policy = np.zeros(len(state_values))
  for state in range(len(state_values)):
    if state == 0 or state == 100:
        continue
    max_state_value = 0.0
    for action in range(min(state, 100 - state)):
      action = action + 1
      state_value = compute_value(state, action, state_values, transition_probability)
      if 1e-5 < abs(max_state_value - state_value) and max_state_value < state_value:
        max_state_value = state_value
        policy[state] = action
  return policy


def state_values_and_policy_for(transition_probability):
  state_values = value_iteration(transition_probability)
  policy = compute_policy(state_values, transition_probability)
  return state_values, policy


def main():
  probabilities = [ 0.4, 0.25, 0.55 ]
  value_function = []
  policy_function = []

  for probability in probabilities:
    values, policy = state_values_and_policy_for(probability)
    value_function.append(values)
    policy_function.append(policy)

  index = 1
  rows = 2
  columns = len(probabilities)
  for probability, values, policy in zip(probabilities, value_function, policy_function):
    # Value function
    plt.subplot(rows, columns, index)
    plt.plot(range(1, len(values) - 1), values[1:100])
    plt.title("value_func prob: " + str(probability))

    # Policy function
    plt.subplot(rows, columns, index + columns)
    plt.step(range(1, len(policy) - 1), policy[1:100])
    plt.title("policy_func prob: " + str(probability))

    index += 1

  plt.show()

if __name__=='__main__':
  main()
