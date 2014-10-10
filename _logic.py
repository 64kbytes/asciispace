import matplotlib.pyplot as plt
from tech.spacecrafts import *

def showSystems(ship):
		
		G = nx.compose(ship.electricalSystem, ship.dataSystem)
		
		"""
		pos=nx.circular_layout(G)

		plt.subplot(111)
		nx.draw(G, pos, font_size = 8)
		
		nx.write_graphml(G,'so.graphml')
		"""
		
		pos = nx.spring_layout(G)
		
		"""
		node_labels = nx.get_node_attributes(G,'data')
		nx.draw_networkx_labels(G, pos, labels = node_labels)
		edge_labels = nx.get_edge_attributes(G,'data')
		nx.draw_networkx_edge_labels(G, pos, labels = edge_labels)
		"""
		
		nx.draw(G, pos)

		plt.suptitle(ship.label)
		plt.show()


shipA = Spacecraft.create()
#showSystems(shipA)

shipA.electricalSystem.cycle()
