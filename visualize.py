import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt

import psycopg2

conn = psycopg2.connect(
    host="127.0.0.1",
    database="postgres",
    user="postgres",
    password="sivapriya"
)

cur = conn.cursor()

cur.execute("SELECT * FROM agent_relationship_graph")

rows = cur.fetchall()

G = nx.Graph()

for row in rows:
    agent_a_id, agent_b_id = row
    G.add_edge(agent_a_id, agent_b_id)

def visualize_graph():
    nx.draw(G, with_labels=True)
    plt.show()

root = tk.Tk()

button = tk.Button(root, text="Visualize graph", command=visualize_graph)
button.pack()

root.mainloop()
