import requests
import json
import pandas as pd


def get_puuid_from_id(api_key, summoner_id, region="euw1"):
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()["puuid"]
    else:
        raise Exception(f"Failed to fetch PUUID: {response.status_code} - {response.text}")


def get_players(api_key, tier, region="euw1", division="IV", queue="RANKED_SOLO_5x5", count=10):
    url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/{queue}/{tier}/{division}?page=1"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        summoners = response.json()
        if not summoners:
            print("No summoners found for the specified tier/division.")
            return []

        puuids = []
        for summoner in summoners[:count]:
            if "summonerId" in summoner:
                try:
                    puuid = get_puuid_from_id(api_key, summoner["summonerId"], region)
                    puuids.append(puuid)
                except Exception as e:
                    print(f"Error fetching puuid for summonerId {summoner['summonerId']}: {e}")
            else:
                print(f"Warning: Missing 'summonerId' for a summoner entry. Skipping.")
                print("Summoner data:", summoner)

        return puuids
    else:
        raise Exception(f"Failed to fetch Bronze players: {response.status_code} - {response.text}")


def get_match_ids(api_key, puuid, region="europe", count=20):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch match IDs: {response.status_code} - {response.text}")


def get_match_data(api_key, match_id, region="europe"):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_match_timeline(api_key, match_id, region="europe"):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline"
    headers = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch match timeline: {response.status_code} - {response.text}")


def extract_stats_for_one_match2(timeline_data, match_data):
    teams = match_data["info"]["teams"]
    winning_team = "Team1" if teams[0]["win"] else "Team2"
    frames = timeline_data["info"]["frames"]

    stats = []
    for frame in frames:
        timestamp = frame["timestamp"] // 60000  # Convert timestamp to minutes
        team1_gold = sum(frame["participantFrames"][str(i)]["totalGold"] for i in range(1, 6))
        team2_gold = sum(frame["participantFrames"][str(i)]["totalGold"] for i in range(6, 11))
        stats.append({"Minute": timestamp, "Team1 Gold": team1_gold, "Team2 Gold": team2_gold})

    df = pd.DataFrame(stats)
    df["Winner"] = winning_team
    df = df.set_index('Minute')
    return df


def extract_stats_for_one_match(timeline_data, match_data):
    teams = match_data["info"]["teams"]
    winning_team = "Team1" if teams[0]["win"] else "Team2"
    frames = timeline_data["info"]["frames"]
    participants = match_data["info"]["participants"]

    player_mapping = {participant["participantId"]: {
        "team": "Team1" if participant["participantId"] <= 5 else "Team2",
        "lane": participant["lane"],
        "role": participant["role"]
    } for participant in participants}

    team1_kills = 0
    team2_kills = 0
    team1_turrets_kills = 0
    team2_turrets_kills = 0
    team1_inhibitors_kills = 0
    team2_inhibitors_kills = 0
    team1_dragon_kills = 0
    team2_dragon_kills = 0
    team1_nash_kills = 0
    team2_nash_kills = 0
    team1_elder_kills = 0
    team2_elder_kills = 0

    dragon_types = {"WATER_DRAGON", "FIRE_DRAGON", "EARTH_DRAGON", "AIR_DRAGON", "CHEMTECH_DRAGON", "HEXTECH_DRAGON"}
    stats = []
    for frame in frames:
        timestamp = frame["timestamp"] // 60000  # millisecond to min
        player_stats = {"Minute": timestamp}
        team1_gold_total = 0
        team2_gold_total = 0
        team1_total_level = 0
        team2_total_level = 0

        for participant_id, info in player_mapping.items():
            team = info["team"]
            lane = info["lane"]
            role = info["role"]
            player_key = f"{team}:{lane}:{role}"
            participant_frame = frame["participantFrames"][str(participant_id)]
            gold = participant_frame["totalGold"]
            level = participant_frame["level"]
            player_stats[player_key] = gold

            if team == "Team1":
                team1_gold_total += gold
                team1_total_level += level
            else:
                team2_gold_total += gold
                team2_total_level += level

        if "events" in frame:
            for event in frame["events"]:
                # Champion Kills
                if event["type"] == "CHAMPION_KILL":
                    killer_id = event.get("killerId", 0)
                    if killer_id <= 5:
                        team1_kills += 1
                    else:
                        team2_kills += 1

                # Structure Kills
                if event["type"] == "BUILDING_KILL":
                    print(event.get("buildingType"))
                    if event.get("buildingType") == "TOWER_BUILDING":
                        if event["killerId"] <= 5:
                            team1_turrets_kills += 1
                        else:
                            team2_turrets_kills += 1
                    elif event["buildingType"] == "INHIBITOR_BUILDING":
                        if event["killerId"] <= 5:
                            team1_inhibitors_kills += 1
                        else:
                            team2_inhibitors_kills += 1

                # Monster Kills
                if event["type"] == "ELITE_MONSTER_KILL":
                    print(event.get("monsterType"))
                    print(event.get("monsterSubType"))
                    # elemental drake kill
                    if event.get("monsterSubType") in dragon_types:
                        if event["killerId"] <= 5:
                            team1_dragon_kills += 1
                        else:
                            team2_dragon_kills += 1
                    # elder drake kills
                    elif event.get("monsterSubType") == "ELDER_DRAGON":
                        if event["killerId"] <= 5:
                            team1_elder_kills += 1
                        else:
                            team2_elder_kills += 1
                    # Baron Nashor kills
                    if event.get("monsterType") == "BARON_NASHOR":
                        if event["killerId"] <= 5:
                            team1_nash_kills += 1
                        else:
                            team2_nash_kills += 1

        team1_avg_level = team1_total_level / 5
        team2_avg_level = team2_total_level / 5

        player_stats["Team1:Gold"] = team1_gold_total
        player_stats["Team2:Gold"] = team2_gold_total
        player_stats["Team1:Kills"] = team1_kills
        player_stats["Team2:Kills"] = team2_kills
        player_stats["Team1:TurretsKills"] = team1_turrets_kills
        player_stats["Team2:TurretsKills"] = team2_turrets_kills
        player_stats["Team1:InhibitorsKills"] = team1_inhibitors_kills
        player_stats["Team2:Inhibitors:Kills"] = team2_inhibitors_kills
        player_stats["Team1:DragonKills"] = team1_dragon_kills
        player_stats["Team2:DragonKills"] = team2_dragon_kills
        player_stats["Team1:ElderDragonKills"] = team1_elder_kills
        player_stats["Team2:ElderDragonKills"] = team2_elder_kills
        player_stats["Team1:BaronKills"] = team1_nash_kills
        player_stats["Team2:BaronKills"] = team2_nash_kills
        player_stats["Team1:AverageLevel"] = team1_avg_level
        player_stats["Team2:AverageLevel"] = team2_avg_level

        stats.append(player_stats)

    df = pd.DataFrame(stats)
    df["Winner"] = winning_team
    df = df.set_index("Minute")
    return df


