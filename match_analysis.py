"""MatchLens milestone 1: load one StatsBomb match and print basic shot statistics.

Data: StatsBomb Open Data (see data/SOURCE.md). Raw files live in data/raw/,
which is git-ignored because the licence does not allow redistributing them.
"""

import json
import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data" / "raw"

COMPETITION_ID = 2   # Premier League
SEASON_ID = 27       # 2015/2016
MATCH_ID = 3754013   # Leicester City vs Chelsea, 2015-12-14

SHOOTOUT_PERIOD = 5  # StatsBomb period 5 = penalty shootout


def load_json(path):
    """Read a JSON file and return the Python object inside it."""
    if not path.exists():
        sys.exit(f"Missing data file: {path}\nDownload it first (see data/SOURCE.md).")
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def find_match(matches, match_id):
    """Return the match dictionary with the given ID, or stop with an error."""
    for match in matches:
        if match["match_id"] == match_id:
            return match
    sys.exit(f"Match {match_id} not found in the match list.")


def summarize_shots(events, team_names):
    """Count shots, shot goals and xG per team, skipping shootout events."""
    stats = {}
    for name in team_names:
        stats[name] = {"shots": 0, "goals": 0, "xg": 0.0, "missing_xg": 0}

    for event in events:
        if event["period"] == SHOOTOUT_PERIOD:
            continue
        if event["type"]["name"] != "Shot":
            continue

        team = stats[event["team"]["name"]]
        team["shots"] += 1
        if event["shot"]["outcome"]["name"] == "Goal":
            team["goals"] += 1

        xg = event["shot"].get("statsbomb_xg")
        if xg is None:
            team["missing_xg"] += 1
        else:
            team["xg"] += xg

    return stats


def main():
    matches = load_json(DATA_DIR / "matches" / str(COMPETITION_ID) / f"{SEASON_ID}.json")
    events = load_json(DATA_DIR / "events" / f"{MATCH_ID}.json")

    match = find_match(matches, MATCH_ID)
    home = match["home_team"]["home_team_name"]
    away = match["away_team"]["away_team_name"]

    print("MatchLens: match analysis")
    print(f"{match['competition']['competition_name']} {match['season']['season_name']}, {match['match_date']}")
    print(f"Final score: {home} {match['home_score']}-{match['away_score']} {away}")
    print(f"Total events: {len(events)}")

    shootout_events = sum(1 for e in events if e["period"] == SHOOTOUT_PERIOD)
    print(f"Shootout events excluded: {shootout_events}")
    print()

    stats = summarize_shots(events, [home, away])
    for team_name, team in stats.items():
        print(f"{team_name}: {team['shots']} shots, {team['goals']} shot goals, xG {team['xg']:.2f}")
        if team["missing_xg"]:
            print(f"  Warning: {team['missing_xg']} shots have no xG; xG total covers the rest only.")

    shot_goals = (stats[home]["goals"], stats[away]["goals"])
    if shot_goals != (match["home_score"], match["away_score"]):
        print(
            f"\nNote: shot goals ({shot_goals[0]}-{shot_goals[1]}) differ from the official "
            f"final score ({match['home_score']}-{match['away_score']}). "
            "The cause is not yet determined; check the event records."
        )


if __name__ == "__main__":
    main()
