
import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="2025 NBA Draft Portal", layout="wide")

# Load Google Sheet CSV export
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTiyb7cV_your_sheet_id_here/pub?output=csv"
df = pd.read_csv(sheet_url)

# Clean and sort
df = df.fillna("")
df["Drafted Pick No."] = pd.to_numeric(df["Drafted Pick No."], errors="coerce")
df = df.sort_values(by=["Drafted Pick No.", "Rank"], na_position="last")

# Header
st.title("2025 NBA Draft Tracker")
st.markdown("Live updates from Austin McConnell's big board")

# Display each player
for _, row in df.iterrows():
    team = row["Drafted Team"]
    pick = int(row["Drafted Pick No."]) if row["Drafted Pick No."] else "—"
    color = "#CCCCCC"  # default gray
    logo_url = ""

    # Example static team color dict (expand as needed)
    team_colors = {
        "ATL": "#E03A3E", "BOS": "#007A33", "CHA": "#1D1160", "CHI": "#CE1141",
        "DAL": "#00538C", "DEN": "#0E2240", "DET": "#C8102E", "GSW": "#1D428A",
        "HOU": "#CE1141", "IND": "#002D62", "LAC": "#C8102E", "LAL": "#552583",
        "MEM": "#5D76A9", "MIA": "#98002E", "MIL": "#00471B", "MIN": "#0C2340",
        "NOP": "#0C2340", "NYK": "#006BB6", "OKC": "#007AC1", "ORL": "#0077C0",
        "PHI": "#006BB6", "PHX": "#1D1160", "POR": "#E03A3E", "SAC": "#5A2D81",
        "SAS": "#C4CED4", "TOR": "#CE1141", "UTA": "#002B5C", "WAS": "#002B5C"
    }
    team_logos = {abbr: f"https://a.espncdn.com/i/teamlogos/nba/500/{abbr.lower()}.png" for abbr in team_colors}

    if team in team_colors:
        color = team_colors[team]
        logo_url = team_logos[team]

    with st.container():
        st.markdown(f"<h3 style='color:{color}'>{pick}. {row['Name']}</h3>", unsafe_allow_html=True)
        cols = st.columns([1, 3])
        with cols[0]:
            if row['Headshot']:
                st.image(row['Headshot'], width=150)
            if logo_url:
                st.image(logo_url, width=75)
        with cols[1]:
            st.markdown(f"**Position**: {row['Position']}")
            st.markdown(f"**School**: {row['School/Country']}")
            st.markdown(f"**Height**: {row['Height']}  |  **Weight**: {row['Weight']}  |  **Wingspan**: {row['Wingspan']}")
            st.markdown(f"**Biggest Skill**: {row['Biggest Skill']}")
            st.markdown(f"**Biggest Weakness**: {row['Biggest Weakness']}")
            st.markdown(f"**Grade**: {row['My Grade']}")
        st.markdown("---")
