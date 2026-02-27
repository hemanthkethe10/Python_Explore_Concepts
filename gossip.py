import random
import time
from threading import Thread

class Node:
    def __init__(self, node_id, all_nodes):
        self.node_id = node_id
        self.all_nodes = all_nodes  # Reference to other nodes in the network
        self.data = None            # The information to spread
        self.active = True

    def receive_data(self, new_data):
        if self.data != new_data:
            print(f"Node {self.node_id} received news: {new_data}")
            self.data = new_data

    def start_gossiping(self):
        while self.active:
            # Only spread if we actually have information
            if self.data:
                # 1. Pick a random neighbor (excluding self)
                neighbor = random.choice([n for n in self.all_nodes if n.node_id != self.node_id])
                
                # 2. Push the data to the neighbor
                neighbor.receive_data(self.data)
            
            time.sleep(1) # Gossip interval

# --- Simulation ---
cluster_size = 5
nodes = []
for i in range(cluster_size):
    nodes.append(Node(i, nodes))

# Start the background threads for each node
for n in nodes:
    Thread(target=n.start_gossiping, daemon=True).start()

# Initially, only Node 0 knows the secret
nodes[0].receive_data("Update v2.1 is live!")

# Let it run for a few seconds to see the spread
time.sleep(5)