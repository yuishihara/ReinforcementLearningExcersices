import numpy as np
import random
from gridworld import GridWorld

EPSILON = 0.1
ALPHA = 0.1

def select_action(q_table, state, available_actions, epsilon):
  index = 0
  if random.uniform(0.0, 1.0) <= epsilon:
    index = random.randint(0, len(available_actions) - 1)
  else:
    index = np.argmax(q_table[:, state[1], state[0]])
  return available_actions[index]


def update_q_table(table, available_actions,
    current_state, next_state,
    current_action, next_action, reward):
  current_action_index = available_actions.index(current_action)
  next_action_index = available_actions.index(next_action)

  current_q = table[current_action_index, current_state[1], current_state[0]]
  next_q = table[next_action_index, next_state[1], next_state[0]]
  new_q = current_q + ALPHA * (reward + next_q - current_q)
  table[current_action_index, current_state[1], current_state[0]] = new_q
  return table


def play_one_episode(world, q_table, initial_state, initial_action, initial_steps, epsilon, update_table=True):
  available_actions = world.available_actions()
  steps = initial_steps
  selected_actions = []
  current_state = initial_state
  current_action = initial_action
  while not world.end_state(current_state):
    reward, next_state = world.act(current_state, current_action)
    next_action = select_action(q_table, next_state, available_actions, epsilon / (steps + 1))
    if update_table:
      q_table = update_q_table(q_table, available_actions,
          current_state, next_state,
          current_action, next_action, reward)
    selected_actions.append(current_action)
    steps = steps + 1
    current_state = next_state
    current_action = next_action
  return q_table, steps, selected_actions


def train(world, q_table):
  available_actions = world.available_actions()
  MAX_EPISODES = 2000
  steps = 0
  for episode in range(MAX_EPISODES):
    initial_state = (0, 3)
    initial_action = select_action(q_table, initial_state, available_actions, EPSILON)
    q_table, steps, _ = play_one_episode(world, q_table, initial_state, initial_action, steps, EPSILON)
  print 'Learning finished! steps = ' + str(steps)
  return q_table


def evaluate(world, q_table):
  available_actions = world.available_actions()
  initial_state = (0, 3)
  initial_action = select_action(q_table, initial_state, available_actions, 0.0)
  _, steps, actions = play_one_episode(world, q_table, initial_state, initial_action, 0, 0.0, update_table = False)

  moves = [world.action_to_str(action) for action in actions]
  return moves


def main():
  world = GridWorld()
  q_table = np.zeros([len(world.available_actions()), 7, 10])
  q_table = train(world, q_table)
  moves = evaluate(world, q_table)
  print 'Moves: ' + str(moves)
  print 'Steps: ' + str(len(moves))


if __name__=='__main__':
  main()
