import tkinter as tk
from tkinter import ttk
import psycopg2

conn = psycopg2.connect(database="postgres", user="postgres", password="sivapriya", host= "127.0.0.1" , port= "5432")
cursor = conn.cursor()


def get_top_agents(market_id, n):
    cursor.execute("SELECT agent_id, name, sales FROM agent_info WHERE market_id = %s ORDER BY sales DESC LIMIT %s",
                   (market_id, n))
    return cursor.fetchall()


def get_top_brokerages(market_id, n):
    cursor.execute("SELECT brokerage_id, name, sales FROM brokerage WHERE market_id = %s ORDER BY sales DESC LIMIT %s",
                   (market_id, n))
    return cursor.fetchall()


root = tk.Tk()
root.title("Top Agents and Brokerages")

market_id_label = ttk.Label(root, text="Market ID:")
market_id_label.grid(row=0, column=0)

market_id_entry = ttk.Entry(root)
market_id_entry.grid(row=0, column=1)

n_label = ttk.Label(root, text="Number of agents/brokerages to display:")
n_label.grid(row=1, column=0)

n_entry = ttk.Entry(root)
n_entry.grid(row=1, column=1)

display_button = ttk.Button(root, text="Display", command=lambda: display_top(market_id_entry.get(), n_entry.get()))
display_button.grid(row=2, column=0, columnspan=2, pady=10)

results_frame = ttk.LabelFrame(root, text="Results", height=200, width=300)
results_frame.grid(row=3, column=0, columnspan=2)


def display_top(market_id, n):
    top_agents = get_top_agents(market_id, n)
    top_brokerages = get_top_brokerages(market_id, n)

    for i, agent in enumerate(top_agents):
        agent_label = ttk.Label(results_frame, text="Agent {}: {} ({} sales)".format(i + 1, agent[1], agent[2]))
        agent_label.grid(row=i, column=0)

    for i, brokerage in enumerate(top_brokerages):
        brokerage_label = ttk.Label(results_frame,
                                    text="Brokerage {}: {} ({} sales)".format(i + 1, brokerage[1], brokerage[2]))
        brokerage_label.grid(row=i, column=1)


root.mainloop()
