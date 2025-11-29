import requests
import sys
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
# Import necessary components for Supabase
from supabase import create_client, Client 

# Load environment variables from .env file
load_dotenv()

# Access the API endpoint
api_endpoint = os.getenv("ESPN_ENDPOINT")

# Supabase configuration
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
if supabase_url and supabase_key:
    supabase: Client = create_client(supabase_url, supabase_key)
    print("Supabase client initialized successfully.")
else:
    supabase = None
    print("Warning: Supabase credentials not found. Database operations will be skipped.")

# Global variable to store API data for each game
api_data = None


def get_game_status(): 
    game_status = api_data["header"]["competitions"][0]["status"]["type"]["description"]
    print(game_status)
    return game_status

def team_one_info():
    team_one_name = api_data["boxscore"]["teams"][1]["team"]["name"]
    print(f"--- {team_one_name}---\n")
    team_one_logo = api_data["boxscore"]["teams"][1]["team"]["logo"]
    print(team_one_logo)
    team_one_record = api_data["header"]["competitions"][0]["competitors"][0]["record"][0]["displayValue"]
    print(team_one_record)
    team_one_score = api_data["header"]["competitions"][0]["competitors"][0]["score"]
    print(team_one_score)

    team_one_field_goals = api_data["boxscore"]["teams"][1]["statistics"][0]["displayValue"]
    print(team_one_field_goals)
    team_one_three_points = api_data["boxscore"]["teams"][1]["statistics"][2]["displayValue"]
    print(team_one_three_points)
    team_one_free_throws = api_data["boxscore"]["teams"][1]["statistics"][4]["displayValue"]
    print(team_one_free_throws)
    team_one_rebounds = api_data["boxscore"]["teams"][1]["statistics"][5]["displayValue"]
    print(team_one_rebounds)
    team_one_assists = api_data["boxscore"]["teams"][1]["statistics"][8]["displayValue"]
    print(team_one_assists)
    team_one_steals = api_data["boxscore"]["teams"][1]["statistics"][9]["displayValue"]
    print(team_one_steals)
    team_one_blocks = api_data["boxscore"]["teams"][1]["statistics"][10]["displayValue"]
    print(team_one_blocks)
    team_one_turnovers = api_data["boxscore"]["teams"][1]["statistics"][13]["displayValue"]
    print(team_one_turnovers)
    team_one_turnover_points = api_data["boxscore"]["teams"][1]["statistics"][18]["displayValue"]
    print(team_one_turnover_points)
    team_one_points_in_paint = api_data["boxscore"]["teams"][1]["statistics"][20]["displayValue"]
    print(team_one_points_in_paint)
    team_one_fouls = api_data["boxscore"]["teams"][1]["statistics"][21]["displayValue"]
    print(team_one_fouls)


def team_two_basic_info():
    team_two_name = api_data["boxscore"]["teams"][0]["team"]["name"]
    print(f"--- {team_two_name}---\n")
    team_two_logo = api_data["boxscore"]["teams"][0]["team"]["logo"]
    print(team_two_logo)
    team_two_record = api_data["header"]["competitions"][0]["competitors"][1]["record"][0]["displayValue"]
    print(team_two_record)
    team_two_score = api_data["header"]["competitions"][0]["competitors"][1]["score"]
    print(team_two_score)

    team_one_field_goals = api_data["boxscore"]["teams"][0]["statistics"][0]["displayValue"]
    print(team_one_field_goals)
    team_one_three_points = api_data["boxscore"]["teams"][0]["statistics"][2]["displayValue"]
    print(team_one_three_points)
    team_one_free_throws = api_data["boxscore"]["teams"][0]["statistics"][4]["displayValue"]
    print(team_one_free_throws)
    team_one_rebounds = api_data["boxscore"]["teams"][0]["statistics"][5]["displayValue"]
    print(team_one_rebounds)
    team_one_assists = api_data["boxscore"]["teams"][0]["statistics"][8]["displayValue"]
    print(team_one_assists)
    team_one_steals = api_data["boxscore"]["teams"][0]["statistics"][9]["displayValue"]
    print(team_one_steals)
    team_one_blocks = api_data["boxscore"]["teams"][0]["statistics"][10]["displayValue"]
    print(team_one_blocks)
    team_one_turnovers = api_data["boxscore"]["teams"][0]["statistics"][13]["displayValue"]
    print(team_one_turnovers)
    team_one_turnover_points = api_data["boxscore"]["teams"][0]["statistics"][18]["displayValue"]
    print(team_one_turnover_points)
    team_one_points_in_paint = api_data["boxscore"]["teams"][0]["statistics"][20]["displayValue"]
    print(team_one_points_in_paint)
    team_one_fouls = api_data["boxscore"]["teams"][0]["statistics"][21]["displayValue"]
    print(team_one_fouls)


