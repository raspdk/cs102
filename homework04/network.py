from api import get_friends
'''import igraph
import numpy as np'''
import time


def get_network(users_ids, as_edgelist=True):
	i = 0
	friend_list = get_friends(users_ids)
	edges = []
	matrix = [[0] * len(friend_list)] * len(friend_list)
	for friend1 in range(len(friend_list)):
		i += 1
		frs = get_friends(friend_list[friend1])
		for friend2 in range(friend1 + 1, len(friend_list)):
			if friend_list[friend2] in frs:
				if as_edgelist:
					edges.append((friend1, friend2))
				else:
					matrix[friend1][friend2] = 1
					matrix[friend2][friend1] = 1
		if i == 3:
			time.sleep(1)
			i = 0
	if as_edgelist:
		return edges
	else:
		return matrix


'''def plot_graph(graph):
    # PUT YOUR CODE HERE'''