import requests
import json
import pandas as pd


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


def get_match_data(api_key, match_id, region):
    """
    Fetch match data for a given match ID.

    Parameters:
        api_key (str): Riot API key.
        match_id (str): Match ID to fetch.
        region (str): Region for the match data.

    Returns:
        dict: Match data.
    """

    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()



def extract_gold_stats_from_timeline(timeline_data, match_data):
    """
    Extract gold statistics from a match timeline JSON data.

    Parameters:
        timeline_data (dict): Match timeline JSON data.

    Returns:
        pd.DataFrame: A DataFrame containing the gold statistics for each minute.
    """
    teams = match_data["info"]["teams"]
    winning_team = "Team1" if teams[0]["win"] else "Team2"

    frames = timeline_data["info"]["frames"]
    gold_stats = []
    for frame in frames:
        timestamp = frame["timestamp"] // 60000  # Convert timestamp to minutes
        team1_gold = sum(frame["participantFrames"][str(i)]["totalGold"] for i in range(1, 6))
        team2_gold = sum(frame["participantFrames"][str(i)]["totalGold"] for i in range(6, 11))
        gold_stats.append({"Minute": timestamp, "Team1 Gold": team1_gold, "Team2 Gold": team2_gold})

    df = pd.DataFrame(gold_stats)
    df["Winning Team"] = winning_team
    return df


def fetch_and_extract_all_gold_stats(api_key, puuid, region="europe", count=20, output_csv_path=None):
    """
    Fetch all match timelines for a player and extract gold statistics.

    Parameters:
        api_key (str): Riot API key.
        puuid (str): Player's PUUID.
        region (str): Region for the match data.
        count (int): Number of matches to process.
        output_csv_path (str, optional): Path to save the combined gold stats as a CSV file.

    Returns:
        pd.DataFrame: Combined gold statistics for all matches.
    """
    match_ids = get_match_ids(api_key, puuid, region, count)
    all_gold_stats = []

    for match_id in match_ids:
        try:
            match_data = get_match_data(api_key, match_id, region)
            timeline_data = get_match_timeline(api_key, match_id, region)

            gold_stats_df = extract_gold_stats_from_timeline(timeline_data,match_data)
            #gold_stats_df["Match ID"] = match_id
            all_gold_stats.append(gold_stats_df)
        except Exception as e:
            print(f"Error processing match {match_id}: {e}")

    combined_gold_stats = pd.concat(all_gold_stats, ignore_index=True)

    if output_csv_path:
        combined_gold_stats.to_csv(output_csv_path, index=False)

    return combined_gold_stats


if __name__ == "__main__":
    api_key = "RGAPI-b3a050c5-1b1c-49f9-a414-2cb6c7061aed"
    puuid = "r_nM2wBLPJrz1FNlrVUEyIf7nDWrgqxoS-kQG9oQeWiZdom6SdJ76PbcgGyIsW31A_jou2wrEx3A6w"
    output_csv_path = "gold_stats_my_games.csv"

    combined_gold_stats_df = fetch_and_extract_all_gold_stats(api_key, puuid, output_csv_path=output_csv_path)
    print(combined_gold_stats_df)
