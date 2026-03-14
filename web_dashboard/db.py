import pandas as pd
from sqlalchemy import create_engine

# Database Connection
engine = create_engine(
    "postgresql://postgres:postgres123@localhost:5433/football_dw"
)

def get_data():
    query = """
    SELECT
        c.club_name,
        f.competition_id,
        f.goals,
        f.assists,
        f.yellow_cards,
        f.red_cards,
        f.minutes_played
    FROM fact_player_appearances f
    JOIN dim_club c
    ON f.club_id = c.club_id
    """
    df = pd.read_sql(query, engine)
    df["cards"] = df["yellow_cards"] + df["red_cards"]
    return df

def get_clubs():
    df = get_data()
    return sorted(df["club_name"].unique())

def get_leagues():
    df = get_data()
    return sorted(df["competition_id"].unique())
