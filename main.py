import subprocess
import time
import os
import sys
from datetime import datetime, timedelta

# Configuration
SCRAPER_SCRIPT = "get_nba_game_id.py"
DATA_FETCHER_SCRIPT = "espn_nba_data.py"
GAME_START_TIME_FILE = "game_start_time.txt"
GAME_IDS_FILE = "game_id.txt"
LOOP_INTERVAL_SECONDS = 60  # 1 minutes
MAX_RUN_DURATION_HOURS = 14  # Stop after 14 hours to prevent infinite runs
BUFFER_MINUTES = 30  # Start fetching data 30 minutes before game time

def run_script(script_name):
    """Runs a python script using the current python interpreter."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting {script_name}...")
    try:
        # Run the script and wait for it to finish
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            check=False # Don't raise exception on non-zero exit code
        )
        
        if result.returncode == 0:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {script_name} finished successfully.")
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {script_name} finished with exit code {result.returncode}.")
            
        # Optional: Print output if needed
        # print(result.stdout)
        if result.stderr:
             print(f"Stderr: {result.stderr}")

        return result.returncode
    except Exception as e:
        print(f"Error running {script_name}: {e}")
        return -1


def check_for_games():
    """Checks if the game_id.txt file exists and has content."""
    if not os.path.exists(GAME_IDS_FILE):
        return False
    
    with open(GAME_IDS_FILE, 'r') as f:
        content = f.read().strip()
        if content:
            return True
    return False

def read_game_start_time():
    """Reads the game start time from file and returns it as a datetime object."""
    try:
        if not os.path.exists(GAME_START_TIME_FILE):
            print(f"Warning: {GAME_START_TIME_FILE} not found.")
            return None
        
        with open(GAME_START_TIME_FILE, 'r') as f:
            time_str = f.read().strip()  # Format: "HH:MM"
        
        # Parse the time
        hour, minute = map(int, time_str.split(':'))
        
        # Create a datetime object for today at that time
        now = datetime.now()
        game_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # If the game time has already passed today, it might be tomorrow
        # (This shouldn't happen if cron runs at 10 AM and games are later)
        if game_time < now:
            print(f"Warning: Game time {game_time.strftime('%H:%M')} has already passed.")
            return None
        
        return game_time
        
    except Exception as e:
        print(f"Error reading game start time: {e}")
        return None

def calculate_sleep_duration(game_time):
    """Calculate how long to sleep until BUFFER_MINUTES before game time."""
    now = datetime.now()
    wake_time = game_time - timedelta(minutes=BUFFER_MINUTES)
    
    if wake_time <= now:
        # Game is starting soon or already started
        return 0
    
    sleep_duration = (wake_time - now).total_seconds()
    return sleep_duration

def main():
    print("--- NBA Data Manager Started ---")
    
    # Step 1: Run the scraper to get today's game IDs
    print("\n--- Step 1: Scraping Game IDs ---")
    exit_code = run_script(SCRAPER_SCRIPT)
    if exit_code != 0:
        print("Scraper failed. Exiting.")
        return

    # Step 2: Check if there are games today
    if not check_for_games():
        print("\nNo games found in game_id.txt. Exiting.")
        return

    print("\nGames found!")
    
    # Step 3: Read game start time and calculate sleep duration
    game_time = read_game_start_time()
    
    if game_time:
        sleep_seconds = calculate_sleep_duration(game_time)
        
        if sleep_seconds > 0:
            wake_time = datetime.now() + timedelta(seconds=sleep_seconds)
            print(f"\nFirst game starts at: {game_time.strftime('%I:%M %p')}")
            print(f"Sleeping until: {wake_time.strftime('%I:%M %p')} ({sleep_seconds/3600:.2f} hours)")
            print("Zzz... 😴")
            time.sleep(sleep_seconds)
            print("\n⏰ Waking up! Time to fetch game data.")
        else:
            print("\nGame is starting soon or already started. Beginning data fetch immediately.")
    else:
        print("\nCould not determine game start time. Beginning data fetch immediately.")
    
    # Step 4: Loop to fetch data
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=MAX_RUN_DURATION_HOURS)
    
    print(f"\nData fetch loop will run until: {end_time.strftime('%Y-%m-%d %I:%M %p')}")
    
    while datetime.now() < end_time:
        print(f"\n--- Fetching Data ---")
        exit_code = run_script(DATA_FETCHER_SCRIPT)
        
        if exit_code == 5:
            print("\n>>> All games are final. Manager stopping. <<<")
            break
        
        print(f"Sleeping for {LOOP_INTERVAL_SECONDS/60} minutes...")
        time.sleep(LOOP_INTERVAL_SECONDS)

    print("\nManager exiting.")

if __name__ == "__main__":
    main()
