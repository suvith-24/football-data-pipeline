import pandas as pd
import logging
import tempfile
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO)

def get_db_engine():
    engine = create_engine("postgresql://postgres:postgres123@localhost:5433/football_dw")
    logging.info("Connected to PostgreSQL")
    return engine

def copy_dataframe_to_postgres(df, table_name, engine):
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as tmp:
        df.to_csv(tmp.name, index=False, header=False)
        conn = engine.raw_connection()
        cursor = conn.cursor()
        with open(tmp.name, "r") as f:
            cursor.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV", f)
        conn.commit()
        cursor.close()
        conn.close()

def get_last_appearance_id(engine):
    query = "SELECT MAX(appearance_id) FROM fact_player_appearances"
    try:
        last_id = pd.read_sql(query, engine).iloc[0, 0]
        if pd.isna(last_id):
            return 0
        return int(last_id)
    except:
        return 0

def load_dim_club(df, engine):
    logging.info("Loading dim_club")
    club_df = df[["club_id", "name", "competition_id"]].drop_duplicates(subset=["club_id"])
    club_df.columns = ["club_id", "club_name", "competition_id"]
    try:
        existing_ids = pd.read_sql("SELECT club_id FROM dim_club", engine)
        club_df = club_df[~club_df["club_id"].isin(existing_ids["club_id"])]
    except:
        pass
    club_df.to_sql("dim_club", engine, if_exists="append", index=False, method="multi", chunksize=1000)
    logging.info("dim_club loaded")

def load_dim_date(df, engine):
    logging.info("Loading dim_date")
    date_df = pd.DataFrame()
    date_df["date_id"] = df["date"].drop_duplicates()
    date_df["year"] = date_df["date_id"].dt.year
    date_df["month"] = date_df["date_id"].dt.month
    date_df["day"] = date_df["date_id"].dt.day
    try:
        existing_dates = pd.read_sql("SELECT date_id FROM dim_date", engine)
        existing_dates["date_id"] = pd.to_datetime(existing_dates["date_id"])
        date_df = date_df[~date_df["date_id"].isin(existing_dates["date_id"])]
    except:
        pass
    date_df.to_sql("dim_date", engine, if_exists="append", index=False, method="multi", chunksize=1000)
    logging.info("dim_date loaded")

def load_dim_competition(df, engine):
    logging.info("Loading dim_competition")
    comp_df = df[["competition_id"]].drop_duplicates()
    try:
        existing_comp = pd.read_sql("SELECT competition_id FROM dim_competition", engine)
        comp_df = comp_df[~comp_df["competition_id"].isin(existing_comp["competition_id"])]
    except:
        pass
    comp_df.to_sql("dim_competition", engine, if_exists="append", index=False, method="multi", chunksize=1000)
    logging.info("dim_competition loaded")

def load_fact_table(df, engine):
    logging.info("Loading fact_player_appearances")
    last_id = get_last_appearance_id(engine)
    print(f"Last appearance_id in warehouse: {last_id}")
    df["appearance_id"] = df["appearance_id"].astype(int)
    df["player_id"] = df["player_id"].astype(int)
    df["club_id"] = df["club_id"].astype(int)
    df["competition_id"] = df["competition_id"].astype(str)

    df = df[df["appearance_id"] > last_id]
    print("Rows before filter:", len(df))
    print("Last ID:", last_id)
    print(f"New rows to load: {len(df)}")
    if df.empty:
        print("No new data to load")
        return
    fact_df = df[[
        "appearance_id", "player_id", "club_id", "competition_id", "date",
        "goals", "assists", "yellow_cards", "red_cards", "minutes_played",
        "goal_contribution", "goals_per_90", "assists_per_90", "goal_contribution_per_90"
    ]]
    fact_df = fact_df.rename(columns={"date": "date_id"})
    copy_dataframe_to_postgres(fact_df, "fact_player_appearances", engine)
    print("COPY load completed")

def load_data(df):
    engine = get_db_engine()
    load_dim_club(df, engine)
    load_dim_date(df, engine)
    load_dim_competition(df, engine)
    load_fact_table(df, engine)
    logging.info("All warehouse tables loaded")
