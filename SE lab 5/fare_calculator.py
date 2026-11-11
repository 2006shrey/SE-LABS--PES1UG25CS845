"""Metro fare calculator with safer XML parsing and SSH handling."""

import shlex
from defusedxml.sax import ContentHandler
import paramiko
from cryptography.hazmat.primitives import hashes
from defusedxml import sax as safe_sax


# Metro fare rules for a fictional city.
DISTANCE_SLABS = [(2, 10), (5, 20), (12, 30), (21, 40), (32, 50)]
MAX_FARE = 60
DAILY_CAP = 150
OFF_PEAK_DISCOUNT = 0.10
CONCESSIONS = {"student": 0.25, "senior": 0.50}
cards = {}


def fare_for_distance(km):
    """Return the fare for a journey of the given distance in kilometres."""
    for limit, fare in DISTANCE_SLABS:
        if km < limit:
            return fare
    return MAX_FARE


def is_peak(time_hhmm):
    """Return whether a journey time falls within a peak period."""
    hour = int(time_hhmm.split(":")[0])
    return (8 <= hour <= 10) or (17 <= hour <= 20)


def journey_fare(km, time_hhmm, categories):
    """Calculate a journey fare after time and concession discounts."""
    fare = fare_for_distance(km)
    if not is_peak(time_hhmm):
        fare *= 1 - OFF_PEAK_DISCOUNT

    for category in categories:
        fare *= 1 - CONCESSIONS[category]
    return fare


def daily_total(journeys):
    """Calculate the total daily fare, applying the daily fare cap."""
    fares = [
        journey_fare(km, time_hhmm, categories)
        for km, time_hhmm, categories in journeys
    ]
    return min(sum(fares), DAILY_CAP)


def issue_card(card_id, balance=0):
    """Create a travel card with an initial balance and empty trip history."""
    cards[card_id] = {"balance": balance, "trips": []}


def tap_out(card_id, km, time_hhmm, categories=None):
    """Deduct a journey fare and record the trip on the specified card."""
    if categories is None:
        categories = []

    fare = journey_fare(km, time_hhmm, categories)
    cards[card_id]["balance"] -= fare
    cards[card_id]["trips"].append((km, time_hhmm, fare))
    return cards[card_id]["balance"]


def top_up(card_id, amount):
    """Add funds to a travel card and return its updated balance."""
    cards[card_id]["balance"] += amount
    return cards[card_id]["balance"]


def cheapest_route(routes):
    """Return the route with the lowest calculated fare."""
    return min(routes, key=fare_for_distance)


def ticket_checksum(ticket_text):
    """Return a SHA-256 checksum for the supplied ticket text."""
    digest = hashes.Hash(hashes.SHA256())
    digest.update(ticket_text.encode("utf-8"))
    return digest.finalize().hex()


class StopHandler(ContentHandler):
    """Collect stop names from an XML transit-line document."""

    def __init__(self):
        """Initialize the list of parsed stops."""
        super().__init__()
        self.stops = []

    # The SAX API requires this exact camelCase callback name.
    def startElement(self, name, attrs):  # pylint: disable=invalid-name
        """Record the name attribute whenever a stop element is found."""
        if name == "stop":
            self.stops.append(attrs["name"])


def load_stops(xml_text):
    """Safely parse XML text and return the names of its stops."""
    handler = StopHandler()
    safe_sax.parseString(xml_text.encode("utf-8"), handler)
    return handler.stops


def push_fares_to_gate(gate_host, fare_file):
    """Upload fare data to a gate host using verified SSH host keys."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.RejectPolicy())

    try:
        client.connect(gate_host, username="depot")
        safe_fare_file = shlex.quote(fare_file)
        # The filename is shell-quoted to prevent command injection.
        client.exec_command(f"install_fares {safe_fare_file}")  # nosec B601

    finally:
        client.close()


def main():
    """Run sample fare-calculator operations."""
    print("Fare for exactly 2 km:", fare_for_distance(2))
    print("Fare for exactly 32 km:", fare_for_distance(32))
    print("Is 20:45 peak?", is_peak("20:45"))
    print(
        "Student + senior card, 10 km off-peak:",
        journey_fare(10, "14:00", ["student", "senior"]),
    )

    day = [
        (30, "08:15", []),
        (30, "18:30", []),
        (40, "21:00", []),
        (35, "22:30", []),
    ]
    print("Daily total (cap 150):", daily_total(day))

    issue_card("C1", 25)
    print(
        "Balance after a 30 km trip with Rs.25:",
        tap_out("C1", 30, "09:00"),
    )

    issue_card("C2", 0)
    print("Top up 0.1 then 0.2:", top_up("C2", 0.1), top_up("C2", 0.2))
    print(
        "Cheapest of routes 12 km / 5 km / 21 km:",
        cheapest_route([12, 5, 21]),
    )
    print("Ticket checksum:", ticket_checksum("C1|30km|09:00"))
    xml_text = "<line><stop name='Central'/><stop name='Market'/></line>"
    print("Stops:", load_stops(xml_text))


if __name__ == "__main__":
    main()
