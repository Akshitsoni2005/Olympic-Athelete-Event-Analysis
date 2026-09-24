import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import streamlit as st
import plotly.express as px
from data.loader import load_data
from data import aggregations


def show():
    df = load_data()
    st.title("🌍 Country Analysis")

    # ------------------------------------------------------------------
    # Sidebar filters
    # ------------------------------------------------------------------
    st.sidebar.header("Filters")

    season = st.sidebar.selectbox("Season", ["All", "Summer", "Winter"])

    year_min, year_max = int(df["Year"].min()), int(df["Year"].max())
    yr = st.sidebar.slider(
        "Year range",
        min_value=1896,
        max_value=2016,
        value=(1896, 2016),
        step=4,
    )

    medal_type = st.sidebar.selectbox("Medal type", ["All", "Gold", "Silver", "Bronze"])

    # ------------------------------------------------------------------
    # Apply filters
    # ------------------------------------------------------------------
    if season != "All":
        df = df[df["Season"] == season]
    df = df[(df["Year"] >= yr[0]) & (df["Year"] <= yr[1])]

    df_medals = df[df["has_medal"] == True]
    if medal_type != "All":
        df_medals = df_medals[df_medals["Medal"] == medal_type]

    if df_medals.empty:
        st.warning("No medal data found for the selected filters. Try broadening your selection.")
        return

    # ------------------------------------------------------------------
    # Build medal tally
    # ------------------------------------------------------------------
    tally_df = aggregations.medal_tally(df_medals)

    # ------------------------------------------------------------------
    # Section 1 — Medal Tally Table + Top-20 Bar Chart
    # ------------------------------------------------------------------
    st.subheader("🏅 Medal Tally")
    col_left, col_right = st.columns([2, 3])

    with col_left:
        if medal_type == "All":
            display_cols = ["region", "Gold", "Silver", "Bronze", "Total"]
        else:
            display_cols = ["region", medal_type, "Total"]
        st.dataframe(
            tally_df[display_cols].reset_index(drop=True),
            use_container_width=True,
            height=400,
        )

    with col_right:
        top20 = tally_df.head(20).sort_values("Total", ascending=True)
        fig_bar = px.bar(
            top20,
            x="Total",
            y="region",
            orientation="h",
            title="Top 20 Nations by Medal Count",
            color="Total",
            color_continuous_scale="Oranges",
            template="plotly_white",
        )
        fig_bar.update_layout(yaxis_title="", xaxis_title="Total Medals")
        st.plotly_chart(fig_bar, use_container_width=True)

    # ------------------------------------------------------------------
    # Section 2 — Choropleth World Map
    # ------------------------------------------------------------------
    st.subheader("🗺️ Medal Count by Country")
    fig_map = px.choropleth(
        tally_df,
        locations="region",
        locationmode="country names",
        color="Total",
        hover_name="region",
        color_continuous_scale="YlOrRd",
        title="Medal Count by Country",
        template="plotly_white",
    )
    fig_map.update_layout(geo=dict(showframe=False, showcoastlines=True))
    st.plotly_chart(fig_map, use_container_width=True)

    # ------------------------------------------------------------------
    # Section 3 — Top-5 Nations Over Time
    # ------------------------------------------------------------------
    st.subheader("📈 Top 5 Nations Medal Count Over Time")
    top5_regions = tally_df.head(5)["region"].tolist()
    df_top5 = df_medals[df_medals["region"].isin(top5_regions)]

    over_time = (
        df_top5.groupby(["Year", "region"])
        .size()
        .reset_index(name="medal_count")
    )

    fig_line = px.line(
        over_time,
        x="Year",
        y="medal_count",
        color="region",
        title="Top 5 Nations Medal Count Over Time",
        template="plotly_white",
        markers=True,
    )
    fig_line.update_layout(yaxis_title="Medal Count", xaxis_title="Year")
    st.plotly_chart(fig_line, use_container_width=True)
