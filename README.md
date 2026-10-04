# City-Tax-Checker---Programming-Foundations-Project

Programming Foundations group project, FHNW BIT PTE26. Creating a city tax checker for a hotel having to compare lists

## Problem statement

Hotel receptionists experience city tax lists that do not match the guests who actually stayed, during the daily city tax check in the hotel's older booking system (PMS), resulting in a slow manual comparison every day and city tax that is charged for the wrong number of people.

### Why this happens

The reception has to compare two lists every day:

| | List 1: MC_Prestations | List 2: Meldeschein |
|---|---|---|
| What it is | Daily charges report from the PMS | Guest registration forms |
| City tax | Per day | Total for the whole stay |
| Persons | As booked, adults and children not told apart | Real guests, with date of birth |
| Children under 12 | Not recognised, must be checked by hand | Recognised automatically |

* Guests often arrive differently from how they booked (booked 2 adults, arrive alone or with a child).
* The guest's name is the only thing both lists have in common.
* One list is per day and the other per stay, so the numbers never look the same.
* Some stays create two invoices, one for the guest and one for the company that pays (for example Booking.com).

### Example

A family books for 2 adults and 2 children, 2 nights. On arrival one child turns out to be 13, so 3 people must pay city tax (rate of 4.20 per person per night, still to be confirmed).

| | List 1 says | Correct | App reports |
|---|---|---|---|
| Taxable persons | 2 | 3 | Change 2 to 3 |
| City tax per night | 8.40 | 12.60 | Difference 4.20 per night |
| City tax for the stay | 16.80 | 25.20 | 8.40 missing in total |

## What the app does

Input: the two exported lists (charges and registrations).
Processing: match guests by name, count taxable persons, compare the amounts.
Output: a list of differences and the values to correct, saved as a file.

## Course requirements

| Requirement | How the app meets it |
|---|---|
| Interactive (console) | Runs in the terminal, the user starts the daily city tax check and picks options from a menu. |
| Data validation | Checks that files exist, dates are real dates, person counts are whole numbers, menu choices are valid, and who is 12 or older. |
| File processing | Reads the two lists and writes a report of differences and corrections. |

## Scope

In scope:
* Compare the two exported lists
* Calculate the correct city tax per room
* List every difference and the fix

Out of scope:
* No connection to the hotel's PMS
* No automatic correction of the data
* No graphical interface

## Data

This repository contains no real guest data. All tests use a small fake dataset.

## User Stories

### Input
### Processing (owner: Timon)

#### User Story 1: Match guests across both lists

As a hotel receptionist, I want the app to find each guest's registration in the other list, so that I spend less time on the daily check.

Acceptance criteria:
1. Guests are matched by surname, the only field both lists have (List 1 has no date of birth).
2. Before matching, names are normalised: upper case, spaces trimmed, a leading "** " removed, accents removed ("Müller" = "MUELLER" = "MULLER").
3. A guest found in only one list is reported as "not matched", not skipped.
4. If the same surname appears in more than one room, the app flags it as "ambiguous" instead of guessing.

Example: Given "MÜLLER Hans" in room 101 of List 1 and "Müller, Hans" in the Meldeschein, when the lists are matched, then the app links both entries to room 101.

Edge case: Given "Weber" in the Meldeschein but in no row of List 1, then the app lists Weber as "not matched".

#### User Story 2: Count taxable guests

As a hotel receptionist, I want the app to work out how many guests are taxable, using date of birth and the 12-or-older rule, so that I no longer have to check children's ages by hand.

Acceptance criteria:
1. A guest's age is calculated on the arrival date (Anreise).
2. A guest aged 12 or older is taxable, under 12 is exempt (assumption, cutoff to confirm).
3. The app counts the taxable guests per room.
4. A missing or invalid date of birth is flagged, and the guest is counted as taxable until checked.

Example: Given a room with 4 guests aged 40, 38, 13 and 9 on the arrival date, when taxable guests are counted, then the result is 3.

Edge case: Given a guest who turns 12 during the stay, then the guest is still exempt, because age is taken on the arrival date.

#### User Story 3: Compare charged and correct city tax

As a hotel receptionist, I want the app to compare what List 1 charged with the correct amount and show the difference and the correction, so that guests are charged city tax for the right number of people.

Acceptance criteria:
1. Correct city tax per night = taxable guests × 4.20 CHF (assumption, rate to confirm).
2. Nights = departure date minus arrival date. Correct city tax per stay = per night × nights.
3. When the lists disagree, the Meldeschein counts as correct (assumption).
4. For every room with a difference, the app shows: room, guest name, persons in List 1, correct persons, amount charged, correct amount, difference.
5. Amounts are shown with 2 decimals. Rooms without a difference are not listed.

Example: Given room 101 charged in List 1 for 2 persons (8.40 per night) and 3 taxable guests for 2 nights, when the amounts are compared, then the app shows "Change 2 to 3, charged 16.80, correct 25.20, difference 8.40".

Edge case: Given a room where List 1 already matches the correct amount, then the room does not appear in the list of differences.

### Output
