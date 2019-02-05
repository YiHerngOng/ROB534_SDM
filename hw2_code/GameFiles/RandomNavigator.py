__author__ = 'Caleytown'
import numpy as np
from random import randint

class RandomNavigator:
    #def __init__(self):


    def getAction(self,robot,map):
        randNumb = randint(0,3)
        if randNumb == 0:
            if robot.getLoc()[0]-1 < 0:
                randNumb = randNumb + 1
            else:
                return 'left'
        if randNumb == 1:
            if robot.getLoc()[0]+1 > 27:
                randNumb = randNumb + 1
            else:
                return 'right'
        if randNumb == 2:
            if robot.getLoc()[1]+1 > 27:
                randNumb = randNumb + 1
            else:
                return 'down'
        if randNumb == 3:
            if robot.getLoc()[1]-1 < 0:
                randNumb = 0
            else:
                return 'up'