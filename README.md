# 🏨 City Tax Checker

> Programming Foundations group project · FHNW BIT PTE26

A console app that helps hotel receptionists compare two lists and find city tax that was charged for the wrong number of people.

## 🧩 Problem statement

Hotel receptionists experience city tax lists that do not match the guests who actually stayed, during the daily city tax check in the hotel's older booking system (PMS), resulting in a slow manual comparison every day and city tax that is charged for the wrong number of people.

### Why this happens

The reception has to compare two lists every day:

| | List 1: MC_Prestations | List 2: Meldeschein |
|---|---|---|
| **What it is** | Daily charges report from the PMS | Guest registration forms |
| **City tax** | Per day | Total for the whole stay |
| **Persons** | As booked, adults and children not told apart | Real guests, with date of birth |
| **Children under 12** | Not recognised, must be checked by hand | Recognised automatically |

* Guests often arrive differently from how they booked (booked 2 adults, arrive alone or with a child).
* Both lists are created from the same reservation in the PMS, so both carry the **reservation number**. Surnames alone are not unique (two different "Müller" can stay on the same night), so the app never matches by name alone.
* One list is per day and the other per stay, so the numbers never look the same.
* Some stays create two invoices, one for the guest and one for the company that pays (for example Booking.com). Both invoices have the same reservation number.

### Example

A family books for 2 adults and 2 children, 2 nights. On arrival one child turns out to be 13, so 3 people must pay city tax.

| | List 1 says | Correct | App reports |
|---|---:|---:|---|
| **Taxable persons** | 2 | 3 | Change 2 to 3 |
| **City tax per night** | 8.40 | 12.60 | Difference 4.20 per night |
| **City tax for the stay** | 16.80 | 25.20 | 8.40 missing in total |

## ⚙️ What the app does

| Step | Description |
|---|---|
| 📥 **Input** | The two exported lists as CSV files (charges and registrations) and the date or period to check. |
| 🔄 **Processing** | Match records by reservation number, count taxable persons per night, compare charged and correct city tax per night. |
| 📤 **Output** | A list of differences and the values to correct, statistics about the check, saved as a file. |

## 📄 Input files

Both lists are exported from the PMS as **CSV** files. PDF, Excel and image files are not supported.

### General format

| Rule | Value |
|---|---|
| File type | `.csv`, UTF-8 encoding |
| Separator | Semicolon `;` (names and company names can contain commas) |
| Header row | Required, first line, column names exactly as below (order does not matter) |
| Date format | `DD.MM.YYYY`, for example `08.10.2026` |
| Amounts | Decimal point, 2 decimals, in CHF, for example `8.40` |
| Person counts | Whole numbers ≥ 0 |
| Shared key | `reservation_id`, present in both files |

### List 1: `mc_prestations.csv` (one row per charge)

| Column | Type | Description |
|---|---|---|
| `reservation_id` | text | Reservation number from the PMS, for example `R-10421` |
| `room` | text | Room number |
| `surname` | text | Surname of the booking guest (may start with `** `) |
| `first_name` | text | First name, may be empty |
| `date` | date | Date of the night that was charged |
| `charge_type` | text | Type of charge, only `CITY_TAX` rows are used |
| `persons` | whole number | Number of persons charged |
| `amount` | amount | Amount charged in CHF |

```csv
reservation_id;room;surname;first_name;date;charge_type;persons;amount
R-10421;101;** MÜLLER;Hans;08.10.2026;CITY_TAX;2;8.40
R-10421;101;** MÜLLER;Hans;08.10.2026;BREAKFAST;2;50.00
R-10421;101;** MÜLLER;Hans;09.10.2026;CITY_TAX;2;8.40
R-10433;214;MÜLLER;Peter;08.10.2026;CITY_TAX;1;4.20
R-10475;220;SCHMID;Laura;08.10.2026;CITY_TAX;1;4.20
R-10475;220;SCHMID;Laura;08.10.2026;CITY_TAX;1;4.20
R-10462;118;ROSSI;Marco;08.10.2026;CITY_TAX;1;4.20
```

### List 2: `meldeschein.csv` (one row per guest)

| Column | Type | Description |
|---|---|---|
| `reservation_id` | text | Reservation number from the PMS, same as in List 1 |
| `room` | text | Room number |
| `surname` | text | Surname of the guest |
| `first_name` | text | First name of the guest |
| `date_of_birth` | date | Date of birth, may be empty (flagged, see User Story 2) |
| `arrival` | date | Arrival date |
| `departure` | date | Departure date |

