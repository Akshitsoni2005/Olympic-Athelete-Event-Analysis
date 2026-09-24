# 🏅 Olympic Athlete Events Dashboard

An interactive data analytics dashboard built with Python (Streamlit + Plotly + Pandas) exploring 120 years of Olympic history from 1896 to 2016.

## 📊 Dataset
- `athlete_events.csv` — 271,116 rows covering every Olympic athlete entry (1896–2016)
- `noc_regions.csv` — NOC to country/region mapping
- Source: [Kaggle — 120 years of Olympic history: athletes and results](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results)

## 🗂️ Pages
| Page | Description |
|---|---|
| 🏠 Overview | KPI metrics + athlete participation trend over time |
| 🏅 Athlete Analysis | Top medal winners, age/height/weight distributions, average age by sport |
| 🌍 Country Analysis | Medal tally, top-20 nations bar chart, choropleth world map, top-5 nations over time |
| 🏋️ Sport & Event Analysis | Events per sport over time, medals by sport, Summer vs Winter comparison, event table |
| 🔍 Athlete Explorer | Search any athlete by name — career timeline and full event history |

## 🚀 Setup & Run

### Prerequisites
- Python 3.9+

### Installation
```bash
cd athlete_events_app
pip install -r requirements.txt
```

### Run the app
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## 🛠️ Tech Stack
| Layer | Library |
|---|---|
| Frontend + Server | Streamlit ≥ 1.32 |
| Data Processing | Pandas ≥ 2.0 |
| Visualisation | Plotly ≥ 5.20 |
| Numerics | NumPy ≥ 1.26 |

## 📁 Project Structure
```
athlete_events_app/
├── app.py                       # Entry point, sidebar navigation
├── data/
│   ├── loader.py                # Cached CSV loading & cleaning
│   └── aggregations.py          # Reusable aggregation helpers
├── pages/
│   ├── overview.py
│   ├── athlete_analysis.py
│   ├── country_analysis.py
│   ├── sport_event_analysis.py
│   └── athlete_explorer.py
└── requirements.txt
```
