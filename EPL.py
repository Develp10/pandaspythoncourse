# Import the necessary libraries
import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd


# Sets the page layout to wide
st.set_page_config(layout="wide")

# Fetch data from the API, and create a list of dictionaries with id, first_name and second_name from the elements section in the API
response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/", verify=False)
data = response.json()
players = [{'id': player['id'], 'name': f"{player['first_name']} {player['second_name']}"} for player in data['elements']]

# Lets start creating our Streamlit App
st.title('FPL Player Selection Dashboard')

# Create two multiselect dropdowns, one for players and other for metrics
player_names = [player['name'] for player in players]
selected_names = st.multiselect('Select Players:', player_names)
all_metrics = [
    "form", "now_cost", "points_per_game", "selected_by_percent",
    "total_points", "goals_scored", "assists", "clean_sheets",
    "goals_conceded", "yellow_cards", "red_cards", "saves",
    "bonus", "influence", "creativity", "threat", "minutes"
]
selected_metrics = st.multiselect('Select Metrics:', all_metrics)

# Get the selected players' ids
if selected_names and selected_metrics:
    selected_players = [player for player in players if player['name'] in selected_names]
    selected_ids = [player['id'] for player in selected_players]

    player_data = [player for player in data['elements'] if player['id'] in selected_ids]

    # Create Graphs for selected players and metrics
    for i in range(0, len(selected_metrics), 3):
        fig, axs = plt.subplots(1, 3, figsize=(20, 5))
        for j, metric in enumerate(selected_metrics[i:i + 3]):
            if i + j < len(selected_metrics):
                for player in player_data:
                    bar = axs[j].bar(player['first_name'], float(player[metric]), label=player['first_name'])
                    yval = bar[0].get_height()
                    axs[j].text(bar[0].get_x() + bar[0].get_width() / 2.0, yval, round(float(player[metric]), 2),
                                va='bottom')
                axs[j].set_title(metric)
                axs[j].legend()
        st.pyplot(fig)

    # Create a data table, here we are using a dataframe to give modern look for the table with an ability to sort and filter columns
    table_data = []
    for player in player_data:
        row_data = {'Name': player['first_name']}
        for metric in selected_metrics:
            row_data[metric] = float(player[metric])
        table_data.append(row_data)

    df = pd.DataFrame(table_data)
    # Display the data table
    st.write(df.style.set_properties(**{'width': '100%'}).format("{:.2f}",subset=pd.IndexSlice[:,df.columns[1:]]))
