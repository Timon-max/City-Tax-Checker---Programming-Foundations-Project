# Program Flow

What the receptionist sees and does, from starting the program to closing it.
The program is started from the project folder with `python main.py`.

## Flow sketch

```
Start
  → show_start_screen()            start_screen.py
  → ask_menu_choice()              start_screen.py
  → load the two lists             input_data/      (US-1)
  → check the data                 input_data/      (US-2)
  → choose the night to check      input_data/      (US-3)
  → match guests to rooms          processing/      (US-4)
  → count taxable persons          processing/      (US-5)
  → compare charged and correct    processing/      (US-6)
  → show statistics                output/          (US-7)
  → show the report                output/          (US-8)
  → save the report?               output/          (US-9)
  → back to the menu
End
```

## Step by step

### Step 0: Start screen

The user types `python main.py`. The program shows:

```
==============================
      CITY TAX CHECKER
==============================
Compares BSCT (Meldeschein) and Morphe (charges)
and shows city tax charged for the wrong number of people.

1) Start city tax check
2) Help: which files do I need?
3) Exit

Your choice:
```

* Only `1`, `2` or `3` is accepted. Anything else: `Please enter 1, 2 or 3` and the question is asked again.
* `2` prints which exports are needed and where to put them, then shows the menu again.
* `3` prints `Goodbye` and ends the program.

### Step 1: Load the two lists (US-1, Cristian)

```
Path to the BSCT file: data/input/BSCT.csv
Path to the Morphe file: data/input/Morphe.csv
BSCT loaded: 70 rows
Morphe loaded: 68 rows
```

* The program checks: file exists, ends in `.csv`, can be opened, separator is `;`.
* On an error it names the file and the problem, then asks for the path again.
* The Excel exports are converted to CSV first (roadmap step 1, code already in `main.py` from Noah).

### Step 2: Check the data (US-2, Cristian)

No input from the user. The program checks every row and prints a short summary:

```
BSCT: 68 rows ok, 2 rows flagged
Morphe: 68 rows ok, 0 rows flagged
```

Flagged rows are not lost, they appear later in the report under "Needs manual check".

### Step 3: Choose the night (US-3, Cristian)

```
Night to check (DD.MM.YYYY): 26.09.2026
Checking the night of 26.09.2026
Guests staying this night: 41 (12 checked out today, not counted)
```

* A wrong date (`31.09.2026`, `abc`) gives an error and the question is asked again.
* Guests whose departure is this day are removed (they did not sleep here this night).

### Steps 4 to 6: Processing (US-4 to US-6, Timon)

No input from the user. The program prints one line per step so the user sees it working:

```
Merging invoices per room ... 68 invoices -> 52 rooms
Matching guests to rooms ... 47 matched, 2 ambiguous, 3 not matched
Comparing city tax ... done
```

What happens inside:

1. Morphe: all invoices of the same room are added up into one charge per room (guest invoice + `**` company invoice).
2. Surnames in both lists are cleaned (upper case, spaces trimmed, `**` removed, accents removed).
3. Each BSCT guest is linked to the room with the same surname. Same surname in two rooms → "ambiguous". Surname only in one list → "not matched".
4. BSCT: the city tax of the whole stay is split into the city tax of one night, which gives the number of taxable persons.
5. For every room: charged (Morphe) is compared with correct (BSCT).

### Steps 7 and 8: Show statistics and report (US-7, US-8, Noah)

```
City tax check for the night of 26.09.2026

DIFFERENCES
Room  Surname   Persons charged  Correct  Charged  Correct  Difference
101   BRUNNER   2                3        8.40     12.60    +4.20

NEEDS MANUAL CHECK
214   MUELLER   ambiguous: surname in rooms 214, 305
-     WEBER     registered but no invoice (not matched)

STATISTICS
Rooms checked: 52, correct: 45, with difference: 3, ambiguous: 2
Charged: 210.00  Correct: 222.60  Difference: +12.60
Rooms with a difference: 5.8 %
```

### Step 9: Save the report (US-9, Noah)

```
Do you want to save the report? (yes/no): y
Report saved to reports/city_tax_report_20260926_20261027_143022.csv
```

* Only `yes`, `y`, `no`, `n` are accepted (any case).
* Then the program goes back to the menu (Step 0).

## Open points to decide as a group

* The README input section still describes the old CSV format (`mc_prestations.csv`, `meldeschein.csv`). The real exports are BSCT and Morphe with different column names. README and user stories need an update, and changes to the scope must be told to the lecturers.
* Morphe is a daily report, so one run checks **one night**. US-3 still says "period of up to 31 days".
* BSCT has the amount for the whole stay, so taxable persons come from `amount / nights / 4.20`, not from the date of birth. US-5 says date of birth.