def team_quarter_score(): 
    team_one_quarter_scores = []
    team_two_quarter_scores = []

    try: 
        linescores  = api_data["header"]["competitions"][0]["competitors"][0]["linescores"]

        # Iterate through the actual list items (more Pythonic)
        for score_dict in linescores: 
            
            # Safely get the value using the .get() method
            score_value = score_dict.get("displayValue")
            
            # Check if the retrieved value is empty or None
            if score_value is None or score_value == "":
                team_one_quarter_scores.append("N/A")
            else:
                team_one_quarter_scores.append(score_value)
    except: 
        # If the initial path fails, ensure the list is empty/handled
        # For a full game, this usually means the path is wrong or data is heavily missing
        print("Could not access 'linescores' path.")

    # Example Output: ['10', '7', 'N/A', '3']
    print(team_one_quarter_scores)

    try: 
        linescores  = api_data["header"]["competitions"][0]["competitors"][1]["linescores"]

        # Iterate through the actual list items (more Pythonic)
        for score_dict in linescores: 
            
            # Safely get the value using the .get() method
            score_value = score_dict.get("displayValue")
            
            # Check if the retrieved value is empty or None
            if score_value is None or score_value == "":
                team_two_quarter_scores.append("N/A")
            else:
                team_two_quarter_scores.append(score_value)
    except: 
        # If the initial path fails, ensure the list is empty/handled
        # For a full game, this usually means the path is wrong or data is heavily missing
        print("Could not access 'linescores' path.")

    # Example Output: ['10', '7', 'N/A', '3']
    print(team_two_quarter_scores)


def game_time_quarter(): 
    game_period_time = ""

    try:
        game_period  = api_data["header"]["competitions"][0]["status"]["type"]["shortDetail"]
        
        # Check if the retrieved value is empty or None
        if game_period is None or game_period == "":
            game_period_time = "N/A"
        else:
            game_period_time = game_period
    except (KeyError, IndexError):
        game_period_time = "N/A"

    print(game_period_time)


def get_safe_value(data_dict, path_list, default="N/A"):
    """Safely navigates a nested dictionary/list structure."""
    current_level = data_dict
    for key in path_list:
        try:
            current_level = current_level[key]
        except (KeyError, IndexError, TypeError):
            # If any part of the path fails, return the default value
            return default
    
    # Check if the found value is empty (like None or an empty string)
    if current_level is None or current_level == "":
        return default
        
    return current_level


