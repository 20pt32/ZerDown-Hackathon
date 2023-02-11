import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import psycopg2

conn = psycopg2.connect(database="postgres", user="postgres", password="sivapriya", host= "127.0.0.1" , port= "5432")
cursor = conn.cursor()

def get_relationships(market_id):
    cursor.execute("SELECT agent1, agent2 FROM relationships WHERE market_id = %s", (market_id,))
    return cursor.fetchall()


def plot_relationships(market_id):
    relationships = get_relationships(market_id)

    # Plot the relationships using matplotlib
    plt.scatter([r[0] for r in relationships], [r[1] for r in relationships])
    plt.show()


root = tk.Tk()
root.title("Top Agents and Brokerages")

market_id_label = ttk.Label(root, text="Market ID:")
market_id_label.grid(row=0, column=0)

market_id_entry = ttk.Entry(root)
market_id_entry.grid(row=0, column=1)

plot_button = ttk.Button(root, text="Plot Graph", command=lambda: plot_relationships(market_id_entry.get()))
plot_button.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()
