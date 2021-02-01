import numpy as np
import time
import requests
## http://localhost:8084/api/ResetState/SetResetState -> POST 
## http://localhost:8084/api/Action/SetAction -> POST
## http://localhost:8084/api/State/GetState -> GET
## data = {"Sensors":[6.09172,37.62426,18.4938183,2.772441,3.32898784,2.41854715,2.77090549,2.22815466],"Relative":[9.956783,1.46001768],"Angle":0.0}
## data = {'ActionNumber':2}
#tensorboard --logdir=runs

class UnityEnv:
    def __init__(self):
        self.state_backup = None
    def PostAction(self,action):
        angle = self.state_backup['Angle']
        if (action == 2 and angle == 60) or (action == 3 and angle == -60):
            action = 4
        data = {'ActionNumber':action}
        time.sleep(0.01)
        r = requests.post(url = "http://localhost:8084/api/Action/SetAction", data = data)
        while r.status_code == 404:
                time.sleep(0.01)
                r = requests.post(url = "http://localhost:8084/api/Action/SetAction", data = data)
        
        return

    def GetState(self):
        try_get = True
        
        while try_get==True:
            time.sleep(0.01)
            _r = requests.get("http://localhost:8084/api/State/GetState")
            if _r.status_code != 404:
                data = _r.json()
                if data["Relative"][0] == 1000000 and  data["Relative"][1]== 1000000:
                     time.sleep(0.01)
                     continue
                else:
                    try_get = False
                    continue
            else:
                continue
        self.state_backup = data
        state = self.Normalize(data)
        reward = self.calcReward(data)
        done = self.isDone(data)
        if done == True: reward = 100
        return state, reward, done

    def ResetUnity(self):
        data = {'ResetState':'True'}
        time.sleep(0.01)
        _r_ = requests.put(url = "http://localhost:8084/api/ResetState/SetResetState", data = data)
        while _r_.status_code == 404:
            time.sleep(0.01)
            _r_ = requests.put(url = "http://localhost:8084/api/ResetState/SetResetState", data = data) 
        return 

    def calcReward(self,state):
        reward = -0.1
        for i in state['Sensors']:
            if i < 0.5:
                reward -= 10
        return reward
        

    def Normalize(self,data):
        ## data = {"Sensors":[6.09172,37.62426,18.4938183,2.772441,3.32898784,2.41854715,2.77090549,2.22815466],"Relative":[9.956783,1.46001768],"Angle":0.0}
        state = [ ]
        for i in data['Sensors']:
            state.append(i/100)
        for i in data['Relative']:
            state.append(i/15)
        state.append(data['Angle']/60)
        return np.array(state)
    
    def isDone(self,data):
        if -0.5 <= data['Relative'][0] <= 0.5 and -0.5 <= data['Relative'][1] <= 0.5:
            return True
        return False