def extract_relevant_stats_all_matches(api_key, match_ids, region="europe"):
    all_stats = []

    for match_id in match_ids:
        try:
            match_data = get_match_data(api_key, match_id, region)
            timeline_data = get_match_timeline(api_key, match_id, region)

            gold_stats_df = extract_stats_for_one_match(timeline_data, match_data)
            gold_stats_df["Match ID"] = match_id
            all_stats.append(gold_stats_df)
        except Exception as e:
            print(f"Error processing match {match_id}: {e}")

    combined_gold_stats = pd.concat(all_stats, ignore_index=True)
    return combined_gold_stats


# main execution part
if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)
    api_key = "RGAPI-6eaec9c2-0c17-49dd-8e22-a69cb81225b3"
    try:
        # get players of specific skill level
        bronze_puuids = get_players(api_key, tier="BRONZE", count=10)
        print(f"{len(bronze_puuids)} Bronze (low elo) Players PUUIDs: \n", bronze_puuids, "\n")

        platinum_puuids = get_players(api_key, tier="PLATINUM", count=10)
        print(f"{len(platinum_puuids)} Platin (mid elo) Players PUUIDs:  \n", platinum_puuids, "\n")

        diamond_puuids = get_players(api_key, tier="DIAMOND", count=10)
        print(f"{len(diamond_puuids)} Diamond(high elo) Players PUUIDs: \n ", diamond_puuids, "\n")

        # get match ids for a puuid
        # ape elo
        bronze_match_ids = []
        for puuidB in bronze_puuids:
            match_id = get_match_ids(api_key, puuidB, count=10)
            bronze_match_ids.extend(match_id)
        print(f"last {len(bronze_match_ids)} game IDs of all bronze players:\n", bronze_match_ids, "\n")

        # human elo
        platinum_match_ids = []
        for puuidP in platinum_puuids:
            match_id = get_match_ids(api_key, puuidP, count=10)
            platinum_match_ids.extend(match_id)
        print(f"last {len(platinum_match_ids)} game IDs of all platinum players:\n", platinum_match_ids, "\n")

        # superhuman elo
        diamond_match_ids = []
        for puuidD in diamond_puuids:
            match_id = get_match_ids(api_key, puuidD, count=10)
            diamond_match_ids.extend(match_id)
        print(f"last {len(diamond_match_ids)} game IDs of all diamond players:\n", diamond_match_ids, "\n")

        # test work in progress
        timeline_data = get_match_timeline(api_key, "EUW1_7176868282", "EUROPE")
        match_data = get_match_data(api_key, "EUW1_7176868282", "EUROPE")
        dataTest = extract_stats_for_one_match(timeline_data, match_data)
        dataTest["GameID"] = "EUW1_7176868282"
        print(dataTest)

    except Exception as e:
        print("Error:", e)
