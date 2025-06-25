import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

# --- CONFIG ---
st.set_page_config(layout="wide", page_title="2025 NBA Draft Tracker")
st.title("2025 NBA Draft Tracker")
st.caption("Live updates from Austin McConnell's big board")

# --- FUNCTIONS ---
@st.cache_data(ttl=60)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSnTW2iNs8DQ--KGu7YkDLmaxumSsA-i8h8x3k79ALPN822N0moB2ajzMFXRp2bUuPoD3vrfvPRmKFi/pub?output=csv"
    return pd.read_csv(url)

def get_team_logo(team_abbr):
    if not team_abbr or team_abbr == "":
        return None
    return f"https://a.espncdn.com/i/teamlogos/nba/500/{team_abbr.lower()}.png"

# --- LOAD DATA ---
df = load_data()
df = df.fillna("")

# --- DROPDOWN MENU ---
selected_player = st.selectbox("Select a player to view", ["-- All Players --"] + df["Name"].tolist())

# --- PLAYER DISPLAY FUNCTION ---
def display_player(row):
    col1, col2 = st.columns([1, 4])

    # Headshot
    with col1:
        if row["Headshot"]:
            st.image(row["Headshot"], width=150)

    # Player Info
    with col2:
        try:
            pick = int(float(row["Drafted Pick No."]))
        except (ValueError, TypeError):
            pick = "—"

        st.markdown(f"### {pick}. {row['Name']}")
        st.markdown(f"**Position:** {row['Position']}")
        st.markdown(f"**School:** {row['School/Country']}")
        st.markdown(f"**Height:** {row['Height']} | **Weight:** {row['Weight']} | **Wingspan:** {row['Wingspan']}")
        st.markdown(f"**Biggest Skill:** {row['Biggest Skill']}")
        st.markdown(f"**Biggest Weakness:** {row['Biggest Weakness']}")

        # Team Logo and Grade
        team_abbr = row['Drafted Team']
        team_logo = get_team_logo(team_abbr)
        if team_logo:
            st.image(team_logo, width=80)
        st.markdown(f"**Grade:** {row['My Grade']}")

# --- DISPLAY LOGIC ---
if selected_player != "-- All Players --":
    player_row = df[df["Name"] == selected_player].iloc[0]
    display_player(player_row)
else:
    for _, row in df.iterrows():
        display_player(row)
        st.markdown("---")
