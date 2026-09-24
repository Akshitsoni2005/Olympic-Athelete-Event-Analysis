"""Data loading and cleaning for the Olympics Dashboard."""

from pathlib import Path

import pandas as pd
import streamlit as st

# Workspace root is two levels above this file:
#   athlete_events_app/data/loader.py  →  parent = data/  →  parent = athlete_events_app/  →  parent = workspace root
_ROOT = Path(__file__).parent.parent.parent


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load, clean and merge athlete_events.csv with noc_regions.csv.

    Returns a DataFrame with:
    - Age, Height, Weight cast to float (NaN where raw value was "NA")
    - region column added from noc_regions merge
    - has_medal boolean column
    """
    athletes = pd.read_csv(
        _ROOT / "athlete_events.csv",
        na_values="NA",
    )

    noc_regions = pd.read_csv(
        _ROOT / "noc_regions.csv",
        engine="python",
        na_values="NA",
    )
    # Keep only the columns we need from noc_regions
    noc_regions = noc_regions[["NOC", "region"]].drop_duplicates(subset="NOC")

    # Cast numeric columns (coerce any remaining non-numeric to NaN)
    for col in ("Age", "Height", "Weight"):
        athletes[col] = pd.to_numeric(athletes[col], errors="coerce")

    # Merge region
    athletes = athletes.merge(noc_regions, on="NOC", how="left")

    # Boolean medal indicator
    athletes["has_medal"] = athletes["Medal"].notna()

    return athletes


def get_filter_options(df: pd.DataFrame) -> dict:
    """Return common filter options derived from *df*.

    Keys:
        sports   — sorted list of unique Sport values
        years    — (min_year, max_year) tuple
        seasons  — ["All", "Summer", "Winter"]
        nocs     — sorted list of unique NOC values
        regions  — sorted list of unique region values (excl. NaN)
    """
    return {
        "sports": sorted(df["Sport"].dropna().unique().tolist()),
        "years": (int(df["Year"].min()), int(df["Year"].max())),
        "seasons": ["All", "Summer", "Winter"],
        "nocs": sorted(df["NOC"].dropna().unique().tolist()),
        "regions": sorted(df["region"].dropna().unique().tolist()),
    }
