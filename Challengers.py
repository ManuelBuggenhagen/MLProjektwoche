import requests
import json
import pandas as pd

def get_top_challenger_players(api_key, region="euw1", count=10):
    """
    Fetch the top challenger players in the region.

    Parameters:
        api_key (str): Riot API key.
        region (str): Region for the player data.
        count (int): Number of top players to fetch.

    Returns:
        list: A list of player PUUIDs with their respective ranks.
    """
    url = f"https://{region}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        players = response.json()["entries"]
        sorted_players = sorted(players, key=lambda x: x["leaguePoints"], reverse=True)[:count]
        return [(player["summonerId"], "Challenger") for player in sorted_players]
    else:
        raise Exception(f"Failed to fetch challenger players: {response.status_code} - {response.text}")

def get_puuid_from_summoner_id(api_key, summoner_id, region="euw1"):
    """
    Get the PUUID of a player from their Summoner ID.

    Parameters:
        api_key (str): Riot API key.
        summoner_id (str): Player's Summoner ID.
        region (str): Region for the player data.

    Returns:
        str: The PUUID of the player.
    """
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["puuid"]
    else:
        raise Exception(f"Failed to fetch PUUID: {response.status_code} - {response.text}")

def get_match_ids(api_key, puuid, region="europe", count=20):
    """
    Fetch a list of match IDs for a given player PUUID.

    Parameters:
        api_key (str): Riot API key.
        puuid (str): Player's PUUID.
        region (str): Region for the match data.
        count (int): Number of matches to retrieve.

    Returns:
        list: A list of match IDs.
    """
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch match IDs: {response.status_code} - {response.text}")

def get_match_data(api_key, match_id, region="europe"):
    """
    Fetch the data for a specific match.

    Parameters:
        api_key (str): Riot API key.
        match_id (str): Match ID.
        region (str): Region for the match data.

    Returns:
        dict: The match data.
    """
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch match data: {response.status_code} - {response.text}")

def get_match_timeline(api_key, match_id, region="europe"):
    """
    Fetch the timeline for a specific match.

    Parameters:
        api_key (str): Riot API key.
        match_id (str): Match ID.
        region (str): Region for the match data.

    Returns:
        dict: The match timeline data.
    """
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch match timeline: {response.status_code} - {response.text}")

def extract_gold_stats_from_timeline(timeline_data):
    """
    Extract gold statistics from a match timeline JSON data.

    Parameters:
        timeline_data (dict): Match timeline JSON data.

    Returns:
        pd.DataFrame: A DataFrame containing the gold statistics for each minute.
    """
    frames = timeline_data["info"]["frames"]
    gold_stats = []
    for frame in frames:
        timestamp = frame["timestamp"] // 60000  # Convert timestamp to minutes
        team1_gold = sum(frame["participantFrames"][str(i)]["totalGold"] for i in range(1, 6))
        team2_gold = sum(frame["participantFrames"][str(i)]["totalGold"] for i in range(6, 11))
        gold_stats.append({"Minute": timestamp, "Team1 Gold": team1_gold, "Team2 Gold": team2_gold})

    return pd.DataFrame(gold_stats)

def fetch_and_analyze_top_challenger_games(api_key, region="euw1", count=10, match_count=20, output_csv_path=None):
    """
    Fetch the top challenger players' recent games and analyze gold statistics.

    Parameters:
        api_key (str): Riot API key.
        region (str): Region for the data.
        count (int): Number of top players to analyze.
        match_count (int): Number of matches per player to analyze.
        output_csv_path (str, optional): Path to save the combined data as a CSV file.

    Returns:
        pd.DataFrame: Combined gold statistics for all matches.
    """
    # Get top challenger players
    summoner_rank_info = get_top_challenger_players(api_key, region, count)
    all_gold_stats = []

    for summoner_id, rank in summoner_rank_info:
        try:
            puuid = get_puuid_from_summoner_id(api_key, summoner_id, region)
            match_ids = get_match_ids(api_key, puuid, region="europe", count=match_count)

            for match_id in match_ids:
                try:
                    match_data = get_match_data(api_key, match_id, region="europe")
                    timeline_data = get_match_timeline(api_key, match_id, region="europe")
                    gold_stats_df = extract_gold_stats_from_timeline(timeline_data)

                    # Extract W/L and winning team
                    team1_win = match_data["info"]["teams"][0]["win"]
                    winning_team = "Team1" if team1_win else "Team2"
                    result = "W" if team1_win else "L"

                    #gold_stats_df["Match ID"] = match_id
                    #gold_stats_df["Player"] = puuid
                    #gold_stats_df["Result"] = result
                    gold_stats_df["Winning Team"] = winning_team
                    #gold_stats_df["Rank"] = rank

                    all_gold_stats.append(gold_stats_df)
                except Exception as e:
                    print(f"Error processing match {match_id}: {e}")
        except Exception as e:
            print(f"Error processing summoner {summoner_id}: {e}")

    combined_gold_stats = pd.concat(all_gold_stats, ignore_index=True)

    if output_csv_path:
        combined_gold_stats.to_csv(output_csv_path, index=False)

    return combined_gold_stats

# Example usage
if __name__ == "__main__":
    api_key = "RGAPI-b3a050c5-1b1c-49f9-a414-2cb6c7061aed"  # Replace with your Riot API key
    output_csv_path = "gold_stats_challenger.csv"  # Replace with your desired output CSV path

    combined_gold_stats_df = fetch_and_analyze_top_challenger_games(api_key, output_csv_path=output_csv_path)
    print(combined_gold_stats_df.head())