# US-4: Match guests across both lists


def normalise_surname(surname):
    replacements = {"Ä": "AE", "Ü": "UE", "Ö": "OE", "É": "E", "È": "E", "À": "A"}
    
    surname = surname.upper()

    for old, new in replacements.items():
        surname = surname.replace(old, new)

    surname = surname.replace("**", "")
    surname = surname.strip()


    return surname



def merge_invoices_per_room(invoices):
    pass


def match_guests(guests, rooms):
    pass


if __name__ == "__main__":
    print(normalise_surname("** Müller"))