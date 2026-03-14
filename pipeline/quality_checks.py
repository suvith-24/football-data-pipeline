import logging

def check_player_id(df):
    logging.info("Checking player_id values")
    if df["player_id"].isnull().sum() > 0:
        logging.error("player_id contains NULL values")
        raise ValueError("Data Quality Error: player_id contains NULL values")
    logging.info("player_id validation passed")

def check_minutes(df):
    logging.info("Checking minutes_played")
    if (df["minutes_played"] < 0).sum() > 0:
        logging.error("Negative minutes detected")
        raise ValueError("Data Quality Error: minutes_played cannot be negative")
    logging.info("minutes_played validation passed")

def check_goals(df):
    logging.info("Checking goals column")
    if (df["goals"] < 0).sum() > 0:
        logging.error("Negative goals detected")
        raise ValueError("Data Quality Error: goals cannot be negative")
    logging.info("goals validation passed")

def check_assists(df):
    logging.info("Checking assists column")
    if (df["assists"] < 0).sum() > 0:
        logging.error("Negative assists detected")
        raise ValueError("Data Quality Error: assists cannot be negative")
    logging.info("assists validation passed")

def check_club_ids(df):
    logging.info("Checking club_id relationships")
    if df["club_id"].isnull().sum() > 0:
        logging.error("Some records have invalid club_id")
        raise ValueError("Data Quality Error: club_id missing after join")
    logging.info("club_id validation passed")

def run_quality_checks(df):
    logging.info("Starting data quality checks")
    check_player_id(df)
    check_minutes(df)
    check_goals(df)
    check_assists(df)
    check_club_ids(df)
    logging.info("All data quality checks passed")
