import math
import json

MAX_TICKETS_PER_CHALLENGE = 25

DEBUG = True

FIRST = "🥇"
SECOND = "🥈"
THIRD = "🥉"

CHALLENGE_IDS = {
    "day_1": "0de9e913-ef14-44c5-ae5a-51b89c12e7df",
    "day_2": "e1236e67-975e-4f47-bc67-26fd61e8dc0c",
    "day_3": "e8f81c6a-3251-4abb-9bdb-a6e5a8d0b23b",
    "day_4": "19fb1e52-a764-4743-a1ed-b35570b6d1aa",
}

CHALLENGE_POINTS = {
    "0de9e913-ef14-44c5-ae5a-51b89c12e7df": 1000,
    "e1236e67-975e-4f47-bc67-26fd61e8dc0c": 1000,
    "e8f81c6a-3251-4abb-9bdb-a6e5a8d0b23b": 1000,
    "19fb1e52-a764-4743-a1ed-b35570b6d1aa": 1000,
}


SCOREBOARD_USER_TEMPLATE = """
<tr>
    <td>{position}</td>
    <td>{nicknames}</td>
    <td>{day_1}</td>
    <td>{day_2}</td>
    <td>{day_3}</td>
    <td>{day_4}</td>
    <td>{score}</td>
    <td>{tickets}</td>
</tr>
"""

SCOREBOARD_HEADER_TEMPLATE = """
<tr>
    <th>#</th>
    <th>Kallenavn</th>
    <th>Skjærtorsdag<br/>({day_1_solves} solves)</th>
    <th>Langfredag<br/>({day_2_solves} solves)</th>
    <th>Påskeaften<br/>({day_3_solves} solves)</th>
    <th>1. Påskedag<br/>({day_4_solves} solves)</th>
    <th>Poeng</th>
    <th>Antall<br/>Lodd</th>
</tr>
"""

# CHALLENGE_SCORE_INITIAL = 1000
# CHALLENGE_SCORE_DECAY = 20
# CHALLENGE_SCORE_MINIMUM = 50
CHALLENGE_SCORE_DECAY = 24
CHALLENGE_SCORE_MINIMUM = 100

#https://github.com/CTFd/DynamicValueChallenge
#https://github.com/CTFd/CTFd/blob/4c31dc23e8cfa0308367732d603b16e01871b00e/CTFd/plugins/dynamic_challenges/__init__.py#L53
def calculate_challenge_score(challenge, user):
    if challenge["id"] not in user["solutions"]:
        return 0

    challenge_initial = CHALLENGE_POINTS[challenge["id"]]

    solve_count = user["solutions"][challenge["id"]]["position"]

    # If the solve count is 0 we shouldn't manipulate the solve count to
    # let the math update back to normal
    if solve_count != 0:
        # We subtract -1 to allow the first solver to get max point value
        solve_count -= 1

    # It is important that this calculation takes into account floats.
    value = (
        ((CHALLENGE_SCORE_MINIMUM - challenge_initial) / (CHALLENGE_SCORE_DECAY ** 2))
        * (solve_count ** 2)
    ) + challenge_initial

    value = math.ceil(value)

    if value < CHALLENGE_SCORE_MINIMUM:
        value = CHALLENGE_SCORE_MINIMUM

    return value

def format_position(position):
    if position == 0:
        return FIRST
    elif position == 1:
        return SECOND
    elif position == 2:
        return THIRD
    else:
        return position + 1

def format_solution(user, challenge_id):
    if challenge_id not in user["solutions"]:
        return ""
    challenge = challenges[challenge_id]
    solution = user["solutions"][challenge_id]
    timestamp = solution["timestamp"]
    position = format_position(solution["position"])

    if DEBUG:
        score = round(solution['score'], 2)
        position = f"<div class='challenge-container'>{str(position)} <span class='challenge-score'>[{score}]</span></div>"

    return f'<span title="{timestamp}">{position}</span>'

with open("solutions.json") as f:
    challenge_solutions = json.load(f)

