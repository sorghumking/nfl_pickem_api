import csv

from database import db, Team, Matchup

teams = [
    ("Arizona Cardinals", "ARI"),
    ("Atlanta Falcons", "ATL"),
    ("Baltimore Ravens", "BAL"),
    ("Buffalo Bills", "BUF"),
    ("Carolina Panthers", "CAR"),
    ("Chicago Bears", "CHI"),
    ("Cincinnati Bengals", "CIN"),
    ("Cleveland Browns", "CLE"),
    ("Dallas Cowboys", "DAL"),
    ("Denver Broncos", "DEN"),
    ("Detroit Lions", "DET"),
    ("Green Bay Packers", "GB"),
    ("Houston Texans", "HOU"),
    ("Indianapolis Colts", "IND"),
    ("Jacksonville Jaguars", "JAX"),
    ("Kansas City Chiefs", "KC"),
    ("Las Vegas Raiders", "LV"),
    ("Los Angeles Chargers", "LAC"),
    ("Los Angeles Rams", "LAR"),
    ("Miami Dolphins",   "MIA"),
    ("Minnesota Vikings", "MIN"),
    ("New England Patriots", "NE"),
    ("New Orleans Saints", "NO"),
    ("New York Giants", "NYG"),
    ("New York Jets", "NYJ"),
    ("Philadelphia Eagles", "PHI"),
    ("Pittsburgh Steelers", "PIT"),
    ("San Francisco 49ers", "SF"),
    ("Seattle Seahawks", "SEA"),
    ("Tampa Bay Buccaneers", "TB"),
    ("Tennessee Titans", "TEN"),
    ("Washington Commanders", "WSH"),
]

def db_create_teams(teams):
    assert Team.query.all() == [], "Only add teams if none are present"
    for name, abbv in teams:
        t = Team(name=name, abbv=abbv, image_uri=f"{abbv.lower()}.png")
        db.session.add(t)
    db.session.commit()


def db_create_matchups(matchups):
    assert Matchup.query.all() == [], "Only add matchups if none are present"
    for week in range(1,19):
        week_matchups = matchups[week]
        for away, home in week_matchups:
            a = Team.query.filter_by(name=away).first()
            assert a, f"Couldn't find away team {away}"
            h = Team.query.filter_by(name=home).first()
            assert h, f"Couldn't find home team {home}"
            m = Matchup(away_team=a.id, home_team=h.id, week=week)
            db.session.add(m)
    db.session.commit()


# Return dict keyed on weeks 1-18. Each value is a list of tuples of the
# form (away team, home team).
def parse_schedule():
    with open('nfl2022schedule.csv', encoding='utf-8-sig') as csvfile:
        matchups = { week:[] for week in range(1,19) }
        reader = csv.reader(csvfile)
        for row_number, row in enumerate(reader):
            if row_number == 0:
                continue
            week = int(row[0])
            if row[5] == '@':
                matchups[week].append((row[4], row[6]))
            else:
                matchups[week].append((row[6], row[4]))

    # for week in range(1,19):
        # print(f"Week {week}\n{matchups[week]}\n\n")
    return matchups



if __name__ == "__main__":
    parse_schedule()



