# -*- coding: utf-8 -*-
import random
import gym
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense, Flatten, Activation
from keras.optimizers import Adam
import environment
import matplotlib.pyplot as plt

EPISODES = 1000
BATCH_SIZE = 32
MAX_STEPS = 100


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.8  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.990
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, episode, state, action, reward, next_state, done):
        self.memory.append((episode, state, action, reward, next_state, done))

    def act(self, state, use_epsilon=True):
        if np.random.rand() <= self.epsilon and use_epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for _, state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)


def trainOrTest(env, state_size, agent, batch_size, episodes, training):
    for e in range(episodes):
        state = env.reset()
        state = np.reshape(state, [1, state_size])
        for a in range(MAX_STEPS):
            action = agent.act(state, use_epsilon=training)
            next_state, reward, done, _ = env.step(action)
            reward = reward if not done else -10
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(e, state, action, reward, next_state, done)
            state = next_state
            if done:
                break
        total_reward = sum([x[3] for x in agent.memory if x[0] == e])
        print("episode: {}/{}, total reward:: {}, e: {:.2}"
              .format(e, episodes, total_reward, agent.epsilon))
        if len(agent.memory) > batch_size and training:
            agent.replay(batch_size)


if __name__ == "__main__":
    env = gym.make('SumoEnv-v0')
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)
    done = False

    env.log = False
    trainOrTest(env, state_size, agent, BATCH_SIZE, EPISODES, training=True)

    env.log = True
    env.test = True
    trainOrTest(env, state_size, agent, BATCH_SIZE, episodes=5, training=False)

    # plot the results.
    env.reset()
    leg = []
    i = 0
    for episode in env.result:
        plt.plot(episode)
        leg.append('episode %d' % i)
        i += 1

    plt.legend(leg, loc='upper left')
    plt.xlabel('Time (0.1s/step)')
    plt.ylabel('Speed (m/s)')

    plt.show()