def collect_game_data(game_id):
    """Collects all game data into a dictionary matching the database schema."""
    
    # Initialize data dictionary
    game_data = {
        'game_id': game_id,
        'last_updated': datetime.now().isoformat(),
    }
    
    try:
        # ======================================================================
        # GAME METADATA
        # ======================================================================
        game_data['game_status'] = get_safe_value(api_data, ["header", "competitions", 0, "status", "type", "description"])
        game_data['game_clock'] = get_safe_value(api_data, ["header", "competitions", 0, "status", "displayClock"])
        game_data['game_period'] = get_safe_value(api_data, ["header", "competitions", 0, "status", "type", "shortDetail"])
        
        # ======================================================================
        # TEAM 1 - BASIC INFO
        # ======================================================================
        game_data['team_one_name'] = get_safe_value(api_data, ["boxscore", "teams", 1, "team", "name"])
        game_data['team_one_logo'] = get_safe_value(api_data, ["boxscore", "teams", 1, "team", "logo"])
        game_data['team_one_record'] = get_safe_value(api_data, ["header", "competitions", 0, "competitors", 0, "record", 0, "displayValue"])
        
        # Score as integer (try to convert, use None if not a number)
        score_one = get_safe_value(api_data, ["header", "competitions", 0, "competitors", 0, "score"], None)
        try:
            game_data['team_one_score'] = int(score_one) if score_one and score_one != "N/A" else None
        except (ValueError, TypeError):
            game_data['team_one_score'] = None
        
        # ======================================================================
        # TEAM 1 - STATISTICS
        # ======================================================================
        game_data['team_one_field_goals'] = get_safe_value(api_data, ["boxscore", "teams", 1, "statistics", 0, "displayValue"])
        game_data['team_one_three_points'] = get_safe_value(api_data, ["boxscore", "teams", 1, "statistics", 2, "displayValue"])
        game_data['team_one_free_throws'] = get_safe_value(api_data, ["boxscore", "teams", 1, "statistics", 4, "displayValue"])
        game_data['team_one_rebounds'] = get_safe_value(api_data, ["boxscore", "teams", 1, "statistics", 5, "displayValue"])
        game_data['team_one_assists'] = get_safe_value(api_data, ["boxscore", "teams", 1, "statistics", 8, "displayValue"])
        game_data['team_one_steals'] = get_safe_value(api_data, ["boxscore", "teams", 1, "statistics", 9, "displayValue"])
        game_data['team_one_blocks'] = get_safe_value(api_data, ["boxscore", "teams", 1, "statistics", 10, "displayValue"])
        game_data['team_one_turnovers'] = get_safe_value(api_data, ["boxscore", "teams", 1, "statistics", 13, "displayValue"])
        game_data['team_one_turnover_points'] = get_safe_value(api_data, ["boxscore", "teams", 1, "statistics", 18, "displayValue"])
        game_data['team_one_points_in_paint'] = get_safe_value(api_data, ["boxscore", "teams", 1, "statistics", 20, "displayValue"])
        game_data['team_one_fouls'] = get_safe_value(api_data, ["boxscore", "teams", 1, "statistics", 21, "displayValue"])
        
        # ======================================================================
        # TEAM 1 - QUARTER SCORES
        # ======================================================================
        team_one_quarter_scores = []
        try:
            linescores = api_data["header"]["competitions"][0]["competitors"][0]["linescores"]
            for score_dict in linescores:
                score_value = score_dict.get("displayValue")
                if score_value is None or score_value == "":
                    team_one_quarter_scores.append(None)  # Use None instead of "N/A" for JSONB
                else:
                    team_one_quarter_scores.append(score_value)
        except (KeyError, IndexError, TypeError):
            pass
        game_data['team_one_quarter_scores'] = team_one_quarter_scores if team_one_quarter_scores else []
        
        # ======================================================================
        # TEAM 1 - POINTS LEADER
        # ======================================================================
        base_pl = ["leaders", 0, "leaders", 0, "leaders", 0]
        game_data['team_one_pl_name'] = get_safe_value(api_data, base_pl + ["athlete", "fullName"])
        game_data['team_one_pl_image'] = get_safe_value(api_data, base_pl + ["athlete", "headshot", "href"])
        game_data['team_one_pl_points'] = get_safe_value(api_data, base_pl + ["statistics", 0, "displayValue"])
        game_data['team_one_pl_field_goals'] = get_safe_value(api_data, base_pl + ["statistics", 1, "displayValue"])
        game_data['team_one_pl_free_throws'] = get_safe_value(api_data, base_pl + ["statistics", 2, "displayValue"])
        
        # ======================================================================
        # TEAM 1 - ASSISTS LEADER
        # ======================================================================
        base_al = ["leaders", 0, "leaders", 1, "leaders", 0]
        game_data['team_one_al_name'] = get_safe_value(api_data, base_al + ["athlete", "fullName"])
        game_data['team_one_al_image'] = get_safe_value(api_data, base_al + ["athlete", "headshot", "href"])
        game_data['team_one_al_assist'] = get_safe_value(api_data, base_al + ["statistics", 0, "displayValue"])
        game_data['team_one_al_turnovers'] = get_safe_value(api_data, base_al + ["statistics", 1, "displayValue"])
        game_data['team_one_al_minutes_played'] = get_safe_value(api_data, base_al + ["statistics", 2, "displayValue"])
        
        # ======================================================================
        # TEAM 1 - REBOUNDS LEADER
        # ======================================================================
        base_rl = ["leaders", 0, "leaders", 2, "leaders", 0]
        game_data['team_one_rl_name'] = get_safe_value(api_data, base_rl + ["athlete", "fullName"])
        game_data['team_one_rl_image'] = get_safe_value(api_data, base_rl + ["athlete", "headshot", "href"])
        game_data['team_one_rl_rebounds'] = get_safe_value(api_data, base_rl + ["statistics", 0, "displayValue"])
        game_data['team_one_rl_defensive_rebounds'] = get_safe_value(api_data, base_rl + ["statistics", 1, "displayValue"])
        game_data['team_one_rl_offensive_rebounds'] = get_safe_value(api_data, base_rl + ["statistics", 2, "displayValue"])
        
        # ======================================================================
        # TEAM 2 - BASIC INFO
        # ======================================================================
        game_data['team_two_name'] = get_safe_value(api_data, ["boxscore", "teams", 0, "team", "name"])
        game_data['team_two_logo'] = get_safe_value(api_data, ["boxscore", "teams", 0, "team", "logo"])
        game_data['team_two_record'] = get_safe_value(api_data, ["header", "competitions", 0, "competitors", 1, "record", 0, "displayValue"])
        
        # Score as integer
        score_two = get_safe_value(api_data, ["header", "competitions", 0, "competitors", 1, "score"], None)
        try:
            game_data['team_two_score'] = int(score_two) if score_two and score_two != "N/A" else None
        except (ValueError, TypeError):
            game_data['team_two_score'] = None
        
        # ======================================================================
        # TEAM 2 - STATISTICS
        # ======================================================================
        game_data['team_two_field_goals'] = get_safe_value(api_data, ["boxscore", "teams", 0, "statistics", 0, "displayValue"])
        game_data['team_two_three_points'] = get_safe_value(api_data, ["boxscore", "teams", 0, "statistics", 2, "displayValue"])
        game_data['team_two_free_throws'] = get_safe_value(api_data, ["boxscore", "teams", 0, "statistics", 4, "displayValue"])
        game_data['team_two_rebounds'] = get_safe_value(api_data, ["boxscore", "teams", 0, "statistics", 5, "displayValue"])
        game_data['team_two_assists'] = get_safe_value(api_data, ["boxscore", "teams", 0, "statistics", 8, "displayValue"])
        game_data['team_two_steals'] = get_safe_value(api_data, ["boxscore", "teams", 0, "statistics", 9, "displayValue"])
        game_data['team_two_blocks'] = get_safe_value(api_data, ["boxscore", "teams", 0, "statistics", 10, "displayValue"])
        game_data['team_two_turnovers'] = get_safe_value(api_data, ["boxscore", "teams", 0, "statistics", 13, "displayValue"])
        game_data['team_two_turnover_points'] = get_safe_value(api_data, ["boxscore", "teams", 0, "statistics", 18, "displayValue"])
        game_data['team_two_points_in_paint'] = get_safe_value(api_data, ["boxscore", "teams", 0, "statistics", 20, "displayValue"])
        game_data['team_two_fouls'] = get_safe_value(api_data, ["boxscore", "teams", 0, "statistics", 21, "displayValue"])
        
        # ======================================================================
        # TEAM 2 - QUARTER SCORES
        # ======================================================================
        team_two_quarter_scores = []
        try:
            linescores = api_data["header"]["competitions"][0]["competitors"][1]["linescores"]
            for score_dict in linescores:
                score_value = score_dict.get("displayValue")
                if score_value is None or score_value == "":
                    team_two_quarter_scores.append(None)  # Use None instead of "N/A" for JSONB
                else:
                    team_two_quarter_scores.append(score_value)
        except (KeyError, IndexError, TypeError):
            pass
        game_data['team_two_quarter_scores'] = team_two_quarter_scores if team_two_quarter_scores else []
        
        # ======================================================================
        # TEAM 2 - POINTS LEADER
        # ======================================================================
        base_pl = ["leaders", 1, "leaders", 0, "leaders", 0]
        game_data['team_two_pl_name'] = get_safe_value(api_data, base_pl + ["athlete", "fullName"])
        game_data['team_two_pl_image'] = get_safe_value(api_data, base_pl + ["athlete", "headshot", "href"])
        game_data['team_two_pl_points'] = get_safe_value(api_data, base_pl + ["statistics", 0, "displayValue"])
        game_data['team_two_pl_field_goals'] = get_safe_value(api_data, base_pl + ["statistics", 1, "displayValue"])
        game_data['team_two_pl_free_throws'] = get_safe_value(api_data, base_pl + ["statistics", 2, "displayValue"])
        
        # ======================================================================
        # TEAM 2 - ASSISTS LEADER
        # ======================================================================
        base_al = ["leaders", 1, "leaders", 1, "leaders", 0]
        game_data['team_two_al_name'] = get_safe_value(api_data, base_al + ["athlete", "fullName"])
        game_data['team_two_al_image'] = get_safe_value(api_data, base_al + ["athlete", "headshot", "href"])
        game_data['team_two_al_assist'] = get_safe_value(api_data, base_al + ["statistics", 0, "displayValue"])
        game_data['team_two_al_turnovers'] = get_safe_value(api_data, base_al + ["statistics", 1, "displayValue"])
        game_data['team_two_al_minutes_played'] = get_safe_value(api_data, base_al + ["statistics", 2, "displayValue"])
        
        # ======================================================================
        # TEAM 2 - REBOUNDS LEADER
        # ======================================================================
        base_rl = ["leaders", 1, "leaders", 2, "leaders", 0]
        game_data['team_two_rl_name'] = get_safe_value(api_data, base_rl + ["athlete", "fullName"])
        game_data['team_two_rl_image'] = get_safe_value(api_data, base_rl + ["athlete", "headshot", "href"])
        game_data['team_two_rl_rebounds'] = get_safe_value(api_data, base_rl + ["statistics", 0, "displayValue"])
        game_data['team_two_rl_defensive_rebounds'] = get_safe_value(api_data, base_rl + ["statistics", 1, "displayValue"])
        game_data['team_two_rl_offensive_rebounds'] = get_safe_value(api_data, base_rl + ["statistics", 2, "displayValue"])
        
    except Exception as e:
        print(f"Error collecting game data: {e}")
        return None
    
    return game_data


