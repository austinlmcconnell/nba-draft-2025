import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(layout="wide", page_title="2025 NBA Draft Tracker")
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            background-color: white !important;
            color: black !important;
        }
        .fact-label {
            font-weight: bold;
            font-size: 1.05rem;
            margin-bottom: 0.25rem;
        }
        .fact-value {
            font-size: 1.1rem;
            margin-bottom: 0.75rem;
        }
    </style>
""", unsafe_allow_html=True)

st.title("2025 NBA Draft Tracker")
st.caption("Live updates from Austin McConnell's big board")

# --- FUNCTIONS ---
@st.cache_data(ttl=60)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSnTW2iNs8DQ--KGu7YkDLmaxumSsA-i8h8x3k79ALPN822N0moB2ajzMFXRp2bUuPoD3vrfvPRmKFi/pub?output=csv"
    df = pd.read_csv(url)

    # Mark all players below "Second Round prospects" as 2nd Round
    if "Second Round prospects" in df["Rank"].values:
        sr_index = df[df["Rank"] == "Second Round prospects"].index[0]
        df.loc[sr_index+1:, "Rank"] = "2nd Round"
        df = df[df["Rank"] != "Second Round prospects"]

    return df

def get_team_color(team):
    team_colors = {
        "Hawks": "#E03A3E", "Celtics": "#007A33", "Nets": "#000000", "Hornets": "#1D1160", "Bulls": "#CE1141",
        "Cavaliers": "#6F263D", "Mavericks": "#00538C", "Nuggets": "#0E2240", "Pistons": "#1D42BA", "Warriors": "#FDB927",
        "Rockets": "#CE1141", "Pacers": "#FDBB30", "Clippers": "#C8102E", "Lakers": "#FDB927", "Grizzlies": "#5D76A9",
        "Heat": "#98002E", "Bucks": "#00471B", "Timberwolves": "#0C2340", "Pelicans": "#0C2340", "Knicks": "#F58426",
        "Thunder": "#007AC1", "Magic": "#0077C0", "76ers": "#006BB6", "Suns": "#E56020", "Trail Blazers": "#E03A3E",
        "Kings": "#5A2D81", "Spurs": "#C4CED4", "Raptors": "#CE1141", "Jazz": "#002B5C", "Wizards": "#002B5C"
    }
    return team_colors.get(team, "black")

def get_grade_color(grade):
    color_map = {
        "A+": "green", "A": "green", "A-": "green",
        "B+": "#85C88A", "B": "#C4DFA2", "B-": "#E3DD87",
        "C+": "#F2C14E", "C": "orange", "C-": "#FF9933",
        "D+": "#FF6666", "D": "#CC0000", "D-": "#990000", "F": "red"
    }
    return color_map.get(grade.strip().upper(), "black")

# --- LOAD DATA ---
df = load_data()
df = df.fillna("")

# Create a dictionary for team name to logo URL mapping
team_logo_lookup = {
    row["Team Name"]: row["Team Logo URL"]
    for _, row in df.iterrows()
    if row["Team Name"] and row["Team Logo URL"]
}

# --- DROPDOWN MENU ---
dropdown_names = ["-- All Players --"] + df["Name"].tolist()
selected_player = st.selectbox("Select a player to view", dropdown_names)

# --- PLAYER DISPLAY FUNCTION ---
def display_player(row):
    col1, col2 = st.columns([1, 3])

    # Headshot
    with col1:
        if row["Headshot"]:
            st.image(row["Headshot"], width=160)

    # Player Info
    with col2:
        try:
            pick = int(float(row["Drafted Pick No."]))
        except (ValueError, TypeError):
            pick = "—"

        try:
            rank = int(float(row['Rank'])) if row['Rank'] != "2nd Round" else "2nd Round"
        except:
            rank = row['Rank']

        try:
            mock_pick = int(float(row['My Mock Pick No.']))
        except:
            mock_pick = row['My Mock Pick No.']

        st.markdown(f"### <span style='font-weight:700'>{rank}.</span> {row['Name']}", unsafe_allow_html=True)

        st.markdown(f"<div class='fact-label'>Position:</div><div class='fact-value'>{row['Position']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='fact-label'>School:</div><div class='fact-value'>{row['School/Country']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='fact-label'>Height:</div><div class='fact-value'>{row['Height']} | Weight: {row['Weight']} | Wingspan: {row['Wingspan']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='fact-label'>NBA Comparison:</div><div class='fact-value'>{row['NBA Comparison']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='fact-label'>Biggest Skill:</div><div class='fact-value'>{row['Biggest Skill']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='fact-label'>Biggest Weakness:</div><div class='fact-value'>{row['Biggest Weakness']}</div>", unsafe_allow_html=True)

        if row['My Mock Team']:
            mock_team = row['My Mock Team']
            mock_color = get_team_color(mock_team)
            mock_logo = team_logo_lookup.get(mock_team, "")
            st.markdown(f"<div class='fact-label'>Mock Draft Position:</div><div class='fact-value' style='color:{mock_color}'>{mock_pick}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='fact-label'>Mock Draft Team:</div><div class='fact-value' style='color:{mock_color}'>{mock_team}</div>", unsafe_allow_html=True)
            if not row['Drafted Team'] and mock_logo:
                st.image(mock_logo, width=60)

        if row['Drafted Team']:
            drafted_team = row['Drafted Team']
            drafted_color = get_team_color(drafted_team)
            drafted_logo = team_logo_lookup.get(drafted_team, "")
            st.markdown(f"<div class='fact-label'>Draft Position:</div><div class='fact-value' style='color:{drafted_color}'>{pick}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='fact-label'>Drafted Team:</div><div class='fact-value' style='color:{drafted_color}'>{drafted_team}</div>", unsafe_allow_html=True)
            if drafted_logo:
                st.image(drafted_logo, width=60)

        if row['My Grade']:
            grade = row['My Grade'].strip()
            grade_color = get_grade_color(grade)
            st.markdown(f"<div class='fact-label'>Grade:</div><div class='fact-value' style='color:{grade_color}'>{grade}</div>", unsafe_allow_html=True)

# --- DISPLAY LOGIC ---
if selected_player != "-- All Players --":
    player_row = df[df["Name"] == selected_player].iloc[0]
    display_player(player_row)
else:
    for _, row in df.iterrows():
        display_player(row)
        st.markdown("---")
