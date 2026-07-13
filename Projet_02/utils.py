"""Utility functions for Project 02 - World Cup 2030 prediction.

This module contains the "plumbing" code of the project: useful, but not
essential to understand the machine learning workflow. It lives here to
keep the main notebook readable. Curious? Feel free to read the functions!
"""

from collections import defaultdict, deque

import pandas as pd

DATA_URL = "https://github.com/martj42/international_results"

FLAGS = {
    "Spain": "🇪🇸", "Portugal": "🇵🇹", "Morocco": "🇲🇦", "France": "🇫🇷",
    "Brazil": "🇧🇷", "Argentina": "🇦🇷", "England": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Germany": "🇩🇪",
    "Netherlands": "🇳🇱", "Belgium": "🇧🇪", "Croatia": "🇭🇷", "Italy": "🇮🇹",
    "Uruguay": "🇺🇾", "Colombia": "🇨🇴", "Japan": "🇯🇵", "United States": "🇺🇸",
    "Mexico": "🇲🇽", "Senegal": "🇸🇳", "Switzerland": "🇨🇭", "Denmark": "🇩🇰",
    "South Korea": "🇰🇷", "Australia": "🇦🇺", "Canada": "🇨🇦", "Ghana": "🇬🇭",
    "Poland": "🇵🇱", "Austria": "🇦🇹", "Turkey": "🇹🇷", "Ecuador": "🇪🇨",
    "Nigeria": "🇳🇬", "Serbia": "🇷🇸", "Greece": "🇬🇷", "Egypt": "🇪🇬",
}

ROUND_NAMES = [
    "Seizièmes de finale",
    "Huitièmes de finale",
    "Quarts de finale",
    "Demi-finales",
    "Finale",
]


def load_results(path="data/results.csv"):
    """Load the international results dataset and parse dates.

    Arguments:
    path -- location of the results.csv file

    Returns:
    df -- DataFrame with one row per international match, sorted by date,
          with an extra 'year' column
    """
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Le fichier '{path}' est introuvable. Télécharge 'results.csv' "
            f"depuis {DATA_URL} et place-le dans le dossier 'data/' du projet "
            "(voir les instructions de la Partie 1 du notebook)."
        ) from None
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    return df.sort_values("date").reset_index(drop=True)


def _points(goals_for, goals_against):
    """Return the number of points earned for one match (3/1/0)."""
    if goals_for > goals_against:
        return 3
    if goals_for == goals_against:
        return 1
    return 0


def add_recent_form(df, window=10, min_matches=5):
    """Add each team's recent form (computed BEFORE the match) to every row.

    For both teams of each match, computes the average points, goals scored
    and goals conceded over their last `window` matches. Rows where a team
    has played fewer than `min_matches` past matches are filled with NaN.

    Arguments:
    df -- match DataFrame, sorted by date
    window -- number of past matches used to compute the form
    min_matches -- minimum history required, otherwise NaN

    Returns:
    df -- copy of the input with 6 new columns:
          home_avg_points, home_avg_goals_scored, home_avg_goals_conceded,
          away_avg_points, away_avg_goals_scored, away_avg_goals_conceded
    """
    history = defaultdict(lambda: deque(maxlen=window))
    new_columns = []

    for row in df.itertuples():
        features = {}
        for side, team in [("home", row.home_team), ("away", row.away_team)]:
            past = history[team]
            if len(past) >= min_matches:
                features[f"{side}_avg_points"] = sum(m[0] for m in past) / len(past)
                features[f"{side}_avg_goals_scored"] = sum(m[1] for m in past) / len(past)
                features[f"{side}_avg_goals_conceded"] = sum(m[2] for m in past) / len(past)
        new_columns.append(features)

        for team, goals_for, goals_against in [
            (row.home_team, row.home_score, row.away_score),
            (row.away_team, row.away_score, row.home_score),
        ]:
            history[team].append((_points(goals_for, goals_against), goals_for, goals_against))

    form_df = pd.DataFrame(new_columns, index=df.index)
    return pd.concat([df, form_df], axis=1)


def get_current_form(df, team, window=10):
    """Compute a team's current form from its most recent matches.

    Arguments:
    df -- match DataFrame, sorted by date
    team -- team name, e.g. 'France'
    window -- number of most recent matches to use

    Returns:
    form -- dict with keys 'avg_points', 'avg_goals_scored', 'avg_goals_conceded'
    """
    mask = (df["home_team"] == team) | (df["away_team"] == team)
    last_matches = df[mask].tail(window)
    if last_matches.empty:
        raise ValueError(f"Aucun match trouvé pour l'équipe '{team}'. Vérifie l'orthographe (noms en anglais).")

    points, scored, conceded = [], [], []
    for row in last_matches.itertuples():
        if row.home_team == team:
            goals_for, goals_against = row.home_score, row.away_score
        else:
            goals_for, goals_against = row.away_score, row.home_score
        points.append(_points(goals_for, goals_against))
        scored.append(goals_for)
        conceded.append(goals_against)

    n = len(points)
    return {
        "avg_points": sum(points) / n,
        "avg_goals_scored": sum(scored) / n,
        "avg_goals_conceded": sum(conceded) / n,
    }


def team_label(team):
    """Return the team name with its flag emoji, e.g. '🇫🇷 France'."""
    return f"{FLAGS.get(team, '🏳️')} {team}"


def print_round(round_name, match_results):
    """Pretty-print one round of the tournament.

    Arguments:
    round_name -- name of the round, e.g. 'Quarts de finale'
    match_results -- list of tuples (team_a, team_b, winner, win_probability)
    """
    print(f"\n{'=' * 60}")
    print(f"  {round_name.upper()}")
    print("=" * 60)
    for team_a, team_b, winner, probability in match_results:
        line = f"{team_label(team_a):<22} vs {team_label(team_b):<22}"
        print(f"{line} -> {team_label(winner)} ({probability:.0%})")


def print_champion(team):
    """Pretty-print the tournament winner."""
    print(f"\n{'*' * 60}")
    print(f"   🏆 CHAMPION DU MONDE 2030 : {team_label(team).upper()} 🏆")
    print("*" * 60)
