__author__ = 'Caleytown'
import numpy as np
import math

class Game:
    def __init__(self, map,goalLocation,navigator,robot):
        self.truthMap = map
        self.navigator = navigator
        self.robot = robot
        self.goal = goalLocation

        self.exploredMap = np.ones(map.shape)*128
        self.updateMap(self.robot,self.exploredMap,self.truthMap)



    def tick_greedy(self, predicted_image):
        # action = self.navigator.getAction(self.robot,self.truthMap)
        action = self.navigator.getgreedyAction(predicted_image)
        self.robot.move(action)
        self.updateMap(self.robot,self.exploredMap,self.truthMap)
        # if self.robot.getLoc() == self.goal:
        #     return True
        # else:
        #     return False

    def tick(self, robot_goal, prevLoc, rewards):
        action = self.navigator.getAction(robot_goal)
        # action = self.navigator.getgreedyAction(predicted_image)
        self.robot.move(action)
        # self.updateMap(self.robot,self.exploredMap,self.truthMap)
        currDist = self.navigator.distance(self.robot.getLoc(), self.goal)
        prevDist = self.navigator.distance(self.robot.getLoc(), self.goal)
        if currDist <= prevDist:
            rewards += 1
        else: 
            rewards -= 1
        if self.robot.getLoc() == robot_goal:
            if self.robot.getLoc() == self.goal:
                rewards += 400
                return True, rewards
            else:
                rewards -= 400
                return False, rewards
        else:
            return None, rewards


    def updateMap(self,robot, exploredMap, truthMap):
        for x in range(-1,2):
            for y in range(-1,2):
                if robot.getLoc()[0]+x > 27 or robot.getLoc()[0]+x < 0 or robot.getLoc()[1]+y > 27 or robot.getLoc()[1]+y < 0:
                    continue
                else:
                    exploredMap[robot.getLoc()[0]+x,robot.getLoc()[1]+y] = truthMap[robot.getLoc()[0]+x,robot.getLoc()[1]+y]