```csv
reservation_id;room;surname;first_name;date_of_birth;arrival;departure
R-10421;101;Müller;Hans;02.05.1986;08.10.2026;10.10.2026
R-10421;101;Müller;Anna;11.09.1988;08.10.2026;10.10.2026
R-10421;101;Müller;Lena;15.03.2013;08.10.2026;10.10.2026
R-10421;101;Müller;Tim;20.06.2017;08.10.2026;10.10.2026
R-10433;214;Müller;Peter;30.01.1979;07.10.2026;09.10.2026
R-10475;220;Schmid;Laura;14.07.1992;08.10.2026;09.10.2026
R-10475;220;Schmid;Jonas;03.12.1990;08.10.2026;09.10.2026
R-10450;305;Weber;Sara;22.04.1995;08.10.2026;09.10.2026
R-10462;118;Rossi;Marco;;08.10.2026;11.10.2026
```

All names and numbers above are fictional.

### Expected result for 08.10.2026

| Reservation | What the app finds |
|---|---|
| `R-10421` (Müller, room 101) | Difference: charged 2 persons (8.40), correct 3 persons (12.60), difference +4.20 |
| `R-10433` (Müller, room 214) | Correct, not listed. Same surname as `R-10421`, but a different reservation number, so no confusion |
| `R-10475` (Schmid, room 220) | Correct, not listed. Two invoices (1 + 1 person) are added up to 2 persons |
| `R-10450` (Weber, room 305) | Manual check: registered in List 2 but no city tax charged in List 1 |
| `R-10462` (Rossi, room 118) | Manual check: date of birth missing, counted as taxable until checked |

## 📐 Calculation rules

| Rule | Definition |
|---|---|
| **Unit of comparison** | One reservation on one night. The app compares **daily charges**, not whole stays. |
| **Night** | A guest stays on night `D` if `arrival ≤ D < departure`. The departure day is not a night. |
| **Charged** | Sum of `persons` and `amount` of all `CITY_TAX` rows in List 1 with the same `reservation_id` and `date = D`. |
| **Correct** | Number of taxable guests in List 2 with the same `reservation_id` who stay on night `D`, × 4.20 CHF. |
| **Taxable** | Guest is 12 or older on the arrival date. |
| **Rate** | 4.20 CHF per taxable person per night *(assumption, rate to confirm)*. |

## 🎓 Course requirements

| Requirement | How the app meets it |
|---|---|
| **Interactive (console)** | Runs in the terminal, the user enters the files and the check date, and picks options from a menu. |
| **Data validation** | Checks that files exist, columns are complete, dates are real dates in `DD.MM.YYYY`, person counts are whole numbers, amounts are valid numbers, inputs are valid, and who is 12 or older. |
| **File processing** | Reads the two CSV lists and writes a report of differences, corrections and statistics. |

## 🎯 Scope

| ✅ In scope | ❌ Out of scope |
|---|---|
| Compare the two exported CSV lists | No connection to the hotel's PMS |
| Calculate the correct city tax per reservation and night | No automatic correction of the data |
| List every difference and the fix | No graphical interface |
| Statistics per day, week and month for the selected period | No PDF, Excel or image input |
| Match guests by surname, after adding up split invoices of the same room into one charge | No automatic matching of guests with the same surname: they are flagged "ambiguous" for manual checking and the check continues |

### Known limitation: matching by surname

The two lists have no shared unique ID (List 1 has no Meldeschein number, the Meldeschein has no room number), and List 1 only contains the surname. The app therefore matches guests by surname only. If the same surname appears in more than one room, the app cannot tell the guests apart: it flags them as "ambiguous", leaves them for manual checking and continues with all other guests. A shared ID (for example the room or booking number in both exports) would solve this, but is out of scope. The demo data uses unique surnames, plus one deliberate duplicate to test the flag.

## 🔒 Data

This repository contains **no real guest data**. All tests use a small fake dataset.

## 📋 User stories

