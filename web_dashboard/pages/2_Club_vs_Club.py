import streamlit as st
import plotly.express as px
import pandas as pd
from db import get_data, get_clubs

st.set_page_config(layout="wide")

st.title("⚔️ Club vs Club Comparison")
st.markdown("Compare two football clubs across **goals, assists, discipline, and playtime intensity**.")

# Load Data
df = get_data()
clubs = get_clubs()

col1, col2 = st.columns(2)
club1 = col1.selectbox("Select Club 1", clubs, index=0)
club2 = col2.selectbox("Select Club 2", clubs, index=1)

df1 = df[df["club_name"] == club1]
df2 = df[df["club_name"] == club2]

# Calculate Metrics
metrics = {
    "Goals": [df1["goals"].sum(), df2["goals"].sum()],
    "Assists": [df1["assists"].sum(), df2["assists"].sum()],
    "Cards": [df1["cards"].sum(), df2["cards"].sum()],
    "Minutes Played": [df1["minutes_played"].sum(), df2["minutes_played"].sum()],
}
clubs_compare = [club1, club2]

# Goals Comparison
st.subheader("⚽ Goals Comparison")
goals_df = pd.DataFrame({
    "Club": clubs_compare,
    "Goals": metrics["Goals"]
}).sort_values("Goals", ascending=False)

fig1 = px.bar(
    goals_df,
    x="Club",
    y="Goals",
    text="Goals",
    color="Goals",
    color_continuous_scale="Blues"
)
st.plotly_chart(fig1, use_container_width=True)

if metrics["Goals"][0] > metrics["Goals"][1]:
    st.success(f"Insight: **{club1}** has scored more goals and shows stronger attacking performance.")
elif metrics["Goals"][1] > metrics["Goals"][0]:
    st.success(f"Insight: **{club2}** leads in offensive strength with more goals scored.")
else:
    st.info("Insight: Both clubs have identical goal-scoring records.")

st.divider()

# Assists Comparison
st.subheader("🎯 Assists Comparison")
assists_df = pd.DataFrame({
    "Club": clubs_compare,
    "Assists": metrics["Assists"]
}).sort_values("Assists", ascending=False)

fig2 = px.bar(
    assists_df,
    x="Club",
    y="Assists",
    text="Assists",
    color="Assists",
    color_continuous_scale="Greens"
)
st.plotly_chart(fig2, use_container_width=True)

if metrics["Assists"][0] > metrics["Assists"][1]:
    st.success(f"Insight: **{club1}** demonstrates stronger playmaking ability with more assists.")
elif metrics["Assists"][1] > metrics["Assists"][0]:
    st.success(f"Insight: **{club2}** appears more creative in building goal opportunities.")
else:
    st.info("Insight: Both clubs have equal assist records.")

st.divider()

# Cards Comparison
st.subheader("🟥 Discipline Comparison (Cards)")
cards_df = pd.DataFrame({
    "Club": clubs_compare,
    "Cards": metrics["Cards"]
}).sort_values("Cards", ascending=False)

fig3 = px.bar(
    cards_df,
    x="Club",
    y="Cards",
    text="Cards",
    color="Cards",
    color_continuous_scale="Reds"
)
st.plotly_chart(fig3, use_container_width=True)

if metrics["Cards"][0] > metrics["Cards"][1]:
    st.warning(f"Insight: **{club1}** plays more aggressively based on card accumulation.")
elif metrics["Cards"][1] > metrics["Cards"][0]:
    st.warning(f"Insight: **{club2}** appears to adopt a more aggressive playing style.")
else:
    st.info("Insight: Both clubs show identical disciplinary records.")

st.divider()

# Minutes Played Comparison
st.subheader("⏱ Gameplay Intensity (Minutes Played)")
minutes_df = pd.DataFrame({
    "Club": clubs_compare,
    "Minutes Played": metrics["Minutes Played"]
}).sort_values("Minutes Played", ascending=False)

fig4 = px.bar(
    minutes_df,
    x="Club",
    y="Minutes Played",
    text="Minutes Played",
    color="Minutes Played",
    color_continuous_scale="Viridis"
)
st.plotly_chart(fig4, use_container_width=True)

if metrics["Minutes Played"][0] > metrics["Minutes Played"][1]:
    st.info(f"Insight: **{club1}** has accumulated more total playing minutes, indicating greater participation across matches.")
elif metrics["Minutes Played"][1] > metrics["Minutes Played"][0]:
    st.info(f"Insight: **{club2}** shows higher gameplay intensity based on total minutes played.")
else:
    st.info("Insight: Both clubs have identical gameplay duration.")
