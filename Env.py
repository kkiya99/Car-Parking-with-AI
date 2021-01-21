import queue
import requests
import json
'''
0 - dummy
1 - ileri git
2 - geri git
3 - tekeri + 15 derece
4 - tekeri - 15 derece
5 - dur

'''
class Env:
    def __init__(self,timestep = 0, maxtimestep = 1000):
        self.state = queue.Queue(maxsize=1) 
        self.timestep = timestep
        self.maxtimestep = maxtimestep
        self.action_size = 5
        self.state_size = 11

    def GET_API(self):
        while True:
            if len(queue) == 0:
                #{"Sensors":[6,38,7,2,2,1,1,2],"Relative":[10,1],"Angle":-15}
                _r = requests.get("http://localhost:8084/api/State/GetState")
                data = _r.json()
                _state = data['Sensors'] + data['Relative']
                _state.append(data['Angle'])
                self.state.put(_state)

    def get_state(self):
        state = self.state.get()
        return state

    def act(self,action,state):
        reward = self.Reward(action,state)
        done = self.isDone(state)
        '''
        0 - ileri git
        1 - geri git
        2 - tekeri + 15 derece
        3 - tekeri - 15 derece
        4 - dur
        '''
        action = {'Action' : action}
        r = requests.post(url = "http://localhost:8084/api/Action/SetAction", data = action)

    def Reward(self,state,action):
        reward = -0.1
        ## yapilacaklar:
        # park yerinin kordinatlarini al ve parka ulasirsa odul ve reset (isDone'da yap)
        # araba carpinca hardcore ceza ve reset (isDone'da yap) (bunun icin unity'den veri gerekebilir)
        return reward
        
    def isDone(state):
        if self.timestep > self.maxtimestep:
            self.timestep = 0
            return 1
