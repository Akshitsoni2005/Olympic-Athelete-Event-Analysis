"""Re-usable aggregation helpers for the Olympics Dashboard.

All functions accept a (possibly filtered) DataFrame and return a new DataFrame.
"""

import pandas as pd


def medal_tally(df: pd.DataFrame) -> pd.DataFrame:
    """Return a medal tally grouped by region.

    Columns: region, Gold, Silver, Bronze, Total
    Sorted by Total descending.
    """
    medals = df[df["has_medal"]].copy()
    tally = (
        medals.groupby(["region", "Medal"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    # Ensure all medal columns exist even if absent in the filtered slice
    for col in ("Gold", "Silver", "Bronze"):
        if col not in tally.columns:
            tally[col] = 0

    tally = tally.rename_axis(None, axis=1)
    tally["Total"] = tally["Gold"] + tally["Silver"] + tally["Bronze"]
    return (
        tally[["region", "Gold", "Silver", "Bronze", "Total"]]
        .sort_values("Total", ascending=False)
        .reset_index(drop=True)
    )


def sport_participation_by_year(df: pd.DataFrame) -> pd.DataFrame:
    """Return unique athlete count per Sport per Year.

    Columns: Year, Sport, athlete_count
    """
    result = (
        df.groupby(["Year", "Sport"])["ID"]
        .nunique()
        .reset_index()
        .rename(columns={"ID": "athlete_count"})
    )
    return result.sort_values(["Year", "Sport"]).reset_index(drop=True)


def top_athletes_by_medals(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Return the top-N athletes ranked by total medals won.

    Columns: Name, Team, Sport, Gold, Silver, Bronze, Total
    """
    medals = df[df["has_medal"]].copy()
    tally = (
        medals.groupby(["Name", "Team", "Sport", "Medal"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    for col in ("Gold", "Silver", "Bronze"):
        if col not in tally.columns:
            tally[col] = 0

    tally = tally.rename_axis(None, axis=1)
    tally["Total"] = tally["Gold"] + tally["Silver"] + tally["Bronze"]

    # If an athlete competed in multiple sports, pick the sport with most medals
    top = (
        tally.sort_values("Total", ascending=False)
        .drop_duplicates(subset="Name")
        .head(n)
        .reset_index(drop=True)
    )
    return top[["Name", "Team", "Sport", "Gold", "Silver", "Bronze", "Total"]]
