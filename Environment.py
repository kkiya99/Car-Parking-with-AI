import queue
import requests
import json
import numpy as np
'''
        0 - ileri git   
        1 - geri git
        2 - tekeri + 5 derece
        3 - tekeri - 5 derece
        4 - dur
'''
class Env:
    def __init__(self,timestep = 0, maxtimestep = 1000):
        self.state = queue.Queue(maxsize=1) 
        self.action = queue.Queue(maxsize=1)
        global state_q
        state_q = self.action
        global action_q
        action_q = self.state
        self.timestep = timestep
        self.maxtimestep = maxtimestep
        self.action_size = 6 # 
        self.state_size = 11
        
        self.carpisma = False
        self.win = False

        self.episode_reward = 0
    # def GET_API(self):

    #     #{"Sensors":[6,38,7,2,2,1,1,2],"Relative":[10,1],"Angle":-15}
    #     _r = requests.get("http://localhost:8084/api/State/GetState")
    #     data = _r.json()
    #     _state = data['Sensors'] + data['Relative']
    #     _state.append(data['Angle'])
    #     print('State: ',_state)
    #     return _state

    def POST_API(self,action):

        print('Action: ',action)
        _r = requests.post(url = "http://localhost:8084/api/Action/SetAction", data = action)
        data = _r.json()
        _state = data['Sensors'] + data['Relative']
        _state.append(data['Angle'])
        print('State: ',_state)
        return np.array(_state)

    def reset(self):
        output = requests.post(url = "http://localhost:8084/api/reset", data = {'asd':'asd'})
        data = output.json()
        _state = data['Sensors'] + data['Relative']
        _state.append(data['Angle'])
        print('State: ',_state)
        return np.array(_state)

    def step(self,action,state):
        done = self.isDone(state)
        if done == True:self.save_reward_per_episode()
        reward = self.Reward(action,state)

        action = {'ActionNumber' : action,'Reset':done}
        next_state = self.POST_API(action)

        return next_state, reward, done
        
        
    def Reward(self,state,action):
        reward = -0.1
        if self.carpisma == True: reward += -100
        if self.win == True: reward += 100
        self.episode_reward += reward
        return reward


    def isDone(self,state):
        if self.timestep > self.maxtimestep:
            self.timestep = 0
            return True

        for i in state[:8]:
            if i < 0.51:
                self.carpirma = True
                return True
        
        ## 8-9 relative x -> 0.6
        if -0.5 <= state[8] <= 0.5 and -0.5 <= state[9] <= 0.5:
            self.win = True
            return True
        return False

    def save_reward_per_episode(self):
        _file = open('RPE.txt', 'a+')
        episode_reward = str(self.episode_reward)
        _file.write(episode_reward)
        _file.close()