def upsert_game_to_supabase(game_data):
    """Upsert game data to Supabase database."""
    if supabase is None:
        print("Supabase client not initialized. Skipping database insert.")
        return False
    
    try:
        # Clean data: convert "N/A" and empty strings to None for better database handling
        # Keep lists/arrays as-is (they'll be converted to JSONB automatically)
        cleaned_data = {}
        for key, value in game_data.items():
            # If it's a list (like quarter_scores), keep it as-is
            if isinstance(value, list):
                cleaned_data[key] = value
            # Convert "N/A" and empty strings to None
            elif value == "N/A" or value == "":
                cleaned_data[key] = None
            else:
                cleaned_data[key] = value
        
        # Upsert to Supabase (update if exists, insert if new)
        response = supabase.table('live_nba_games').upsert(
            cleaned_data,
            on_conflict='game_id'
        ).execute()
        
        print(f"✓ Successfully upserted game {game_data['game_id']} to Supabase")
        return True
        
    except Exception as e:
        print(f"✗ Error upserting game {game_data.get('game_id', 'unknown')} to Supabase: {e}")
        import traceback
        traceback.print_exc()  # Print full traceback for debugging
        return False


def upsert_final_game_to_supabase(game_data):
    """Upsert final game data to final_nba_games table."""
    if supabase is None:
        print("Supabase client not initialized. Skipping database insert.")
        return False
    
    try:
        # Clean data: convert "N/A" and empty strings to None for better database handling
        # Keep lists/arrays as-is (they'll be converted to JSONB automatically)
        cleaned_data = {}
        for key, value in game_data.items():
            # If it's a list (like quarter_scores), keep it as-is
            if isinstance(value, list):
                cleaned_data[key] = value
            # Convert "N/A" and empty strings to None
            elif value == "N/A" or value == "":
                cleaned_data[key] = None
            else:
                cleaned_data[key] = value
        
        # Upsert to final_nba_games table (update if exists, insert if new)
        response = supabase.table('final_nba_games').upsert(
            cleaned_data,
            on_conflict='game_id'
        ).execute()
        
        print(f"✓ Successfully upserted final game {game_data['game_id']} to final_nba_games")
        return True
        
    except Exception as e:
        print(f"✗ Error upserting final game {game_data.get('game_id', 'unknown')} to Supabase: {e}")
        import traceback
        traceback.print_exc()  # Print full traceback for debugging
        return False


