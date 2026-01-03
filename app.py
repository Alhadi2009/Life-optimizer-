import streamlit as st
import datetime
import json
import os

# --- DATA HANDLING (Pure Python) ---
DATA_FILE = "habits.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# --- UI SETUP ---
st.set_page_config(page_title="Life Optimizer", layout="centered")
st.title("🚀 Life Optimizer")

data = load_data()
today_date = datetime.date.today()
today_str = str(today_date)

# --- SIDEBAR: LOG HABITS ---
with st.sidebar:
    st.header("Settings")
    new_habit = st.text_input("New Habit Name")
    if st.button("Add Habit"):
        if new_habit and new_habit not in data:
            data[new_habit] = []
            save_data(data)
            st.rerun()
    
    if st.button("Clear All Data", type="primary"):
        save_data({})
        st.rerun()

# --- MAIN INTERFACE: CHECKLIST ---
st.subheader("Daily Checklist")
if not data:
    st.info("Use the sidebar to add your first habit!")
else:
    for habit in list(data.keys()):
        is_done = today_str in data[habit]
        # Checkbox to toggle habit
        checked = st.checkbox(f"Did you {habit} today?", value=is_done, key=habit)
        
        if checked and not is_done:
            data[habit].append(today_str)
            save_data(data)
            st.rerun()
        elif not checked and is_done:
            data[habit].remove(today_str)
            save_data(data)
            st.rerun()

# --- VISUALIZATION: EMOJI GRID ---
st.divider()
st.subheader("Last 7 Days Activity")

if data:
    for habit, dates in data.items():
        st.write(f"**{habit}**")
        cols = st.columns(7)
        for i in range(7):
            # Calculate date for the last 7 days (Right to Left)
            day = today_date - datetime.timedelta(days=(6 - i))
            day_str = str(day)
            
            # Label for the day (e.g., "Mon")
            day_label = day.strftime("%a")
            
            with cols[i]:
                if day_str in dates:
                    st.markdown(f"🟩\n\n{day_label}")
                else:
                    st.markdown(f"⬜\n\n{day_label}")
else:
    st.write("No data to display yet.")

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
