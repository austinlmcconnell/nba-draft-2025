import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(layout="wide", page_title="2025 NBA Draft Tracker")
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

def get_team_logo(team_abbr):
    if not team_abbr or team_abbr == "":
        return None
    return f"https://a.espncdn.com/i/teamlogos/nba/500/{team_abbr.lower()}.png"

def get_team_color(team):
    team_colors = {
        "Hawks": "#E03A3E",
        "Celtics": "#007A33",
        "Nets": "#000000",
        "Hornets": "#1D1160",
        "Bulls": "#CE1141",
        "Cavaliers": "#6F263D",
        "Mavericks": "#00538C",
        "Nuggets": "#0E2240",
        "Pistons": "#1D42BA",
        "Warriors": "#FDB927",
        "Rockets": "#CE1141",
        "Pacers": "#FDBB30",
        "Clippers": "#C8102E",
        "Lakers": "#FDB927",
        "Grizzlies": "#5D76A9",
        "Heat": "#98002E",
        "Bucks": "#00471B",
        "Timberwolves": "#0C2340",
        "Pelicans": "#0C2340",
        "Knicks": "#F58426",
        "Thunder": "#007AC1",
        "Magic": "#0077C0",
        "76ers": "#006BB6",
        "Suns": "#E56020",
        "Trail Blazers": "#E03A3E",
        "Kings": "#5A2D81",
        "Spurs": "#C4CED4",
        "Raptors": "#CE1141",
        "Jazz": "#002B5C",
        "Wizards": "#002B5C"
    }
    return team_colors.get(team, "white")

# --- LOAD DATA ---
df = load_data()
df = df.fillna("")

# --- DROPDOWN MENU ---
dropdown_names = ["-- All Players --"] + df["Name"].tolist()
selected_player = st.selectbox("Select a player to view", dropdown_names)

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

        try:
            rank = int(float(row['Rank'])) if row['Rank'] != "2nd Round" else "2nd Round"
        except:
            rank = row['Rank']

        st.markdown(f"### {pick}. {row['Name']}")
        st.markdown(f"**Rank:** {rank}")
        st.markdown(f"**Position:** {row['Position']}")
        st.markdown(f"**School:** {row['School/Country']}")
        st.markdown(f"**Height:** {row['Height']} | **Weight:** {row['Weight']} | **Wingspan:** {row['Wingspan']}")
        st.markdown(f"**Biggest Skill:** {row['Biggest Skill']}")
        st.markdown(f"**Biggest Weakness:** {row['Biggest Weakness']}")

        # Mocked Team
        if row['My Mock Team']:
            mock_team_logo = get_team_logo(row['My Mock Team'])
            team_color = get_team_color(row['My Mock Team'])
            st.markdown(f"**Mock Draft Team:** <span style='color:{team_color}'>{row['My Mock Team']}</span>", unsafe_allow_html=True)
            if mock_team_logo:
                st.image(mock_team_logo, width=60)

        # Drafted Team Logo and Grade
        if row['Drafted Team']:
            drafted_team_logo = get_team_logo(row['Drafted Team'])
            st.markdown(f"**Drafted Team:** {row['Drafted Team']}")
            if drafted_team_logo:
                st.image(drafted_team_logo, width=60)

        st.markdown(f"**Grade:** {row['My Grade']}")

# --- DISPLAY LOGIC ---
if selected_player != "-- All Players --":
    player_row = df[df["Name"] == selected_player].iloc[0]
    display_player(player_row)
else:
    for _, row in df.iterrows():
        display_player(row)
        st.markdown("---")

