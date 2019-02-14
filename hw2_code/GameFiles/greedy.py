#!/usr/bin/env python3
'''
Author: Yi Herng Ong
Description: greedy algorithm that search an optimal path for robot to travel
'''

import os, sys
import numpy as np
from PIL import Image
from RobotClass import Robot
from GameClass import Game
from RandomNavigator import RandomNavigator
from networkFolder.functionList import Map,WorldEstimatingNetwork,DigitClassifcationNetwork
import pdb
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import random

class greedy():
	def __init__(self, robot):
		self.robot = robot
		self.visited = []

	def getgreedyMore(self, predicted_image):
		robotLoc = np.array([self.robot.getLoc()[0], self.robot.getLoc()[1]])
		# pdb.set_trace()
		max_pixel_index = np.where(predicted_image == np.amax(predicted_image))
		max_pixel_vector = np.array([max_pixel_index[0][0], max_pixel_index[1][0]])
		print("vector",max_pixel_vector)
		print("robot",robotLoc)
		print("max pixel",np.amax(predicted_image))
		action = self.get_direction(robotLoc, max_pixel_vector)
		print("action", action)
		return action


	def getgreedySimple(self, predicted_image):
		robotLoc = np.array([self.robot.getLoc()[0], self.robot.getLoc()[1]])
		self.visited.append(list(robotLoc))
		# print("visited neighbours", self.visited)
		neighbours = self.get_neighbours(robotLoc)
		print("neighbours", neighbours)
		neighbours_pixel =[]
		# pdb.set_trace()
		for i in range(len(neighbours)):
			# print(neighbours[i][0], neighbours[i][1])
			if neighbours[i] in self.visited:
				print("visited neighbours", neighbours[i])
				continue
			else:
				neighbours_pixel.append(predicted_image[neighbours[i][0], neighbours[i][1]])
		max_neighbour_pixel = self.get_maxPixel(neighbours_pixel)
		# pdb.set_trace()

		print("pixels",neighbours_pixel)
		max_neighbour_index = neighbours_pixel.index(max_neighbour_pixel)
		try:
			action = self.get_direction(robotLoc, neighbours[max_neighbour_index])
		except:
			pdb.set_trace()
		print("vector", max_neighbour_index)
		return action, neighbours[max_neighbour_index]

	def distance(self, a, b):
		return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

	def get_maxPixel(self,neighbours_pixel):
		if len(neighbours_pixel) > 1:
			if neighbours_pixel[1:] == neighbours_pixel[:-1]:
				num = random.randint(0, len(neighbours_pixel)-1)
				return neighbours_pixel[num]
			else:
				return max(neighbours_pixel)
		else:
			try:
				return neighbours_pixel[0]
			except:
				pdb.set_trace()


	def getAction(self, goal):
		robotLoc = np.array([self.robot.getLoc()[0], self.robot.getLoc()[1]])
		return self.get_direction(robotLoc, goal)

	def get_neighbours(self, robotLoc):
		neighbours = []
		for x in range(-1,2):
			for y in range(-1,2):
				if robotLoc[0] + x > 27 or robotLoc[0] + x < 0 or robotLoc[1] + y > 27 or robotLoc[1] + y < 0:
					continue
				if robotLoc[0] + x == robotLoc[0] and robotLoc[1] + y == robotLoc[1]:
					continue
				neighbours.append([robotLoc[0]+x, robotLoc[1]+y])
		return neighbours		

	def get_direction(self, robotLoc, goal):
		if abs(goal[0] -robotLoc[0]) > abs(goal[1] - robotLoc[1]) and (goal[0] >= robotLoc[0]):
			return 'right'
		if abs(goal[0] -robotLoc[0]) > abs(goal[1] - robotLoc[1]) and (goal[0] <= robotLoc[0]):
			return 'left'
		if abs(goal[0] -robotLoc[0]) < abs(goal[1] - robotLoc[1]) and (goal[1] >= robotLoc[1]):
			return 'down'
		if abs(goal[0] -robotLoc[0]) < abs(goal[1] - robotLoc[1]) and (goal[1] <= robotLoc[1]):
			return 'up'
		if abs(goal[0] -robotLoc[0]) == abs(goal[1] - robotLoc[1]):
			if (goal[0] >= robotLoc[0]) and (goal[1] >= robotLoc[1]):
				where = random.randint(0,1)
				if where == 0:
					return 'right'
				else:
					return 'down'
		if abs(goal[0] -robotLoc[0]) == abs(goal[1] - robotLoc[1]):
			if (goal[0] <= robotLoc[0]) and (goal[1] >= robotLoc[1]):
				where = random.randint(0,1)
				if where == 0:
					return 'left'
				else:
					return 'down'
		if abs(goal[0] -robotLoc[0]) == abs(goal[1] - robotLoc[1]):
			if (goal[0] >= robotLoc[0]) and (goal[1] <= robotLoc[1]):
				where = random.randint(0,1)
				if where == 0:
					return 'right'
				else:
					return 'up'
		if abs(goal[0] -robotLoc[0]) == abs(goal[1] - robotLoc[1]):
			if (goal[0] <= robotLoc[0]) and (goal[1] <= robotLoc[1]):
				where = random.randint(0,1)
				if where == 0:
					return 'left'
				else:
					return 'up'
				


