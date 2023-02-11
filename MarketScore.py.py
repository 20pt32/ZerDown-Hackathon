import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt


def market_score(market_id):
    market = pd.read_csv("metric.csv")
    market_metrics = pd.read_csv("market_metrics.csv")

    market_data = market_metrics[market_metrics['market_id'] == market_id]

    median_list_price_psqft = market_data['median_list_price_psqft'].median()
    homes_sold_over_list_price_count = market_data['homes_sold_over_list_price_count'].median()
    median_sale_price_psqft = market_data['median_sale_price_psqft'].median()
    median_sale_to_list_ratio = market_data['median_sale_to_list_ratio'].median()
    days_to_pending = market_data['days_to_pending'].median()
    days_to_sell = market_data['days_to_sell'].median()

    score = ( median_list_price_psqft + homes_sold_over_list_price_count + median_sale_price_psqft + median_sale_to_list_ratio + days_to_pending + days_to_sell) / 6

    return score


def show_score():
    market_id = int(entry.get())
    score = market_score(market_id)
    label.config(text="Score for market id " + str(market_id) + " is: " + str(score))

    market_metrics = pd.read_csv("market_metrics.csv")

    market_data = market_metrics[market_metrics['market_id'] == market_id]

    median_list_price_psqft = market_data['median_list_price_psqft'].median()
    homes_sold_over_list_price_count = market_data['homes_sold_over_list_price_count'].median()
    median_sale_price_psqft = market_data['median_sale_price_psqft'].median()
    median_sale_to_list_ratio = market_data['median_sale_to_list_ratio'].median()
    days_to_pending = market_data['days_to_pending'].median()
    days_to_sell = market_data['days_to_sell'].median()

    metrics = ['median_list_price_psqft', 'homes_sold_over_list_price_count', 'median_sale_price_psqft',
               'median_sale_to_list_ratio', 'days_to_pending', 'days_to_sell']
    values = [median_list_price_psqft, homes_sold_over_list_price_count, median_sale_price_psqft,
              median_sale_to_list_ratio, days_to_pending, days_to_sell]

    fig = plt.figure(figsize=(10, 5))
    plt.bar(metrics, values)
    plt.xlabel('Metrics')
    plt.ylabel('Values')
    plt.title('Score for market id ' + str(market_id))
    plt.show()

def visualize_score(market_id, score):


    if score >= 80:
        print(f"Market {market_id} is very hot. Homes are selling quickly and for high prices.")
    elif score >= 60:
        print(f"Market {market_id} is hot. Homes are selling at a faster pace but may not be selling for high prices.")
    elif score >= 40:
        print(f"Market {market_id} is warm. Homes are selling at a moderate pace and prices are average.")
    else:
        print(f"Market {market_id} is cold. Homes are selling at a slow pace and for low prices.")


def calculate_score(market_id):
    market_metrics = pd.read_csv("market_metrics.csv")
    market_metrics = market_metrics[market_metrics['market_id'] == market_id]

    # Calculate the average number of days to sell
    avg_days_to_sell = market_metrics['days_to_sell'].mean()

    # Calculate the average number of days to pending
    avg_days_to_pending = market_metrics['days_to_pending'].mean()

    # Calculate the average sale to list ratio
    avg_sale_to_list_ratio = market_metrics['median_sale_to_list_ratio'].mean()

    # Calculate the score based on the values
    score = avg_days_to_sell * 0.2 + avg_days_to_pending * 0.3 + avg_sale_to_list_ratio * 0.5

    return score


root = tk.Tk()
root.geometry("400x400")
root.title("Market Score")

label = tk.Label(root, text="Enter market id:")
label.pack()

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Visualize Score", command=show_score)
button.pack()

button2 = tk.Button(root, text="Show Score", command=lambda: visualize_score(int(entry.get()), calculate_score(int(entry.get()))))
button2.pack()

root.mainloop()

