import queue
import requests
import json
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

    def GET_API(self):
        while True:
            if len(self.state_size) == 0:
                #{"Sensors":[6,38,7,2,2,1,1,2],"Relative":[10,1],"Angle":-15}
                _r = requests.get("http://localhost:8084/api/State/GetState")
                data = _r.json()
                _state = data['Sensors'] + data['Relative']
                _state.append(data['Angle'])
                self.state.put(_state)

    def POST_API(self):
        while True:
            action = self.action.get()
            requests.post(url = "http://localhost:8084/api/Action/SetAction", data = action)

    def get_state(self):
        state = self.state.get()
        return state

    def act(self,action,state):
        done = self.isDone(state)
        reward = self.Reward(action,state)

        action = {'ActionNumber' : action,'Reset':done}
        self.action.put(action)
        next_state = state
        return next_state, reward, done
        
        
    def Reward(self,state,action):
        reward = -0.1
        if self.carpisma == True: reward += -100
        if self.win == True: reward += 100
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

