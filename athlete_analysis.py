import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import streamlit as st
import plotly.express as px
from data.loader import load_data
from data import aggregations


def show():
    df = load_data()
    st.title("🏅 Athlete Analysis")

    # ── Sidebar filters ───────────────────────────────────────────────────────
    sex = st.sidebar.radio("Gender", ["All", "M", "F"])
    year_range = st.sidebar.slider(
        "Year Range", min_value=1896, max_value=2016, value=(1896, 2016), step=4
    )
    opts = sorted(df["Sport"].unique().tolist())
    selected_sports = st.sidebar.multiselect("Sport", opts, default=[])

    # ── Apply filters ─────────────────────────────────────────────────────────
    if sex != "All":
        df = df[df["Sex"] == sex]
    df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]
    if selected_sports:
        df = df[df["Sport"].isin(selected_sports)]

    if df.empty:
        st.warning("No data matches the selected filters.")
        return

    # ── Section 1: Top Medal Winners ──────────────────────────────────────────
    st.subheader("🥇 Top Medal Winners")
    top_n = st.slider("Top N Athletes", 5, 30, 10)
    top_df = aggregations.top_athletes_by_medals(df, top_n)
    top_df = top_df.sort_values("Total", ascending=True)  # ascending for horizontal bar

    fig_top = px.bar(
        top_df,
        x="Total",
        y="Name",
        color="Gold",
        orientation="h",
        title="Top Medal-Winning Athletes",
        template="plotly_white",
        labels={"Total": "Total Medals", "Gold": "Gold Medals"},
    )
    fig_top.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_top, use_container_width=True)

    # ── Deduplicate for demographic plots ─────────────────────────────────────
    df_dedup = df.drop_duplicates(subset=["ID", "Year"])

    # ── Section 2: Demographics ───────────────────────────────────────────────
    st.subheader("📊 Demographics")
    col_left, col_right = st.columns(2)

    # Age distribution
    with col_left:
        age_df = df_dedup.dropna(subset=["Age"])
        fig_age = px.histogram(
            age_df,
            x="Age",
            color="Sex",
            barmode="overlay",
            nbins=40,
            title="Age Distribution by Gender",
            template="plotly_white",
        )
        st.plotly_chart(fig_age, use_container_width=True)

    # Height vs Weight scatter
    with col_right:
        hw_df = df_dedup.dropna(subset=["Height", "Weight"]).copy()
        if len(hw_df) > 10_000:
            hw_df = hw_df.sample(10_000, random_state=42)
        hw_df["Medal Status"] = hw_df["has_medal"].map({True: "Medal", False: "No Medal"})
        fig_hw = px.scatter(
            hw_df,
            x="Weight",
            y="Height",
            color="Medal Status",
            title="Height vs Weight",
            template="plotly_white",
            opacity=0.5,
            labels={"Weight": "Weight (kg)", "Height": "Height (cm)"},
        )
        st.plotly_chart(fig_hw, use_container_width=True)

    # ── Section 3: Average Age by Sport ───────────────────────────────────────
    st.subheader("📅 Average Age by Sport")
    age_sport_df = df_dedup.dropna(subset=["Age"])

    # Top 15 sports by participation count
    participation = age_sport_df.groupby("Sport")["ID"].count()
    top15_sports = participation.nlargest(15).index

    avg_age = (
        age_sport_df[age_sport_df["Sport"].isin(top15_sports)]
        .groupby("Sport")["Age"]
        .mean()
        .reset_index()
        .rename(columns={"Age": "Mean Age"})
        .sort_values("Mean Age", ascending=True)  # ascending for horizontal bar readability
    )

    fig_age_sport = px.bar(
        avg_age,
        x="Mean Age",
        y="Sport",
        orientation="h",
        title="Average Age by Sport (Top 15 by Participation)",
        template="plotly_white",
        color="Mean Age",
        color_continuous_scale="Blues",
    )
    st.plotly_chart(fig_age_sport, use_container_width=True)