challenges = {}
users = {}
total_tickets = 0

for challenge in challenge_solutions:
    if not challenge["solutions"]:
        continue
    challenge_id = challenge["_id"]
    challenges[challenge_id] = {
        "id": challenge_id,
        "title": challenge["title"],
        "solve_count": len(challenge["solutions"]),
    }
    for position, user in enumerate(challenge["solutions"]):
        solve_data = {
            "timestamp": user["timestamp"],
            "position": position,
        }
        if user["id"] in users:
            users[user["id"]]["nicknames"].add(user["nickname"])
            users[user["id"]]["solutions"][challenge_id] = solve_data
        else:
            users[user["id"]] = {
                "nicknames": {user["nickname"]},
                "tickets": 0,
                "solutions": {
                    challenge_id: solve_data,
                },
            }

        if position < MAX_TICKETS_PER_CHALLENGE:
            users[user["id"]]["tickets"] += 1
            total_tickets += 1

# Find duplicate usernames with unique IDs and merge them
handled_users = set()
current_users = {}
for user_id, user in users.items():
    if user_id in handled_users:
        continue
    user["user_ids"] = { user_id }
    for other_user_id, other_user in users.items():
        for nickname in user["nicknames"]:
            if nickname not in other_user["nicknames"]:
                continue
            for challenge_id, solve_data in other_user["solutions"].items():
                if challenge_id in user["solutions"]:
                    continue
                user["solutions"][challenge_id] = solve_data
                if solve_data["position"] < MAX_TICKETS_PER_CHALLENGE:
                    user["tickets"] += 1
            handled_users.add(other_user_id)
            break
    handled_users.add(user_id)
    current_users[user_id] = user


# Calculate final position/score
final_users = {}
for user_id, user in current_users.items():
    total_score = 0
    solutions = user["solutions"]
    tickets = user["tickets"]
    for challenge_id, challenge in challenges.items():
        score = calculate_challenge_score(challenge, user)
        if challenge_id in solutions:
            user["solutions"][challenge_id]["score"] = score
        total_score += score

    user["winning_chance"] = int((tickets / total_tickets) * 100)
    user["id"] = user_id
    user["score"] = total_score
    final_users[user_id] = user
    
final_users = {k: final_users[k] for k in sorted(final_users, key=lambda user_id: final_users[user_id]["score"], reverse=True)}

# Write out the scoreboard
scoreboard_header = SCOREBOARD_HEADER_TEMPLATE.format(
    day_1_solves=challenges[CHALLENGE_IDS["day_1"]]["solve_count"],
    day_2_solves=challenges[CHALLENGE_IDS["day_2"]]["solve_count"],
    day_3_solves=challenges[CHALLENGE_IDS["day_3"]]["solve_count"],
    day_4_solves=challenges[CHALLENGE_IDS["day_4"]]["solve_count"],
)
scoreboard_body = ""
for position, user in enumerate(final_users.values()):
    user_id = user["id"]
    extra_class = "rainbowText svelte-1s8qpfq" if position == 0 else ""
    nicknames = f'<span title="{user_id}" class="{extra_class}">' + "<br>".join(list(user["nicknames"])) + "</span>"

    scoreboard_body += SCOREBOARD_USER_TEMPLATE.format(
        position=format_position(position),
        nicknames=nicknames,
        day_1=format_solution(user, CHALLENGE_IDS["day_1"]),
        day_2=format_solution(user, CHALLENGE_IDS["day_2"]),
        day_3=format_solution(user, CHALLENGE_IDS["day_3"]),
        day_4=format_solution(user, CHALLENGE_IDS["day_4"]),
        score=round(user["score"], 2),
        tickets=user["tickets"],
    )


with open("scoreboard_template.html") as f:
    template = f.read()

with open("index.html", "w") as f:
    f.write(template
        .replace("{{TICKET_COUNT}}", str(total_tickets))
        .replace("{{SCOREBOARD_HEADER}}", scoreboard_header)
        .replace("{{SCOREBOARD_BODY}}", scoreboard_body)
    )