def move_game_to_final(game_id):
    """Move a game from live_nba_games to final_nba_games and delete from live table."""
    if supabase is None:
        print("Supabase client not initialized. Skipping database operations.")
        return False
    
    try:
        # First, get the game data from live_nba_games
        response = supabase.table('live_nba_games').select('*').eq('game_id', game_id).execute()
        
        if not response.data:
            print(f"Game {game_id} not found in live_nba_games table. It may have already been moved.")
            return False
        
        # Get the game data
        live_game_data = response.data[0]
        
        # Update last_updated timestamp
        live_game_data['last_updated'] = datetime.now().isoformat()
        
        # Insert into final_nba_games
        final_response = supabase.table('final_nba_games').upsert(
            live_game_data,
            on_conflict='game_id'
        ).execute()
        
        # Delete from live_nba_games
        delete_response = supabase.table('live_nba_games').delete().eq('game_id', game_id).execute()
        
        print(f"✓ Successfully moved game {game_id} from live_nba_games to final_nba_games")
        return True
        
    except Exception as e:
        print(f"✗ Error moving game {game_id} to final table: {e}")
        import traceback
        traceback.print_exc()  # Print full traceback for debugging
        return False


def handle_final_game(game_id, game_data):
    """Handle a game that is in Final status: move to final_nba_games and remove from live."""
    if supabase is None:
        print("Supabase client not initialized. Skipping database operations.")
        return False
    
    try:
        # First, check if the game exists in live_nba_games
        check_response = supabase.table('live_nba_games').select('game_id').eq('game_id', game_id).execute()
        game_exists_in_live = len(check_response.data) > 0
        
        # Upsert to final_nba_games with final game data
        success = upsert_final_game_to_supabase(game_data)
        
        if success and game_exists_in_live:
            # Delete from live_nba_games if it was there
            delete_response = supabase.table('live_nba_games').delete().eq('game_id', game_id).execute()
            print(f"✓ Removed game {game_id} from live_nba_games (game is now final)")
        
        return success
        
    except Exception as e:
        print(f"✗ Error handling final game {game_id}: {e}")
        import traceback
        traceback.print_exc()  # Print full traceback for debugging
        return False


