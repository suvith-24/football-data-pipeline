import pandas as pd
import logging

def clean_appearances(df):
    logging.info("Cleaning appearances dataset")
    df["date"] = pd.to_datetime(df["date"])
    df = df[df["player_id"].notnull()]
    df = df[df["minutes_played"] >= 0]
    df["goals"] = df["goals"].fillna(0)
    df["assists"] = df["assists"].fillna(0)
    df["yellow_cards"] = df["yellow_cards"].fillna(0)
    df["red_cards"] = df["red_cards"].fillna(0)
    logging.info("Appearances data cleaned")
    return df

def clean_clubs(df):
    logging.info("Cleaning clubs dataset")
    df = df.drop_duplicates(subset="club_id")
    df["name"] = df["name"].str.strip()
    logging.info("Clubs data cleaned")
    return df

def create_features(df):
    logging.info("Creating analytics features")
    df["goal_contribution"] = df["goals"] + df["assists"]
    df["goals_per_90"] = (df["goals"] / df["minutes_played"]) * 90
    df["assists_per_90"] = (df["assists"] / df["minutes_played"]) * 90
    df["goal_contribution_per_90"] = (df["goal_contribution"] / df["minutes_played"]) * 90
    df = df.fillna(0)
    logging.info("Feature engineering complete")
    return df

def join_datasets(appearances, clubs):
    logging.info("Joining appearances with clubs")

    merged_df = appearances.merge(
        clubs,
        left_on="player_club_id",
        right_on="club_id",
        how="left"
    )

    print("Rows after merge:", len(merged_df))
    print("Rows with club match:", merged_df["club_id"].notnull().sum())

    # Drop rows where club didn't match
    merged_df = merged_df.dropna(subset=["club_id"])

    logging.info("Datasets merged successfully")
    return merged_df



def transform_data(appearances_df, clubs_df):
    appearances_df = clean_appearances(appearances_df)
    clubs_df = clean_clubs(clubs_df)
    appearances_df = create_features(appearances_df)
    final_df = join_datasets(appearances_df, clubs_df)
    logging.info("Transformation completed")
    return final_df
