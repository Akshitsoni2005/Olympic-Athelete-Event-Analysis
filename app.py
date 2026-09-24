"""Olympic Athlete Events Dashboard — entry point.

Run with:
    streamlit run app.py
(from inside the athlete_events_app/ directory)
"""

import sys
from pathlib import Path

import streamlit as st

# Ensure the app directory is on sys.path so page imports work when running
# `streamlit run app.py` from athlete_events_app/.
_APP_DIR = Path(__file__).parent
if str(_APP_DIR) not in sys.path:
    sys.path.insert(0, str(_APP_DIR))

from pages import (  # noqa: E402
    athlete_analysis,
    athlete_explorer,
    country_analysis,
    overview,
    sport_event_analysis,
)

st.set_page_config(
    layout="wide",
    page_title="Olympics Dashboard",
    page_icon="🏅",
)

st.sidebar.title("🏅 Olympics Dashboard")

PAGE_OPTIONS = [
    "Overview",
    "Athlete Analysis",
    "Country Analysis",
    "Sport & Event Analysis",
    "Athlete Explorer",
]

selection = st.sidebar.radio("Navigate to", PAGE_OPTIONS)

if selection == "Overview":
    overview.show()
elif selection == "Athlete Analysis":
    athlete_analysis.show()
elif selection == "Country Analysis":
    country_analysis.show()
elif selection == "Sport & Event Analysis":
    sport_event_analysis.show()
elif selection == "Athlete Explorer":
    athlete_explorer.show()

st.sidebar.markdown("---")
st.sidebar.caption("📊 Data: 120 Years of Olympic History (Kaggle)\n\n🐍 Built with Streamlit + Plotly")
