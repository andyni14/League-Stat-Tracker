import requests

# API_KEY = "fill new one"

def get_summoner_data(summoner_name):
    # This function retrieves summoner data using the summoner name.
    base_url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(f"{base_url}{summoner_name}", headers=headers)
    
    if response.status_code == 200:
        # If the API request is successful (status code 200), return the summoner data.
        data = response.json()
        return data
    elif response.status_code == 404:
        # If the summoner is not found (status code 404), return None.
        return None
    else:
        # If there's an error with the API request, print the error status code and return None.
        print("Error:", response.status_code)
        return None

def get_most_played_champion(summoner_id):
    # This function retrieves the most played champion for a summoner using their summoner ID.
    base_url = f"https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(base_url, headers=headers)
    data = response.json()
    
    if data:
        # If champion mastery data is available, return the ID of the most played champion.
        most_played_champion_id = data[0]["championId"]
        return most_played_champion_id
    
    return None

def get_champion_name(champion_id):
    # This function retrieves the name of a champion using their champion ID.
    base_url = "https://ddragon.leagueoflegends.com/api/versions.json"
    response = requests.get(base_url)
    data = response.json()
    version = data[0]  # Get the latest version
    
    base_url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
    response = requests.get(base_url)
    data = response.json()
    champion_data = data["data"]
    
    for champion_key, champion_info in champion_data.items():
        if champion_info["key"] == str(champion_id):
            # If the champion ID matches, return the champion name.
            return champion_info["name"]
    
    return None

def get_rank_and_wins(summoner_id):
    # This function retrieves the rank and number of wins for a summoner in ranked solo queue.
    base_url = f"https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(base_url, headers=headers)
    data = response.json()
    
    if data:
        for entry in data:
            if entry["queueType"] == "RANKED_SOLO_5x5":
                # If the entry is for ranked solo queue, return the rank and number of wins.
                rank = f"{entry['tier']} {entry['rank']}"
                wins = entry["wins"]
                return rank, wins
    
    return None, None

def main():
    # This is the main function that runs the summoner tracker.
    print("Welcome to the Summoner Tracker!")
    
    while True:
        summoner_name = input("Enter your summoner name (or 'quit' to exit): ")
        
        if summoner_name.lower() == "quit":
            # If the user enters 'quit', exit the loop and end the program.
            break
        
        summoner_data = get_summoner_data(summoner_name)
        
        if summoner_data is None:
            # If the summoner is not found, display an error message and continue to the next iteration.
            print("Summoner not found. Please enter a valid summoner name.")
            continue
        
        print("\nSummoner Level:", summoner_data["summonerLevel"])
        print("Summoner ID:", summoner_data["id"])
        
        most_played_champion_id = get_most_played_champion(summoner_data["id"])
        if most_played_champion_id is not None:
            champion_name = get_champion_name(most_played_champion_id)
            print("Most Played Champion:", champion_name)
        
        rank, wins = get_rank_and_wins(summoner_data["id"])
        if rank and wins is not None:
            print("Rank:", rank)
            print("Wins:", wins)
        else:
            print("No ranked data available for this summoner.")
        
        print("=" * 10)

main()