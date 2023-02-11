import tkinter as tk
import psycopg2

def execute_query(query):
    # Connect to the database
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="postgres",
        user="postgres",
        password="sivapriya"
    )
    cur = conn.cursor()
    # Execute the query
    cur.execute(query)
    result = cur.fetchall()
    # Close the cursor and connection
    cur.close()
    conn.close()
    return result


def get_top_agents_and_brokerages(market_id, n):
    query = f"SELECT agent_info.id, agent_info.first_name, brokerage.name \
             FROM agent_info \
             LEFT JOIN brokerage ON agent_info.brokerage_id = brokerage.id \
             WHERE agent_info.city = '{market_id}' \
             ORDER BY agent_info.id \
             LIMIT {n}"
    # Connect to the database and execute the query
    result = execute_query(query)
    return result

def display_result(result):
    # Clear the previous result
    result_text.delete('1.0', tk.END)
    # Display the new result
    for row in result:
        result_text.insert(tk.END, f"Agent ID: {row[0]}, Agent Name: {row[1]}, Brokerage Name: {row[2]} \n")

# Create the GUI window
root = tk.Tk()
root.title("Top Agents and Brokerages")

# Create the input field for the market id
market_id_label = tk.Label(root, text="Market ID:")
market_id_entry = tk.Entry(root)

# Create the input field for the number of top agents and brokerages to display
n_label = tk.Label(root, text="Number of Top Agents and Brokerages to Display:")
n_entry = tk.Entry(root)

# Create the submit button
submit_button = tk.Button(root, text="Submit", command=lambda: display_result(get_top_agents_and_brokerages(market_id_entry.get(), int(n_entry.get()))))

# Create the result display field
result_text = tk.Text(root, height=10, width=50)

# Place the widgets on the window
market_id_label.grid(row=0, column=0, padx=10, pady=10)
market_id_entry.grid(row=0, column=1, padx=10, pady=10)
n_label.grid(row=1, column=0, padx=10, pady=10)
n_entry.grid(row=1, column=1, padx=10, pady=10)
submit_button.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
result_text.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

# Start the GUI event loop
root.mainloop()
