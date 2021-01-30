import pygame
from random import randint
import numpy as np
import threading
from PPO import main
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
        self.px = randint(200,600)
        self.py = randint(200,600)
        self.tx = randint(100,700)
        self.ty = randint(100,700)
        self.speed = 10

    def Main(self):
        self.episode_t = 0
        self.winning = 0
        self.out = 0
        #Put all variables up here
        stopped = False
        font = pygame.font.SysFont(None, 28)
        while stopped == False:
            text = font.render("Episode: "+str(self.episode_t), True, (0, 128, 0))
            text2 = font.render("Win: "+str(self.winning), True, (0, 128, 0))
            #text3 = font.render("Out of Place: "+str(self.out), True, (0, 128, 0))
            window.fill((0,0,0)) #Tuple for filling display... Current is white
            window.blit(text,(0,0))
            window.blit(text2,(0,30))
            #window.blit(text3,(0,60))
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
            windowclock.tick(120)
    
    def step(self,action):
        if action == 0:
            if self.px + self.speed> 15: self.px -= self.speed
        elif action == 1:
            if self.px +50 + self.speed < 780: self.px += self.speed
        elif action == 2:
            if self.py + 50 + self.speed < 780: self.py += self.speed
        elif action == 3:
            if self.py + self.speed > 15: self.py -= self.speed
        state = self.get_state()
        done = self.isDone()
        if done == True:
            reward = 300
        else:
            reward = -0.1


     

        return [np.array(state), reward, done]

    def reset(self):
        self.episode_t += 1
        self.__init__()
        

    def get_state(self):
        state = np.array([self.px/1000,self.py/1000,(self.px-self.tx)/1000,(self.py-self.ty)/1000])
        return np.array(state)
    
    def isDone(self):
        if abs(self.px-self.tx) < 30 and abs(self.py-self.ty) < 30:
            self.winning += 1
            print('done true')
            return True
        else:
            return False


if __name__ == '__main__':

    env = MainRun()
    stateq.put(env.step(1))
    threading.Thread(target=main, args=(stateq, actionq, resetq,)).start()
    env.Main()
