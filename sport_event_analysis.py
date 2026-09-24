import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import streamlit as st
import plotly.express as px
from data.loader import load_data


def show():
    df = load_data()
    st.title("🏋️ Sport & Event Analysis")

    # ── Sidebar filters ──────────────────────────────────────────────────────
    st.sidebar.header("Filters")

    season = st.sidebar.selectbox("Season", ["All", "Summer", "Winter"])

    yr = st.sidebar.slider(
        "Year Range", min_value=1896, max_value=2016,
        value=(1896, 2016), step=4
    )

    all_sports = sorted(df["Sport"].dropna().unique().tolist())
    sport_sel = st.sidebar.multiselect("Sport", all_sports, default=[])

    # Apply filters
    if season != "All":
        df = df[df["Season"] == season]
    df = df[(df["Year"] >= yr[0]) & (df["Year"] <= yr[1])]
    if sport_sel:
        df = df[df["Sport"].isin(sport_sel)]

    if df.empty:
        st.warning("No data matches the current filters. Adjust the sidebar filters and try again.")
        return

    # ── Section 1 — Stacked Area Chart: Events per Sport over Time ───────────
    st.subheader("Events per Sport Over Time")

    top10_sports = (
        df.groupby("Sport")["Event"].nunique()
          .sort_values(ascending=False)
          .head(10).index.tolist()
    )
    area_df = (
        df[df["Sport"].isin(top10_sports)]
          .groupby(["Year", "Sport"])["Event"]
          .nunique()
          .reset_index()
          .rename(columns={"Event": "event_count"})
    )

    fig_area = px.area(
        area_df, x="Year", y="event_count", color="Sport",
        title="Number of Events per Sport Over Time (Top 10 Sports)",
        template="plotly_white"
    )
    st.plotly_chart(fig_area, use_container_width=True)

    # ── Section 2 — Medals by Sport ──────────────────────────────────────────
    st.subheader("Medals by Sport")

    medals_by_sport = (
        df[df["has_medal"] == True]
          .groupby("Sport")
          .size()
          .reset_index(name="medal_count")
          .sort_values("medal_count", ascending=False)
          .head(20)
          .sort_values("medal_count", ascending=True)   # ascending so highest is at top of bar chart
    )

    fig_bar = px.bar(
        medals_by_sport, x="medal_count", y="Sport", orientation="h",
        title="Total Medals by Sport (Top 20)",
        template="plotly_white",
        color="medal_count",
        color_continuous_scale="Teal"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # ── Section 3 — Summer vs Winter Comparison ──────────────────────────────
    st.subheader("Summer vs Winter Comparison")

    df_all_seasons = load_data()
    df_all_seasons = df_all_seasons[
        (df_all_seasons["Year"] >= yr[0]) & (df_all_seasons["Year"] <= yr[1])
    ]
    summer = df_all_seasons[df_all_seasons["Season"] == "Summer"]
    winter = df_all_seasons[df_all_seasons["Season"] == "Winter"]

    col_s, col_w = st.columns(2)
    with col_s:
        st.markdown("### ☀️ Summer Games")
        st.metric("Unique Athletes", summer["ID"].nunique())
        st.metric("Nations", summer["NOC"].nunique())
        st.metric("Sports", summer["Sport"].nunique())
        st.metric("Events", summer["Event"].nunique())
    with col_w:
        st.markdown("### ❄️ Winter Games")
        st.metric("Unique Athletes", winter["ID"].nunique())
        st.metric("Nations", winter["NOC"].nunique())
        st.metric("Sports", winter["Sport"].nunique())
        st.metric("Events", winter["Event"].nunique())

    # ── Section 4 — Event-Level Medal Breakdown Table ────────────────────────
    st.subheader("Event Medal Breakdown")

    sport_filter = st.selectbox(
        "Filter by Sport", ["All"] + sorted(df["Sport"].unique().tolist())
    )

    medal_rows = df[df["has_medal"] == True].copy()
    if sport_filter != "All":
        medal_rows = medal_rows[medal_rows["Sport"] == sport_filter]

    medal_rows = (
        medal_rows[["Year", "Games", "Sport", "Event", "Name", "Team", "Medal"]]
          .sort_values(["Year", "Event"], ascending=[False, True])
    )

    st.dataframe(medal_rows, use_container_width=True, height=350)
