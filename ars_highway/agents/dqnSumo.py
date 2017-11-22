import gym
import numpy as np
from keras.layers import Dense, Activation, Flatten
from keras.models import Sequential
from keras.optimizers import Adam
from rl.agents.dqn import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import BoltzmannQPolicy
import matplotlib.pyplot as plt
import environment

ENV_NAME = 'SumoEnv-v0'

#Training vars
WARMUP_STEPS = 50000
TRAIN_STEPS = 25000
TOTAL_STEPS = WARMUP_STEPS + TRAIN_STEPS

MAX_STEPS_TRAIN = 10000
MAX_STEPS_TEST = 2000

# Get the environment and extract the number of actions.
env = gym.make(ENV_NAME)
np.random.seed(123)
env.seed(123)
nb_actions = env.action_space.n

# Next, we build a very simple model.
model = Sequential()
model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('linear'))
print(model.summary())

# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
# even the metrics!
memory = SequentialMemory(limit=50000, window_length=1)
policy = BoltzmannQPolicy()
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, gamma=0.9, nb_steps_warmup=WARMUP_STEPS,
               target_model_update=1e-2, policy=policy)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])

# Okay, now it's time to learn something! We visualize the training here for show, but this
# slows down training quite a lot. You can always safely abort the training prematurely using
# Ctrl + C.
env.log = False
dqn.fit(env, nb_steps=TOTAL_STEPS, visualize=True, verbose=2, nb_max_episode_steps=MAX_STEPS_TRAIN)

# After training is done, we save the final weights.
#dqn.save_weights('dqn_{}_weights.h5f'.format(ENV_NAME), overwrite=True)

# Finally, evaluate our algorithm for 5 episodes.
env.num_test_episodes = 5
env.log = True
env.test = True
dqn.test(env, nb_episodes=env.num_test_episodes, visualize=True, nb_max_episode_steps=MAX_STEPS_TEST)
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