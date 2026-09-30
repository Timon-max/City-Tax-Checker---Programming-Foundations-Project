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
