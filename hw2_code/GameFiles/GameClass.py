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



    def tick_greedy(self, predicted_image, option, rewards):
        if option == "simple":
            action, vec = self.navigator.getgreedySimple(predicted_image)
        # action = self.navigator.getAction(self.robot,self.truthMap)
        if option == "bettergreedy":
            action = self.navigator.getgreedyMore(predicted_image)
        self.robot.move(action)
        if action is not None:
            rewards -= 1
        self.updateMap(self.robot,self.exploredMap,self.truthMap)
        # print("explored map",self.exploredMap[vec[0], vec[1]])
        if self.robot.getLoc() == self.goal:
            rewards += 100
            return True, rewards
        else:
            return False, rewards

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
                rewards += 100
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

