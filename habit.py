import json
import datetime
import os

# Configuration
DATA_FILE = os.path.expanduser("~/.habits.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def log_habit(habit_name):
    data = load_data()
    today = str(datetime.date.today())
    
    if habit_name not in data:
        data[habit_name] = []
    
    if today not in data[habit_name]:
        data[habit_name].append(today)
        print(f"✅ Logged '{habit_name}' for today!")
    else:
        print(f"⚠️  '{habit_name}' already logged for today.")
    
    save_data(data)

def show_heatmap():
    data = load_data()
    print("\n--- 7-Day Habit Heatmap ---")
    today = datetime.date.today()
    last_7_days = [(today - datetime.timedelta(days=i)) for i in range(6, -1, -1)]
    
    for habit, dates in data.items():
        row = []
        for d in last_7_days:
            # Full block (█) if done, light shade (░) if not
            row.append("█" if str(d) in dates else "░")
        
        print(f"{habit.ljust(12)} [{' '.join(row)}]")
    print("---------------------------\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python habit.py [habit_name] OR python habit.py --view")
    elif sys.argv[1] == "--view":
        show_heatmap()
    else:
        log_habit(sys.argv[1])
        
