from PPO import PPO, Memory
from PIL import Image
import torch
from Env import UnityEnv
def test(env):
    ############## Hyperparameters ##############
    # creating environment

    state_dim = 11
    action_dim = 5

    n_latent_var = 128           # number of variables in hidden layer
    lr = 0.0007
    betas = (0.9, 0.999)
    gamma = 0.99                # discount factor
    K_epochs = 4                # update policy for K epochs
    eps_clip = 0.2              # clip parameter for PPO
    #############################################

    n_episodes = 15
    max_timesteps = 75


    filename = "PPO_{}.pth".format('bitirmeindep')
    directory = "./"
    
    memory = Memory()
    ppo = PPO(state_dim, action_dim, n_latent_var, lr, betas, gamma, K_epochs, eps_clip)
    
    ppo.policy_old.load_state_dict(torch.load(directory+filename))
    
    for ep in range(1, n_episodes+1):
        env.ResetUnity()
        state, _ , _ = env.GetState()
        episode_reward = 0
        for t in range(max_timesteps):
            action = ppo.policy_old.act(state, memory)
            env.PostAction(action)
            state, reward, done = env.GetState()
            ep_reward += reward
 
            if done:
                break
            
        print('Episode: {}\tReward: {}'.format(ep, int(ep_reward)))
        ep_reward = 0

if __name__ = '__main__':
    env = UnityEnv()
    test(env)

    
    
