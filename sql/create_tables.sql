CREATE TABLE IF NOT EXISTS dim_club (
    club_id INT PRIMARY KEY,
    club_name TEXT,
    competition_id TEXT
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_id DATE PRIMARY KEY,
    year INT,
    month INT,
    day INT
);

CREATE TABLE IF NOT EXISTS dim_competition (
    competition_id TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS fact_player_appearances (
    appearance_id TEXT PRIMARY KEY,
    player_id INT,
    club_id INT,
    competition_id TEXT,
    date_id DATE,
    goals INT,
    assists INT,
    yellow_cards INT,
    red_cards INT,
    minutes_played INT,
    goal_contribution INT,
    goals_per_90 FLOAT,
    assists_per_90 FLOAT,
    goal_contribution_per_90 FLOAT,
    FOREIGN KEY (club_id) REFERENCES dim_club(club_id),
    FOREIGN KEY (competition_id) REFERENCES dim_competition(competition_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);