| Area | Stories | Owner |
|---|---|---|
| [Input](#input-owner-cristian) | 1, 2, 3 | Cristian |
| [Processing](#processing-owner-timon) | 4, 5, 6 | Timon |
| [Output](#output-owner-noah) | 7, 8, 9 | Noah |

---

### Input (owner: Cristian)

#### User Story 1: Load the two lists

As a hotel receptionist, I want the application to load the MC_Prestations and Meldeschein CSV files, so that I can start the daily city tax check without entering the data manually.

**Acceptance criteria**

1. The application asks the user to enter the path of the MC_Prestations file and of the Meldeschein file.
2. The application checks that both files exist, have the `.csv` extension and can be opened.
3. The application reads both files as UTF-8 with `;` as separator and the first line as header (see [Input files](#-input-files)).
4. If a file is missing, has the wrong extension or cannot be opened, the application displays a clear error message naming the file and asks for the path again.
5. If the header does not contain `;`, the application displays `Wrong separator, expected ';'`.
6. The comparison does not start until both files have been loaded successfully.
7. The original input files are not modified.

**Example:** Given the valid files `mc_prestations.csv` and `meldeschein.csv` from the [examples](#-input-files), when the user enters both paths, then both files are loaded and the application continues with the data validation.

**Edge case:** Given the user enters `meldeschein.xlsx`, when the file is checked, then the application displays `Only .csv files are supported` and asks for the path again.

#### User Story 2: Validate input data and handle missing guest information

As a hotel receptionist, I want the application to validate the data in both lists and identify missing guest information, so that incorrect or incomplete data does not lead to an incorrect city tax calculation.

**Acceptance criteria**

1. The application checks that all required columns of both files are present (see [Input files](#-input-files)). If a column is missing, the file is rejected and the missing column is named.
2. Every row must have a `reservation_id`.
3. All dates must be valid dates in `DD.MM.YYYY` format.
4. In List 2, the departure date must be after the arrival date.
5. `persons` must be a whole number ≥ 0, `amount` must be a number ≥ 0 with at most 2 decimals.
6. If the date of birth is missing or invalid, the guest is flagged for manual checking and still processed (counted as taxable, see User Story 5).
7. Any other invalid row (missing reservation number, invalid date, invalid number) is flagged as invalid and is not used to calculate the city tax.
8. Every flag names the file, the line number, the reservation number (if present) and the reason.
9. Invalid rows do not stop the check, the other rows are processed. All flags appear in the report as "unclear data" (User Stories 7 and 8).
10. The application does not silently make assumptions about missing information.

**Example:** Given the List 2 row `R-10421;101;Müller;Hans;02.05.1986;08.10.2026;10.10.2026`, when the input is validated, then the guest can be processed.

**Edge case:** Given the List 2 row `R-10462;118;Rossi;Marco;;08.10.2026;11.10.2026`, when the input is validated, then the application flags `meldeschein.csv line 10, R-10462: date of birth missing` for manual checking instead of treating the row as invalid.

#### User Story 3: Select the check date or period

As a hotel receptionist, I want to select the date or the period to be checked, so that the application only processes the records that belong to that check.

**Acceptance criteria**

1. The application asks for a start date and an optional end date in `DD.MM.YYYY` format. If the end date is left empty, only the start date is checked.
2. The application validates that both dates are real dates and that the end date is not before the start date.
3. The period is at most 31 days.
4. From List 1, only rows with `charge_type = CITY_TAX` and a `date` inside the period are selected.
5. From List 2, only guests who stay at least one night inside the period are selected (`arrival ≤ D < departure`).
6. The selected period and the number of selected rows from each list are shown to the user before processing starts.
7. If no rows are selected from one of the lists, the application shows a warning and asks whether to continue or enter another date.
8. If an invalid date is entered, the application displays a clear error message and asks again. It never assumes a date.

**Example:** Given the [example files](#-input-files) and the check date `08.10.2026` with an empty end date, when the records are selected, then 5 `CITY_TAX` rows from List 1 (the breakfast row and the 09.10.2026 row are ignored) and 9 guests from List 2 are selected.

**Edge case:** Given the user enters `31.09.2026`, when the date is validated, then the application displays `31.09.2026 is not a valid date` and asks again.

---

### Processing (owner: Timon)

#### User Story 4: Match guests across both lists

As a hotel receptionist, I want the app to link each city tax charge in List 1 to the matching guest in the Meldeschein, so that I spend less time on the daily check and guests the app cannot tell apart are shown to me instead of being guessed.

**Acceptance criteria**

1. Before matching, List 1 rows with the same room number and surname (for example a guest invoice and a company invoice) are added up into one charge per room.
2. Surnames in both lists are normalised before matching: upper case, spaces trimmed, a leading `** ` removed, accents removed (`Müller` = `MUELLER` = `MULLER`).
3. Guests are matched by surname only, because the two lists have no shared unique ID (see Known limitation).
4. If the same surname appears in more than one room, all affected entries are flagged "ambiguous", left out of the calculation and listed for manual checking.
5. The check does not stop at an ambiguous entry: all other guests are still matched and calculated.
6. A guest found in only one list is reported as "not matched" (charged but not registered, or registered but not charged), not skipped.

**Example:** Given room 101 with two List 1 rows `** MÜLLER` (city tax 8.40, 0 persons) and `MÜLLER` (2 persons, no city tax), and one Meldeschein entry `Müller` with 2 persons, when the lists are matched, then both List 1 rows are added up into one charge for room 101 (8.40, 2 persons) and linked to the Meldeschein entry.

**Edge case:** Given `KELLER` in rooms 204 and 305 of List 1 and two Meldeschein entries `Keller`, when the lists are matched, then the app flags both as `ambiguous: KELLER (rooms 204, 305), check manually` and continues with all other guests.

#### User Story 5: Count taxable guests

As a hotel receptionist, I want the app to work out how many guests are taxable, using date of birth and the 12-or-older rule, so that I no longer have to check children's ages by hand.

**Acceptance criteria**

1. A guest's age is calculated on the arrival date.
2. A guest aged 12 or older is taxable, under 12 is exempt.
3. The app counts the taxable guests per reservation and per night (only guests who stay that night).
4. A missing or invalid date of birth is flagged, and the guest is counted as taxable until checked.

**Example:** Given reservation `R-10421` with 4 guests aged 40, 38, 13 and 9 on the arrival date 08.10.2026, when taxable guests are counted for the night of 08.10.2026, then the result is 3.

**Edge case:** Given a guest who turns 12 during the stay, then the guest is still exempt for the whole stay, because age is taken on the arrival date.

#### User Story 6: Compare charged and correct city tax per night

As a hotel receptionist, I want the app to compare, for every reservation and every night of the selected period, what List 1 charged with the correct amount, so that guests are charged city tax for the right number of people.

**Acceptance criteria**

1. The comparison is done per reservation and per night (daily charges), following the [calculation rules](#-calculation-rules). Whole stays are not compared.
2. Charged = sum of `persons` and `amount` of the List 1 `CITY_TAX` rows of that reservation and night.
3. Correct = taxable guests of that reservation staying that night × 4.20 CHF *(assumption, rate to confirm)*.
4. Difference = correct amount − charged amount. A positive difference means too little was charged, a negative one means too much.
5. When the lists disagree, the Meldeschein counts as correct, and the row is marked so the user sees it in the report.
6. If the charged amount does not equal charged persons × 4.20, the row is flagged "amount does not match persons".
7. For every reservation and night with a difference, the app produces: date, reservation, room, guest name, persons charged, correct persons, amount charged, correct amount, difference. Reservations and nights without a difference are not listed as differences.
8. Amounts are rounded to 2 decimals.

**Example:** Given `R-10421` charged for 2 persons (8.40) on 08.10.2026 and 3 taxable guests staying that night, when the amounts are compared, then the app produces `08.10.2026, R-10421, 101, MÜLLER Hans, 2 → 3, charged 8.40, correct 12.60, difference +4.20`.

**Edge case:** Given `R-10475` charged by two invoices of 1 person each (4.20 + 4.20) on 08.10.2026 and 2 adult guests, then the charges are added up to 2 persons and 8.40, and the reservation does not appear in the list of differences.

---

### Output (owner: Noah)

#### User Story 7: Show statistics about the check

As a hotel receptionist, I want to see statistics about the checked period, such as how much city tax was charged and should have been charged per day, week and month and how much data was unclear, so that I can see how big the problem is and report it to my manager.

**Acceptance criteria**

1. After processing, the app shows a statistics section with:
   * number of reservations checked, correct, with a difference, and not matched,
   * number of unclear records, grouped by reason (missing date of birth, invalid row, name mismatch, amount does not match persons),
   * total city tax charged, total correct city tax and total difference for the period.
2. The app shows the charged, correct and difference totals **per day** for every day of the selected period.
3. If the period covers more than one day, the app also shows the totals **per week** (Monday to Sunday) and **per calendar month**. Weeks or months that are only partly inside the period are marked `(partial)`.
4. The app shows the share of reservations with a difference as a percentage with 1 decimal.
5. All amounts are shown in CHF with exactly 2 decimals.
6. Amount totals only include matched reservations. Not matched reservations are counted, but their amounts are not added, because they need a manual check first.
7. The numbers in the statistics are consistent with the list of differences (the total difference equals the sum of all listed differences).

**Example:** Given the [example files](#-input-files) and the check date 08.10.2026, when the statistics are shown, then the user sees `Reservations checked: 5, correct: 3, with difference: 1, not matched: 1`, `Unclear data: 1 (missing date of birth: 1)`, `Charged: 25.20, Correct: 29.40, Difference: +4.20` and `Reservations with a difference: 20.0 %`.

**Edge case:** Given the period 28.09.2026 to 04.10.2026, then the weekly totals show one full week (28.09–04.10) and the monthly totals show `September 2026 (partial)` and `October 2026 (partial)`.

#### User Story 8: Display the report of differences to the user

As a hotel receptionist, I want to see a clear, organized report of all differences between the two lists, so that I can quickly understand what needs to be corrected.

**Acceptance criteria**

1. The report shows the checked period at the top.
2. The differences are displayed in a table with the columns: Date, Reservation, Room, Guest Name, Persons Charged, Correct Persons, Amount Charged, Correct Amount, Difference.
3. Rows are sorted by date, then by room number.
4. All monetary amounts show exactly 2 decimal places in CHF, differences with a sign (`+4.20`, `-4.20`).
5. Only reservations and nights with a difference are shown in the table.
6. A second section "Needs manual check" lists every not matched reservation and every unclear record, with the reason (from User Stories 2, 4 and 6).
7. The statistics from User Story 7 are shown below.

**Example:** Given processing found 1 difference and 2 records needing a manual check, when the report is displayed, then the user sees a table with 1 row, a "Needs manual check" section with 2 rows, and the statistics.

**Edge case:** Given no differences and no unclear records are found, then the app displays `No differences found` and `Nothing to check manually` instead of empty tables.

#### User Story 9: Save the report to a file

As a hotel receptionist, I want to save the report as a file, so that I can archive it for documentation and review it later if needed.

**Acceptance criteria**

1. After viewing the report, the user is asked `Do you want to save the report? (yes/no)`. Only `yes`/`y` or `no`/`n` (any upper/lower case) are accepted, any other answer repeats the question.
2. If yes, the app saves the report as a `.txt` file in the `reports` folder. The folder is created if it does not exist.
3. The file name is `city_tax_report_<check date>_<YYYYMMDD_HHMMSS>.txt` (for a period: `city_tax_report_<start>_<end>_<YYYYMMDD_HHMMSS>.txt`), with dates written as `YYYYMMDD`.
4. An existing file is **never overwritten**. If the file name already exists, the app adds `_2`, `_3`, … before `.txt` until it finds a free name. The file is opened in "create only" mode, so even a file created at the same moment cannot be overwritten.
5. The file contains exactly the same content as the report on screen (differences, needs manual check, statistics).
6. After saving, a confirmation message shows the full path of the saved file.
7. If saving fails (folder cannot be created, no write permission, disk full, invalid path), the app displays `Report could not be saved: <reason>`, deletes any partly written file, and asks whether to try again or return to the menu without saving.
8. A failed save never stops the program or loses the report on screen.

**Example:** Given the report for 08.10.2026 has been displayed at 14:30:22 on 08.10.2026, when the user answers `yes`, then the file `reports/city_tax_report_20261008_20261008_143022.txt` is created and the user sees `Report saved to reports/city_tax_report_20261008_20261008_143022.txt`.

**Edge case 1:** Given `reports/city_tax_report_20261008_20261008_143022.txt` already exists, when the user saves within the same second, then the app saves `reports/city_tax_report_20261008_20261008_143022_2.txt` and the existing file is unchanged.

**Edge case 2:** Given the `reports` folder is read-only, when the user saves, then the app displays `Report could not be saved: permission denied` and offers `1) Try again  2) Back to menu`.
