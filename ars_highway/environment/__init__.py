from gym.envs.registration import register

register(
    id='SumoEnv-v0',
    entry_point='environment.sumoEnv:SumoEnv',
)