import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import streamlit as st
import plotly.express as px
from data.loader import load_data


def show():
    df = load_data()

    st.title("🔍 Athlete Explorer")
    st.markdown("Search for any Olympic athlete by name to explore their career.")

    # ------------------------------------------------------------------
    # Step 1 — Name Search
    # ------------------------------------------------------------------
    search_query = st.text_input("🔍 Search Athlete Name", placeholder="e.g. Michael Phelps")

    if not search_query or len(search_query) < 2:
        st.info("Enter at least 2 characters to search.")
        return

    matches = df[df["Name"].str.contains(search_query, case=False, na=False, regex=False)]

    if matches.empty:
        st.warning(f"No athletes found matching '{search_query}'.")
        return

    # ------------------------------------------------------------------
    # Step 2 — Athlete Selection
    # ------------------------------------------------------------------
    unique_names = sorted(matches["Name"].unique().tolist())

    if len(unique_names) == 1:
        selected_name = unique_names[0]
    else:
        selected_name = st.selectbox(
            f"Found {len(unique_names)} athletes — select one:", unique_names
        )

    athlete_df = df[df["Name"] == selected_name]
    athlete_id = athlete_df["ID"].iloc[0]
    athlete_df = df[df["ID"] == athlete_id]

    # ------------------------------------------------------------------
    # Step 3 — Bio Card
    # ------------------------------------------------------------------
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Name", selected_name)
    col2.metric("Sex", athlete_df["Sex"].iloc[0])
    col3.metric("Team", athlete_df["Team"].iloc[0])
    col4.metric("NOC", athlete_df["NOC"].iloc[0])

    col5, col6, col7, col8 = st.columns(4)
    years_active = f"{int(athlete_df['Year'].min())} – {int(athlete_df['Year'].max())}"
    total_medals = int(athlete_df["has_medal"].sum())
    unique_sports = ", ".join(sorted(athlete_df["Sport"].unique().tolist()))
    games_count = athlete_df["Games"].nunique()

    col5.metric("Years Active", years_active)
    col6.metric("Olympic Appearances", games_count)
    col7.metric("Total Medals", total_medals)
    col8.metric("Sport(s)", unique_sports)

    st.divider()

    # ------------------------------------------------------------------
    # Step 4 — Career Timeline Chart
    # ------------------------------------------------------------------
    timeline = (
        athlete_df.groupby("Year")
        .agg(events=("Event", "count"), medals=("has_medal", "sum"))
        .reset_index()
    )

    fig = px.bar(
        timeline,
        x="Year",
        y="events",
        color="medals",
        color_continuous_scale="YlOrRd",
        title=f"{selected_name} — Olympic Career Timeline",
        labels={"events": "Events Competed", "medals": "Medals Won"},
        template="plotly_white",
    )
    fig.update_layout(xaxis=dict(tickmode="linear", dtick=4))
    st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------------------------
    # Step 5 — Event Detail Table
    # ------------------------------------------------------------------
    st.subheader("All Events")
    detail_df = athlete_df[
        ["Year", "Games", "Season", "City", "Sport", "Event", "Medal"]
    ].sort_values("Year")
    detail_df["Medal"] = detail_df["Medal"].fillna("—")
    st.dataframe(detail_df, use_container_width=True, hide_index=True)
