from api import get_friends
import igraph
import numpy as np
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


def plot_graph(user_id):
    surnames = get_friends(user_id, 'last_name')
    vertices = [i['last_name'] for i in surnames]
    edges = get_network(user_id)

    gr = igraph.Graph(vertex_attrs={'shape': 'circle',
    	'label': vertices,
    	'size': 10},
    	edges=edges, directed=False)

    n = len(vertices)
    style = {
    	'vertex_size': 20,
    	'edge_color': 'gray',
    	'bbox':(2000, 2000),
    	'autocurve': True,
    	'vertex_label_dist': 1.6,
    	'margin': 100,
    	'layout': gr.layout_fruchterman_reingold(
    		maxiter=100000,
    		area=n ** 2,
    		repulserad=n ** 2)
    }

    gr.simplify(multiple=True, loops=True)
    clusters = gr.community_multilevel()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    gr.vs['color'] = pal.get_many(clusters.membership)

    igraph.plot(gr, **style)