def team_one_player_status():
    # --- Points Leader (P L) ---
    print("\n--- Points Leader (PL) ---")

    # Base path for PL: ["leaders", 1, "leaders", 0, "leaders", 0]
    base_pl = ["leaders", 0, "leaders", 0, "leaders", 0]

    team_one_pl_name = get_safe_value(api_data, base_pl + ["athlete", "fullName"])
    print(f"Name: {team_one_pl_name}")

    team_one_pl_image = get_safe_value(api_data, base_pl + ["athlete", "headshot", "href"])
    print(f"Image: {team_one_pl_image}")
    
    team_one_pl_points = get_safe_value(api_data, base_pl + ["statistics", 0, "displayValue"])
    print(f"Points: {team_one_pl_points}")
    
    team_one_pl_field_goals = get_safe_value(api_data, base_pl + ["statistics", 1, "displayValue"])
    print(f"Field Goals: {team_one_pl_field_goals}")
    
    team_one_pl_free_throws = get_safe_value(api_data, base_pl + ["statistics", 2, "displayValue"])
    print(f"Free Throws: {team_one_pl_free_throws}")


    # --- Assists Leader (A L) ---
    print("\n--- Assists Leader (AL) ---")
    
    # Base path for AL: ["leaders", 1, "leaders", 1, "leaders", 0]
    base_al = ["leaders", 0, "leaders", 1, "leaders", 0]
    
    team_one_al_name = get_safe_value(api_data, base_al + ["athlete", "fullName"])
    print(f"Name: {team_one_al_name}")
    
    team_one_al_image = get_safe_value(api_data, base_al + ["athlete", "headshot", "href"])
    print(f"Image: {team_one_al_image}")
    
    team_one_al_assist = get_safe_value(api_data, base_al + ["statistics", 0, "displayValue"])
    print(f"Assist: {team_one_al_assist}")
    
    team_one_al_turnovers = get_safe_value(api_data, base_al + ["statistics", 1, "displayValue"])
    print(f"Turnovers: {team_one_al_turnovers}")
    
    # MP = Minutes Played
    team_one_al_mp = get_safe_value(api_data, base_al + ["statistics", 2, "displayValue"])
    print(f"Minutes Played: {team_one_al_mp}")


    # --- Rebounds Leader (R L) ---
    print("\n--- Rebounds Leader (RL) ---")
    
    # Base path for RL: ["leaders", 1, "leaders", 2, "leaders", 0]
    base_rl = ["leaders", 0, "leaders", 2, "leaders", 0]
    
    team_one_rl_name = get_safe_value(api_data, base_rl + ["athlete", "fullName"])
    print(f"Name: {team_one_rl_name}")
    
    team_one_rl_image = get_safe_value(api_data, base_rl + ["athlete", "headshot", "href"])
    print(f"Image: {team_one_rl_image}")
    
    team_one_rl_rebounds = get_safe_value(api_data, base_rl + ["statistics", 0, "displayValue"])
    print(f"Rebounds: {team_one_rl_rebounds}")
    
    #DR = Defensive Rebounds
    team_one_rl_dr = get_safe_value(api_data, base_rl + ["statistics", 1, "displayValue"])
    print(f"Defensive Rebounds: {team_one_rl_dr}")
    
    #OR = Offensive Rebounds
    team_one_rl_or = get_safe_value(api_data, base_rl + ["statistics", 2, "displayValue"])
    print(f"Offensive Rebounds: {team_one_rl_or}")


