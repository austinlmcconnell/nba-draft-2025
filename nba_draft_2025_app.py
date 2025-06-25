import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(layout="wide", page_title="2025 NBA Draft Tracker")
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            background-color: #0e1117 !important;
            color: white !important;
        }
        .fact-label {
            font-weight: bold;
            font-size: 1.05rem;
            margin-bottom: 0.25rem;
            color: white;
        }
        .fact-value {
            font-size: 1.1rem;
            margin-bottom: 0.75rem;
            color: white;
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

    if "Second Round prospects" in df["Rank"].values:
        sr_index = df[df["Rank"] == "Second Round prospects"].index[0]
        df.loc[sr_index+1:, "Rank"] = "2nd Round"
        df = df[df["Rank"] != "Second Round prospects"]

    return df

def calculate_mock_accuracy(df):
    total_score = 0
    max_score = 0
    detailed_rows = []

    for _, row in df.iterrows():
        try:
            name = row["Name"]
            mock_pick = int(float(row["My Mock Pick No."]))
            drafted_pick = int(float(row["Drafted Pick No."]))
            mock_team = row["My Mock Team"].strip()
            drafted_team = row["Drafted Team"].strip()
        except:
            continue

        if drafted_pick > 0:
            max_score += 10
            diff = abs(drafted_pick - mock_pick)
            pick_score = max(0, 5 - diff)
            team_score = 5 if mock_team == drafted_team else 0
            total_score += (pick_score + team_score)

            detailed_rows.append({
                "Player": name,
                "Mocked Pick": mock_pick,
                "Drafted Pick": drafted_pick,
                "Mocked Team": mock_team,
                "Drafted Team": drafted_team,
                "Pick Score": pick_score,
                "Team Score": team_score,
                "Total": pick_score + team_score
            })

    if max_score == 0:
        grade = "N/A"
    else:
        percent = (total_score / max_score) * 100
        if percent >= 90:
            grade = f"A ({percent:.1f}%)"
        elif percent >= 75:
            grade = f"B ({percent:.1f}%)"
        elif percent >= 60:
            grade = f"C ({percent:.1f}%)"
        elif percent >= 45:
            grade = f"D ({percent:.1f}%)"
        else:
            grade = f"F ({percent:.1f}%)"

    return grade, detailed_rows

# --- LOAD DATA ---
df = load_data().fillna("")
accuracy_grade, accuracy_details = calculate_mock_accuracy(df)

team_logo_lookup = {
    row["Team Name"]: row["Team Logo URL"]
    for _, row in df.iterrows()
    if row["Team Name"] and row["Team Logo URL"]
}

team_colors = {
    row["Team Name"]: row["Team Font Color"]
    for _, row in df.iterrows()
    if "Team Font Color" in df.columns and row["Team Name"] and row["Team Font Color"]
}

def get_team_color(team):
    team_colors = {
        "Hawks": "#E03A3E", "Celtics": "#008248", "Nets": "#FFFFFF", "Hornets": "#1D1160", "Bulls": "#CE1141",
        "Cavaliers": "#6F263D", "Mavericks": "#00538C", "Nuggets": "#0E2240", "Pistons": "#006BB6", "Warriors": "#FDB927",
        "Rockets": "#CE1141", "Pacers": "#F6A01A", "Clippers": "#C8102E", "Lakers": "#FDB927", "Grizzlies": "#5D76A9",
        "Heat": "#98002E", "Bucks": "#00471B", "Timberwolves": "#236192", "Pelicans": "#85714D", "Knicks": "#F58426",
        "Thunder": "#007AC1", "Magic": "#0077C0", "76ers": "#006BB6", "Suns": "#E56020", "Trail Blazers": "#E03A3E",
        "Kings": "#5A2D81", "Spurs": "#C4CED4", "Raptors": "#CE1141", "Jazz": "#002B5C", "Wizards": "#002B5C"
    }
    return team_colors.get(team, "white")

def get_grade_color(grade):
    color_map = {
        "A+": "green", "A": "green", "A-": "green",
        "B+": "#85C88A", "B": "#C4DFA2", "B-": "#E3DD87",
        "C+": "#F2C14E", "C": "orange", "C-": "#FF9933",
        "D+": "#FF6666", "D": "#CC0000", "D-": "#990000", "F": "red"
    }
    return color_map.get(grade.strip().upper(), "white")

# --- LAYOUT ---
tabs = st.tabs(["Draft Board", "Mock Accuracy"])

with tabs[0]:
    dropdown_names = ["-- All Players --"] + df["Name"].tolist()
    selected_player = st.selectbox("Select a player to view", dropdown_names)

    def display_player(row):
        col1, col2, col3 = st.columns([1, 2.5, 1.5])
        with col1:
            if row["Headshot"]:
                st.image(row["Headshot"], width=160)

        with col2:
            try: pick = int(float(row["Drafted Pick No."]))
            except: pick = "—"
            try: rank = int(float(row['Rank'])) if row['Rank'] != "2nd Round" else "2nd Round"
            except: rank = row['Rank']
            try: mock_pick = int(float(row['My Mock Pick No.']))
            except: mock_pick = row['My Mock Pick No.']
            try: weight_val = int(float(row['Weight']))
            except: weight_val = row['Weight']

            st.markdown(f"### <span style='font-weight:700'>{rank}.</span> {row['Name']}", unsafe_allow_html=True)
            st.markdown(f"<div class='fact-label'>Age:</div><div class='fact-value'>{row['Draft Age']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='fact-label'>Position:</div><div class='fact-value'>{row['Position']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='fact-label'>School:</div><div class='fact-value'>{row['School/Country']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='fact-label'>Height | Weight | Wingspan:</div><div class='fact-value'>{row['Height']} | {weight_val} | {row['Wingspan']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='fact-label'>NBA Comparison:</div><div class='fact-value'>{row['NBA Comparison']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='fact-label'>Biggest Skill:</div><div class='fact-value'>{row['Biggest Skill']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='fact-label'>Biggest Weakness:</div><div class='fact-value'>{row['Biggest Weakness']}</div>", unsafe_allow_html=True)
            if row['My Grade']:
                grade = row['My Grade'].strip()
                grade_color = get_grade_color(grade)
                st.markdown(f"<div class='fact-label'>Grade:</div><div class='fact-value' style='color:{grade_color}'>{grade}</div>", unsafe_allow_html=True)

        with col3:
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

    if selected_player != "-- All Players --":
        display_player(df[df["Name"] == selected_player].iloc[0])
    else:
        for _, row in df.iterrows():
            display_player(row)
            st.markdown("---")

with tabs[1]:
    st.header("Mock Draft Accuracy")
    st.metric("Current Overall Grade", accuracy_grade)
    st.write("Pick-by-pick scoring below based on how close each player was to your projected pick and team.")
    st.dataframe(pd.DataFrame(accuracy_details))
