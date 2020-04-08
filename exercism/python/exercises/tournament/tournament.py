from operator import itemgetter

def tally(results):
    header = "Team                           | MP |  W |  D |  L |  P"
    score_map = {
        "win": [1, 0, 0],
        "draw": [0, 1, 0],
        "loss": [0, 0, 1]
    }
    points_list = [3, 1, 0]

    def update_data(team, match_result):
        team_data = raw_data.get(team, None)
        if team_data:
            team_data.append(match_result)
        else:
            raw_data[team] = [match_result]

    def process_input(result):
        team1, team2, match_result = result.split(";")
        update_data(team1, score_map[match_result])
        update_data(team2, list(reversed(score_map[match_result])))

    raw_data = {}
    raw_tables = []
    printed_tables = [header]
    fields_length = [len(field) for field in header.split("|")]

    for result in results:
        process_input(result)

    for team, team_results in raw_data.items():
        _team_table = []
        _team_table.append(team.strip())
        scores = [sum(team_result) for team_result in zip(*team_results)]
        total_score = sum([x * y for x, y in zip(scores, points_list)])
        _team_table.append(len(team_results))
        _team_table += scores
        _team_table.append(total_score)
        raw_tables.append(_team_table)
    raw_tables = sorted(raw_tables, key=itemgetter(0))
    raw_tables = sorted(raw_tables, key=itemgetter(5), reverse=True)

    for raw_table in raw_tables:
        _table = []
        for i, field in enumerate(raw_table):
            if i == 0:
                _table.append(str(field).ljust(fields_length[i], " "))
            elif i == len(raw_table) - 1:
                _table.append(str(field).rjust(fields_length[i], " "))
            else:
                _table.append(str(field).rjust(fields_length[i] -1, " ") + " ")
        printed_tables.append(("|").join(_table))
    return printed_tables
