import pygame
from random import randint
import numpy as np
import threading
from test import test
pygame.init()

# Window Information
displayw = 800
displayh = 800
window = pygame.display.set_mode((displayw,displayh))

# Clock
windowclock = pygame.time.Clock()
import queue
global stateq, actionq, resetq
stateq = queue.Queue(maxsize=1) 
actionq = queue.Queue(maxsize=1)
resetq = queue.Queue(maxsize=1)
# Main Class
class MainRun(object):
    def __init__(self):
        self.px = randint(300,600)
        self.py = randint(300,600)
        self.tx = randint(50,300)
        self.ty = randint(50,300)
        self.speed = 8


    def Main(self):
        #Put all variables up here
        stopped = False

        while stopped == False:
            window.fill((0,0,0)) #Tuple for filling display... Current is white
            if resetq.empty():
                pass
            else:
                resetq.get( )
                self.reset()
                if stateq.empty():
                    stateq.put(env.step(1))
                else:
                    stateq.get()
                    stateq.put(env.step(1))


            actio = actionq.get()
            print('Action: ',actio)
            asd = self.step(actio)
            print('state: ',asd)
            stateq.put(asd)
            pygame.draw.rect(window,(250,0,0),(self.px,self.py,50,50))
            pygame.draw.rect(window,(250,250,250),(self.tx,self.ty,5,5))
            #Event Tasking
            #Addthreading.Thread(target=env.GET_API, daemon=True).start() all your event tasking things here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    stopped = True

            #Add things like player updates here
            #Also things like score updates or drawing additional items
            # Remember things on top get done first so they will update in the order yours is set at

            # Remember to update your clock and display at the end
            pygame.display.update()
            windowclock.tick(60)
    
    def step(self,action):
        if action == 0:
            self.px -= self.speed
        elif action == 1:
            self.px += self.speed
        elif action == 2:
            self.py += self.speed
        elif action == 3:
            self.py -= self.speed
        state = self.get_state()
        done = self.isDone()
        if done == True:
            reward = 100
        else:
            reward = -0.1
        if self.px > 850 or self.px < 10 or self.py < 10 or self.py> 780:
            done = True
            reward = -100
        return [np.array(state), reward, done]

    def reset(self):
        self.__init__()
        

    def get_state(self):
        state = np.array([self.px/800,self.py/800,(self.px-self.tx)/800,(self.py-self.ty)/800])
        return np.array(state)
    
    def isDone(self):
        if abs(self.px-self.tx) < 10 and abs(self.py-self.ty) < 10:
            print('done true')
            return True
        else:
            return False


if __name__ == '__main__':

    env = MainRun()
    stateq.put(env.step(1))
    threading.Thread(target=test, args=(stateq, actionq, resetq,)).start()
    env.Main()