import streamlit as st
import pandas as pd
import datetime
import json
import os
import seaborn as sns
import matplotlib.pyplot as plt

# --- DATA HANDLING ---
DATA_FILE = "habits.json"

def load_data():
    (DATA_FILE)
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# --- UI SETUP ---
st.set_page_config(page_title="Life Optimizer", layout="centered")
st.title("🚀 Life Optimizer")

data = load_data()
today = str(datetime.date.today())

# --- SIDEBAR: LOG HABITS ---
with st.sidebar:
    st.header("Log Activity")
    new_habit = st.text_input("Add new habit (e.g., Coding, Gym)")
    if st.button("Add Habit"):
        if new_habit and new_habit not in data:
            data[new_habit] = []
            save_data(data)
            st.rerun()

# --- MAIN INTERFACE ---
st.subheader("Today's Progress")
cols = st.columns(len(data) if data else 1)

for i, (habit, dates) in enumerate(data.items()):
    is_done = today in dates
    if cols[i % 3].checkbox(habit, value=is_done, key=habit):
        if today not in dates:
            data[habit].append(today)
            save_data(data)
            st.rerun()
    else:
        if today in dates:
            data[habit].remove(today)
            save_data(data)
            st.rerun()

# --- VISUALIZATION (THE HEATMAP) ---
st.divider()
st.subheader("Consistency Heatmap (Last 30 Days)")

if data:
    # Create a date range for the last 30 days
    date_range = [str(datetime.date.today() - datetime.timedelta(days=x)) for x in range(30)]
    df_map = pd.DataFrame(index=data.keys(), columns=date_range)

    for habit in data.keys():
        for d in date_range:
            df_map.loc[habit, d] = 1 if d in data[habit] else 0

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 3))
    sns.heatmap(df_map.astype(float), cmap="Greens", cbar=False, linewidths=1, linecolor="#f0f2f6", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.info("Add a habit in the sidebar to start tracking!")


# --- FOOTER ---
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: #888888;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        letter-spacing: 1px;
    }
    </style>
    <div class="footer">
        <p>made by <b>Al Hadi</b></p>
    </div>
    """, unsafe_allow_html=True)

