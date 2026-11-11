
def format_player_name(name):
    """Safely format a player name for the scoreboard."""
    if not isinstance(name, str):
        return ""
    return name.strip().title()[:10]


def parse_frame(text):
    """Safely parse bowling frame notation."""
    if not isinstance(text, str):
        return 0, 0

    text = text.strip().upper()

    if text == "X":
        return 10, 0

    if len(text) != 2:
        return 0, 0

    if not text[0].isdigit() or text[0] not in "0123456789":
        return 0, 0

    first = int(text[0])

    if text[1] == "/":
        return first, 10 - first

    if text[1].isdigit() and text[1] in "0123456789":
        second = int(text[1])
        if first + second <= 10:
            return first, second

    return 0, 0


def parse_scoreboard(text):
    """Safely parse a bowling scoreboard."""
    scores = {}

    if not isinstance(text, str):
        return scores

    for entry in text.split(","):
        if ":" not in entry:
            continue

        name, score = entry.split(":", 1)
        name = name.strip()
        score = score.strip()

        if not name or not score:
            continue

        try:
            value = int(score)
        except ValueError:
            continue

        if value < 0:
            continue

        scores[name] = value

    return scores


def main():
    print("==== Running format_player_name ====")
    value = input("Enter a player name for the scoreboard: ")
    print("Scoreboard name:", format_player_name(value))

    print("\n==== Running parse_frame ====")
    value = input(
        "Enter a frame as X (strike), 7/ (spare) or two digits (e.g. 45): "
    )
    print("Pins (first roll, second roll):", parse_frame(value))

    print("\n==== Running parse_scoreboard ====")
    value = input(
        "Enter scores as NAME:SCORE separated by commas "
        "(e.g. Asha:150,Ravi:132): "
    )
    print("Scoreboard:", parse_scoreboard(value))


if __name__ == "__main__":
    main()
