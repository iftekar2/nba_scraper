import time
from datetime import date
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException


# --- PATH SETUP (STEP 2 & 3) ---
# Get the absolute path to the directory where this script resides.
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 

# Define file paths using the absolute BASE_DIR.
GAME_IDS_FILE = os.path.join(BASE_DIR, 'game_id.txt')
GAME_START_TIME_FILE = os.path.join(BASE_DIR, 'game_start_time.txt')
game_ids_file_handle = None


# todays_date = date.today().strftime("%Y%m%d")
todays_date = 20251130

#--- SETUP ---
chrome_options = Options()

# 1. Essential arguments for a headless Linux server:
chrome_options.add_argument("--headless=new") 
chrome_options.add_argument("--no-sandbox")        
chrome_options.add_argument("--disable-dev-shm-usage") 
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("window-size=1920x1080")

# 2. Keep the detach option
chrome_options.add_experimental_option("detach", True) 

# 3. Initialize the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get(f"https://www.espn.com/nba/scoreboard/_/date/{todays_date}")
time.sleep(5)


try: 
    # Open the file once in 'w' (write/overwrite) mode
    # NOTE: GAME_IDS_FILE is now an absolute path.
    game_ids_file_handle = open(GAME_IDS_FILE, 'w', encoding='utf-8')
    print(f"Opened file '{GAME_IDS_FILE}' for writing game IDs.")

    game_sections = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section/div/section")
    num_days = len(game_sections)
    print("-----------------------------------------------")
    print(f"The number of days found is: {num_days}")
    print("-----------------------------------------------")
    print("\n")

    for day in range(num_days): 
        try:
            game_section_element = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section/div/section[{day + 1}]")
            scraped_id = game_section_element.get_attribute('id')
            print(f"Scraped ID: {scraped_id}")

            game_ids_file_handle.write(scraped_id + "\n")
        except NoSuchElementException:
            print("Element at the long XPath not found.")

except Exception as e:
    print(f"An unexpected error occurred: {e}")

#--- Set scraper to start time ---
# GAME_START_TIME_FILE is now an absolute path.

try:
    # Find the time element
    start_time_xpath = (
        "/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section/div/section[1]"
        "//div[contains(@class, 'ScoreCell__Time')]"
    )
    
    start_time_element = driver.find_element(By.XPATH, start_time_xpath)
    start_time_full = start_time_element.text.strip()
    
    print(f"Raw start time: {start_time_full}")
    
    # Parse the time (e.g., "5:00 PM" or "12:30 PM")
    # Split by space to separate time from AM/PM
    time_parts = start_time_full.split()
    
    if len(time_parts) >= 2:
        time_str = time_parts[0]  # "5:00"
        period = time_parts[1].upper()  # "PM"
        
        # Split hours and minutes
        hour_min = time_str.split(':')
        hour = int(hour_min[0])
        minute = int(hour_min[1]) if len(hour_min) > 1 else 0
        
        # Convert to 24-hour format
        if period == 'PM' and hour != 12:
            hour += 12
        elif period == 'AM' and hour == 12:
            hour = 0
        
        # Write to file in format "HH:MM"
        # NOTE: GAME_START_TIME_FILE is now an absolute path.
        with open(GAME_START_TIME_FILE, 'w') as f:
            f.write(f"{hour:02d}:{minute:02d}")
        
        print(f"Game start time saved: {hour:02d}:{minute:02d} (24-hour format)")
    else:
        print(f"Could not parse start time: {start_time_full}")
        
except Exception as e:
    print(f"Error extracting start time: {e}")

finally:
    driver.quit()