def team_two_player_status():
    # --- Points Leader (P L) ---
    print("\n--- Points Leader (PL) ---")
    
    # Base path for PL: ["leaders", 1, "leaders", 0, "leaders", 0]
    base_pl = ["leaders", 1, "leaders", 0, "leaders", 0]
    
    team_two_pl_name = get_safe_value(api_data, base_pl + ["athlete", "fullName"])
    print(f"Name: {team_two_pl_name}")
    
    team_two_pl_image = get_safe_value(api_data, base_pl + ["athlete", "headshot", "href"])
    print(f"Image: {team_two_pl_image}")
    
    team_two_pl_points = get_safe_value(api_data, base_pl + ["statistics", 0, "displayValue"])
    print(f"Points: {team_two_pl_points}")
    
    team_two_pl_field_goals = get_safe_value(api_data, base_pl + ["statistics", 1, "displayValue"])
    print(f"Field Goals: {team_two_pl_field_goals}")
    
    team_two_pl_free_throws = get_safe_value(api_data, base_pl + ["statistics", 2, "displayValue"])
    print(f"Free Throws: {team_two_pl_free_throws}")


    # --- Assists Leader (A L) ---
    print("\n--- Assists Leader (AL) ---")
    
    # Base path for AL: ["leaders", 1, "leaders", 1, "leaders", 0]
    base_al = ["leaders", 1, "leaders", 1, "leaders", 0]
    
    team_two_al_name = get_safe_value(api_data, base_al + ["athlete", "fullName"])
    print(f"Name: {team_two_al_name}")
    
    team_two_al_image = get_safe_value(api_data, base_al + ["athlete", "headshot", "href"])
    print(f"Image: {team_two_al_image}")
    
    team_two_al_assist = get_safe_value(api_data, base_al + ["statistics", 0, "displayValue"])
    print(f"Assist: {team_two_al_assist}")
    
    team_two_al_turnovers = get_safe_value(api_data, base_al + ["statistics", 1, "displayValue"])
    print(f"Turnovers: {team_two_al_turnovers}")
    
    # MP = Minutes Played
    team_two_al_mp = get_safe_value(api_data, base_al + ["statistics", 2, "displayValue"])
    print(f"Minutes Played: {team_two_al_mp}")


    # --- Rebounds Leader (R L) ---
    print("\n--- Rebounds Leader (RL) ---")
    
    # Base path for RL: ["leaders", 1, "leaders", 2, "leaders", 0]
    base_rl = ["leaders", 1, "leaders", 2, "leaders", 0]
    
    team_two_rl_name = get_safe_value(api_data, base_rl + ["athlete", "fullName"])
    print(f"Name: {team_two_rl_name}")
    
    team_two_rl_image = get_safe_value(api_data, base_rl + ["athlete", "headshot", "href"])
    print(f"Image: {team_two_rl_image}")
    
    team_two_rl_rebounds = get_safe_value(api_data, base_rl + ["statistics", 0, "displayValue"])
    print(f"Rebounds: {team_two_rl_rebounds}")
    
    #DR = Defensive Rebounds
    team_two_rl_dr = get_safe_value(api_data, base_rl + ["statistics", 1, "displayValue"])
    print(f"Defensive Rebounds: {team_two_rl_dr}")
    
    #OR = Offensive Rebounds
    team_two_rl_or = get_safe_value(api_data, base_rl + ["statistics", 2, "displayValue"])
    print(f"Offensive Rebounds: {team_two_rl_or}")


