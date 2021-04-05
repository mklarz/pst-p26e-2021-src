import json

MAX_TICKETS_PER_CHALLENGE = 25

FIRST = "🥇"
SECOND = "🥈"
THIRD = "🥉"

CHALLENGE_IDS = {
    "day_1": "0de9e913-ef14-44c5-ae5a-51b89c12e7df",
    "day_2": "e1236e67-975e-4f47-bc67-26fd61e8dc0c",
    "day_3": "e8f81c6a-3251-4abb-9bdb-a6e5a8d0b23b",
    "day_4": "19fb1e52-a764-4743-a1ed-b35570b6d1aa",
}


SCOREBOARD_USER_TEMPLATE = """
<tr>
  <td>{position}</td>
  <td>{nicknames}</td>
  <td>{day_1}</td>
  <td>{day_2}</td>
  <td>{day_3}</td>
  <td>{day_4}</td>
  <td>{winning_change}</td>
</tr>
"""

def format_position(position):
    if position == 0:
        return FIRST
    elif position == 1:
        return SECOND
    elif position == 2:
        return THIRD
    else:
        return position

def format_solution(user, challenge_id):
    if challenge_id not in user["solutions"]:
        return ""
    solution = user["solutions"][challenge_id]
    timestamp = solution["timestamp"]
    position = format_position(solution["position"])

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
        "title": challenge["title"],
        "total_solves": len(challenge["solutions"]),
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

print(total_tickets)

# Calculate final position/score
final_users = {}
for user_id, user in users.items():
    score = 0
    solutions = user["solutions"]
    tickets = user["tickets"]
    for challenge_id, challenge in challenges.items():
        total_solves = challenge["total_solves"]
        if challenge_id not in solutions:
            score -= total_solves
            continue
        position = solutions[challenge_id]["position"]
        score += total_solves / (position + 1)

    user["winner_change"] = int((tickets / total_tickets) * 100)
    user["id"] = user_id
    final_users[score] = user
    
final_users = {k: final_users[k] for k in sorted(final_users, reverse=True)}

scoreboard_body = ""
for position, user in enumerate(final_users.values()):
    user_id = user["id"]
    extra_class = "rainbowText svelte-1s8qpfq" if position == 0 else ""
    nicknames = f'<span title="{user_id}" class="{extra_class}">' + "<br>".join(list(user["nicknames"])) + "</span>"

    scoreboard_body += SCOREBOARD_USER_TEMPLATE.format(
        position=position + 1,
        nicknames=nicknames,
        day_1=format_solution(user, CHALLENGE_IDS["day_1"]),
        day_2=format_solution(user, CHALLENGE_IDS["day_2"]),
        day_3=format_solution(user, CHALLENGE_IDS["day_3"]),
        day_4=format_solution(user, CHALLENGE_IDS["day_4"]),
        winning_change=f"{user['winner_change']}%",
    )


with open("scoreboard_template.html") as f:
    template = f.read()

with open("index.html", "w") as f:
    f.write(template.replace("{{TICKET_COUNT}}", str(total_tickets)).replace("{{SCOREBOARD_BODY}}", scoreboard_body))
