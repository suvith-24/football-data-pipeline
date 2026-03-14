import streamlit as st
import plotly.express as px
import pandas as pd
from db import get_data, get_clubs

st.set_page_config(layout="wide")

st.title("🏟 Club League Performance")
st.markdown("Explore how a **football club performs across different leagues and competitions**.")

# Load Data
df = get_data()
clubs = get_clubs()

club = st.selectbox("🔍 Search Club", clubs)

club_df = df[df["club_name"] == club]

if club_df.empty:
    st.warning("No data available for this club.")
    st.stop()

# Aggregate by League
league_stats = (
    club_df.groupby("competition_id")
    .agg({
        "goals": "sum",
        "assists": "sum",
        "cards": "sum",
        "minutes_played": "sum"
    })
    .reset_index()
)

# Goals Performance
st.subheader("⚽ Goals Scored by League")
goals_df = league_stats.sort_values("goals", ascending=False)
fig1 = px.bar(
    goals_df,
    x="competition_id",
    y="goals",
    text="goals",
    color="goals",
    color_continuous_scale="Blues"
)
st.plotly_chart(fig1, use_container_width=True)

top_league = goals_df.iloc[0]["competition_id"]
st.success(f"{club} scores the most goals in **{top_league}**, indicating strong attacking performance in this competition.")

st.divider()

# Assists Performance
st.subheader("🎯 Assists by League")
assists_df = league_stats.sort_values("assists", ascending=False)
fig2 = px.bar(
    assists_df,
    x="competition_id",
    y="assists",
    text="assists",
    color="assists",
    color_continuous_scale="Greens"
)
st.plotly_chart(fig2, use_container_width=True)

top_league = assists_df.iloc[0]["competition_id"]
st.success(f"{club} creates the most assists in **{top_league}**, suggesting stronger playmaking in this league.")

st.divider()

# Discipline
st.subheader("🟥 Cards by League")
cards_df = league_stats.sort_values("cards", ascending=False)
fig3 = px.bar(
    cards_df,
    x="competition_id",
    y="cards",
    text="cards",
    color="cards",
    color_continuous_scale="Reds"
)
st.plotly_chart(fig3, use_container_width=True)

top_league = cards_df.iloc[0]["competition_id"]
st.warning(f"{club} receives the most cards in **{top_league}**, indicating a more aggressive playing style in this competition.")

st.divider()

# Minutes Played
st.subheader("⏱ Minutes Played by League")
minutes_df = league_stats.sort_values("minutes_played", ascending=False)
fig4 = px.bar(
    minutes_df,
    x="competition_id",
    y="minutes_played",
    text="minutes_played",
    color="minutes_played",
    color_continuous_scale="Viridis"
)
st.plotly_chart(fig4, use_container_width=True)

top_league = minutes_df.iloc[0]["competition_id"]
st.info(f"{club} has accumulated the highest gameplay minutes in **{top_league}**, indicating heavier participation in this competition.")