def get_goal(map_number):
	if map_number >= 0 and map_number <= 2:
		return (0,27)
	if map_number >= 3 and map_number <= 5:
		return (27,27)
	if map_number >= 6 and map_number <= 9:
		return (27,0)


def calc_prob(char):
	arr = []
	for i in char[0]:
		p = math.exp(i)
		arr.append(p)
	# pdb.set_trace()

	highest = max(arr)
	return highest / sum(arr)

def main():
	# nums = np.arange(0,10)
	# for i in nums:
	# print("current img num", i)
	option = "simple"
	M = Map(0)
	data = M.map
	robot = Robot(0,0)
	navigator = greedy(robot)
	real_goal = get_goal(M.number)
	game = Game(data,real_goal,navigator,robot)
	print("actual goal",real_goal)
	print("actual number:", M.number)
	# pdb.set_trace()
	# define networks
	wEstNet = WorldEstimatingNetwork()
	classNet = DigitClassifcationNetwork()
	mask = np.zeros((28,28))
	path_taken = np.zeros((28,28))
	rewards = 0
	while True:
		path_taken[robot.getLoc()[0], robot.getLoc()[1]] = 1 # record path being taken by robot
		for x in range(0,28):
			for y in range(0,28):
				if game.exploredMap[x,y] != 128:
					mask[x,y] = 1
		image = wEstNet.runNetwork(game.exploredMap,mask)
		char = classNet.runNetwork(image) # softmax output values
		prob = calc_prob(char)
		print("prob:", prob)
		print("current prediction",char.argmax())
		if prob > 0.95:
			break
		new_image = (image * (1 - mask))
		# print("mask", mask[22,17])
		# pdb.set_trace()
		run, rewards = game.tick_greedy(new_image, option, rewards)
		if run  == True:
			break
	# print(char)
	# print(char.argmax())
	# Image.fromarray(image).show()
	# a = plt.imshow(image)
	# plt.show()
	# print(mask)
	# pdb.set_trace()
	print("robot finds path")
	robot_goal = get_goal(char.argmax())

	prevLoc = np.array([robot.getLoc()[0], robot.getLoc()[1]])
	while True:
		check_goal, rewards = game.tick(robot_goal, prevLoc, rewards)
		if check_goal == True:
			print("prediction is right")
			print("rewards", rewards)
			break
		if check_goal == False:
			flag = 1
			print("rewards", rewards)
			print("WRONG DESTINATION")

		# check if robot is moving towards the right goal
		prevLoc = np.array([robot.getLoc()[0], robot.getLoc()[1]])
		# pdb.set_trace()







if __name__ == '__main__':
	main()