# Read game IDs from file
GAME_IDS_FILE = 'game_id.txt'

try:
    with open(GAME_IDS_FILE, 'r', encoding='utf-8') as file:
        game_ids = [line.strip() for line in file if line.strip()]
    
    print(f"Found {len(game_ids)} game ID(s) to process.\n")
    print("=" * 80)
    
    # Process each game ID
    all_games_are_final = True
    for idx, game_id in enumerate(game_ids, 1):
        print(f"\n{'=' * 80}")
        print(f"Processing Game {idx}/{len(game_ids)} - Game ID: {game_id}")
        print(f"{'=' * 80}\n")
        
        # Fetch API data for this game
        url = f"{api_endpoint}{game_id}"
        response = requests.get(url)
        
        if response.status_code == 200:
            api_data = response.json()
            
            # Get game status
            game_status = get_game_status()
            
            # Only fetch game information if the game is not "Scheduled"
            if game_status != "Scheduled":
                print(f"\nGame Status: {game_status} - Fetching game details...\n")
                
                # Collect all game data into a dictionary
                game_data = collect_game_data(game_id)
                
                if game_data:
                    # Check if game is Final (case-insensitive check for variations)
                    game_status_lower = game_status.lower() if game_status else ""
                    is_final = (
                        "final" in game_status_lower or 
                        game_status == "F/OT" or 
                        game_status == "Final/OT"
                    )
                    
                    if is_final:
                        # Handle final game: move to final_nba_games and remove from live_nba_games
                        print(f"Game {game_id} is final. Moving to final_nba_games...")
                        handle_final_game(game_id, game_data)
                    else:
                        # Game is still live: upsert to live_nba_games
                        upsert_game_to_supabase(game_data)
                        all_games_are_final = False
                else:
                    print("Failed to collect game data.")
                    all_games_are_final = False
            else:
                print(f"\nGame Status: {game_status} - No information will be fetched.")
                if game_status == "Scheduled":
                    all_games_are_final = False
        else:
            print(f'Failed to retrieve data for game ID {game_id}: {response.status_code}')
        
        print(f"\n{'=' * 80}\n")
    
    print(f"Finished processing all {len(game_ids)} game(s).")
    
    if all_games_are_final and len(game_ids) > 0:
        print("All games are final. Exiting with code 5.")
        sys.exit(5)
    
    
except FileNotFoundError:
    print(f"Error: File '{GAME_IDS_FILE}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")