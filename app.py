import streamlit as st
import datetime
import json
import os

# --- DATA HANDLING ---
DATA_FILE = "habits_v2.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    # Default structure with XP
    return {"habits": {}, "total_xp": 0}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# --- UI SETUP ---
st.set_page_config(page_title="Life Optimizer", layout="centered")
st.title("🚀 Life Optimizer")

data = load_data()
today_date = datetime.date.today()
today_str = str(today_date)

# --- XP LOGIC ---
xp_per_habit = 10
xp_needed_per_level = 100
current_level = (data["total_xp"] // xp_needed_per_level) + 1
progress_to_next_level = (data["total_xp"] % xp_needed_per_level) / xp_needed_per_level

# --- DISPLAY STATS ---
st.subheader(f"Level {current_level} Warrior")
st.progress(progress_to_next_level)
st.caption(f"✨ {data['total_xp'] % xp_needed_per_level} / {xp_needed_per_level} XP to Level {current_level + 1} (Total XP: {data['total_xp']})")

# --- SIDEBAR: SETTINGS ---
with st.sidebar:
    st.header("Settings")
    new_habit = st.text_input("New Habit Name")
    if st.button("Add Habit"):
        if new_habit and new_habit not in data["habits"]:
            data["habits"][new_habit] = []
            save_data(data)
            st.rerun()
    
    if st.button("Reset All Progress", type="primary"):
        save_data({"habits": {}, "total_xp": 0})
        st.rerun()

# --- MAIN INTERFACE: CHECKLIST ---
st.divider()
st.subheader("Daily Tasks")

if not data["habits"]:
    st.info("Add a habit in the sidebar to start earning XP!")
else:
    for habit in list(data["habits"].keys()):
        dates = data["habits"][habit]
        is_done = today_str in dates
        
        # Checkbox for habit
        checked = st.checkbox(f"Completed: {habit}", value=is_done, key=habit)
        
        if checked and not is_done:
            data["habits"][habit].append(today_str)
            data["total_xp"] += xp_per_habit
            save_data(data)
            st.toast(f"Gain +{xp_per_habit} XP!", icon="🔥")
            st.rerun()
        elif not checked and is_done:
            data["habits"][habit].remove(today_str)
            data["total_xp"] = max(0, data["total_xp"] - xp_per_habit)
            save_data(data)
            st.rerun()

# --- VISUALIZATION: MINI GRID ---
st.subheader("Weekly Momentum")
cols = st.columns(7)
for i in range(7):
    day = today_date - datetime.timedelta(days=(6 - i))
    day_str = str(day)
    day_label = day.strftime("%a")
    
    # Check if ANY habit was done on that day
    any_done = any(day_str in dates for dates in data["habits"].values())
    
    with cols[i]:
        st.markdown(f"{'🟩' if any_done else '⬜'}")
        st.caption(day_label)

# --- FOOTER ---
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0; bottom: 0; width: 100%;
        background-color: transparent; color: #888888;
        text-align: center; padding: 10px;
        font-size: 14px; letter-spacing: 1px;
    }
    </style>
    <div class="footer">
        <p>made by <b>Al Hadi</b></p>
    </div>
    """, unsafe_allow_html=True)
