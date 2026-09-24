import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import streamlit as st
import plotly.express as px
from data.loader import load_data


def show():
    df = load_data()

    # --- Sidebar filter ---
    season_options = ["All", "Summer", "Winter"]
    selected_season = st.sidebar.selectbox("Season", season_options)

    if selected_season != "All":
        df_filtered = df[df["Season"] == selected_season]
    else:
        df_filtered = df

    # --- Page heading ---
    st.title("Overview")
    st.subheader("Key Statistics")

    # --- KPI totals (always over the full dataset) ---
    total_athletes = df["ID"].nunique()
    total_nations  = df["NOC"].nunique()
    total_sports   = df["Sport"].nunique()
    total_medals   = int(df["has_medal"].sum())

    # --- Filtered counts ---
    filt_athletes = df_filtered["ID"].nunique()
    filt_nations  = df_filtered["NOC"].nunique()
    filt_sports   = df_filtered["Sport"].nunique()
    filt_medals   = int(df_filtered["has_medal"].sum())

    def _delta(total_val):
        """Return delta string only when a season filter is active."""
        if selected_season == "All":
            return None
        return f"of {total_val:,} total"

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "Total Unique Athletes",
        f"{filt_athletes:,}",
        delta=_delta(total_athletes),
    )
    col2.metric(
        "Total Nations",
        f"{filt_nations:,}",
        delta=_delta(total_nations),
    )
    col3.metric(
        "Total Sports",
        f"{filt_sports:,}",
        delta=_delta(total_sports),
    )
    col4.metric(
        "Total Medals Awarded",
        f"{filt_medals:,}",
        delta=_delta(total_medals),
    )

    st.divider()

    # --- Participation trend chart ---
    st.subheader("Athlete Participation Over Time")

    participation = (
        df_filtered.groupby(["Year", "Season"])["ID"]
        .nunique()
        .reset_index()
        .rename(columns={"ID": "Athletes"})
    )

    fig = px.line(
        participation,
        x="Year",
        y="Athletes",
        color="Season",
        title="Olympic Participation Over Time",
        template="plotly_white",
        markers=True,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Each point represents the number of unique athletes who competed in a given "
        "Olympic Games (identified by year and season). Summer and Winter Games are "
        "shown in separate colours. Use the Season filter in the sidebar to focus on "
        "one season."
    )
