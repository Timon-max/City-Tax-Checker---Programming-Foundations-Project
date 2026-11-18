# US-3: Select the night to check

from datetime import datetime


def ask_check_night():
    while True:
        text = input("Night to check (DD.MM.YYYY): ").strip()
        try:
            return datetime.strptime(text, "%d.%m.%Y").date()
        except ValueError:
            print(f"{text} is not a valid date")


def keep_guests_staying(guests, night):
    # A guest stays on night D if arrival <= D < departure
    staying = []
    for guest in guests:
        arrival = datetime.strptime(guest["Anreise"], "%d.%m.%Y").date()
        departure = datetime.strptime(guest["Abreise"], "%d.%m.%Y").date()
        if arrival <= night < departure:
            staying.append(guest)
    return staying


if __name__ == "__main__":
    guests = [
        {"Name": "BRUNNER", "Anreise": "26.09.2026", "Abreise": "28.09.2026"},
        {"Name": "ZANETTI", "Anreise": "24.09.2026", "Abreise": "26.09.2026"},
    ]
    night = ask_check_night()
    staying = keep_guests_staying(guests, night)
    for guest in staying:
        print(guest["Name"])
