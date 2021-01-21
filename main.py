from ddpg import DDPG as Agent
from Environment import Env

def loop(agent, env):
    try:
        state = env.get_state()
        action = agent.get_action(state)
        next_state, reward, done = env.act(action,state)
        agent.remember(state, action, reward, done, next_state)
        agent.train()
    except Exception as e:
        print(e)


def main():
    env = Env()
    agent = Agent(state_size=env.state_size, action_size=env.action_size)
    threading.Thread(target=env.GET_API, daemon=True).start()
    threading.Thread(target=env.POST_API, daemon=True).start()
    while True:
        loop(agent, env)


# GET_API
# POST_API