#!/usr/bin/env python3
"""Validate and clean the synthetic Silwood tree survey."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "silwood_trees_raw.csv"
RESULTS_DIR = PROJECT_ROOT / "results" 

INPUT_FIELDS = [
    "record_id",
    "location",
    "genus",
    "species",
    "distance_m",
    "angle_degrees",
]
ISSUE_FIELDS = ["source_row", "record_id", "reasons"]
OAK_COUNT_FIELDS = ["species", "count"]


def load_records(path: Path = INPUT_PATH) -> list[dict[str, str]]:
    """Read the survey and check its column names."""
    with path.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != INPUT_FIELDS:
            raise ValueError(
                f"Expected columns {INPUT_FIELDS}, found {reader.fieldnames}"
            )
        return list(reader) # return a list of dictionaries, one per row {"record_id": "ST001", "genus": "Quercus", ...}


def validate_record(
    row: dict[str, str],
    source_row: int,
    accepted_ids: set[str], # Set of valid record IDs to check for uniqueness
) -> tuple[dict[str, str] | None, list[str]]:
    """Clean one record, or return the reasons it cannot be used."""
    reasons: list[str] = []
    # record_id validation
    # Remove surrounding whitespace -> Reference: https://stackoverflow.com/questions/1185524/how-do-i-trim-whitespace
    row["record_id"] = row["record_id"].strip() 
    # Check if record_id is empty
    if row["record_id"] == "":
        reasons.append("missing record_id")
    # Check for pattern: starts with "ST" followed by 3 digits
    elif len(row["record_id"]) != 5 or row["record_id"][0:2] != "ST" or not row["record_id"][2:].isdigit():
        reasons.append("invalid record_id")
    # Check for duplicate record_id
    elif row["record_id"] in accepted_ids:
        reasons.append("duplicate record_id")

    # location validation 
    # Remove surrounding whitespace and convert to title case -> Reference: https://stackoverflow.com/questions/8347048/how-to-convert-string-to-title-case-in-python
    row["location"] = row["location"].strip().title()
    # Correct capitalization for Nash's Field
    if row["location"] == "Nash'S Field":
        row["location"] = "Nash's Field"  
    # Check if location is empty
    if row["location"] == "":
        reasons.append("missing location")
    # Check if location is one of the valid options
    elif row["location"] not in ["Silwood Bottom", "Nash's Field", "Manor House", "Reactor Wood"]:  
        reasons.append("invalid location")

    # genus validation
    # Remove surrounding whitespace and convert to title case -> Reference: https://stackoverflow.com/questions/8347048/how-to-convert-string-to-title-case-in-python
    row["genus"] = row["genus"].strip().title()
    # Check if genus is empty
    if row["genus"] == "":
        reasons.append("missing genus")
    # Check if genus is one of the valid options
    elif row["genus"] not in ["Quercus", "Acer", "Betula", "Fagus", "Fraxinus"]:
        reasons.append("invalid genus")
    
    # species validation
    # Remove surrounding whitespace and convert to lower case
    row["species"] = row["species"].strip().lower()
    # Check if species is empty
    if row["species"] == "":
        reasons.append("missing species")
    # Check if species is one of the valid options
    elif row["species"] not in ["robur", "petraea", "pseudoplatanus", "pendula", "sylvatica", "excelsior"]:
        reasons.append("invalid species")

    # genus & species combination validation
    # Only check the combination if both genus and species are valid and not missing
    if "missing genus" not in reasons and "invalid genus" not in reasons and "missing species" not in reasons and "invalid species" not in reasons:
        valid_combinations = {
            "Quercus": ["robur", "petraea"],
            "Acer": ["pseudoplatanus"],
            "Betula": ["pendula"],
            "Fagus": ["sylvatica"],
            "Fraxinus": ["excelsior"],
        }
        if row["genus"] in valid_combinations:
            if row["species"] not in valid_combinations[row["genus"]]:
                reasons.append("invalid genus/species combination")     

    # distance_m validation
    # Check if distance_m is empty
    if row["distance_m"] == "":
        reasons.append("missing distance_m")
    else:
        # Check if distance_m is a valid number -> # Reference: https://www.reddit.com/r/learnpython/comments/dy8u90/anything_like_isdigit_that_would_work_for_floats/
        try: 
            float(row["distance_m"]) 
            # Check if distance_m is within the valid range (0-100)
            if float(row["distance_m"]) <= 0 or float(row["distance_m"]) > 100:
                reasons.append("distance_m out of range")
        except ValueError:
            reasons.append("invalid distance_m")
        
    # angle_degrees validation
    # Check if angle_degrees is empty
    if row["angle_degrees"] == "":
        reasons.append("missing angle_degrees")
    else:
        # Check if angle_degrees is a valid number, is a digit will also be finite 
        try:
            float(row["angle_degrees"]) 
            # Check if angle_degrees is within the valid range (0-90)
            if float(row["angle_degrees"]) <= 0 or float(row["angle_degrees"]) >= 90:
                reasons.append("angle_degrees out of range")
        except ValueError:
            reasons.append("invalid angle_degrees")

    # Return the cleaned row if there are no reasons, otherwise return None and the list of reasons
    if reasons:
        return None, reasons
    else:
        return row, []


def process_records(
    rows: Iterable[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Sort records into accepted rows and issue reports."""
    clean_rows: list[dict[str, str]] = []
    issue_rows: list[dict[str, str]] = []
    source_row = 1  # Initiate at header row and keep track of the row number 
    accepted_ids: set[str] = set()  # Set to keep track of accepted record to prevent duplicates
    
    # Validate each row and separate them into clean rows and issued rows
    for row in rows:
        source_row += 1 # Increment the source_row for each row processed & skipping the header
        clean_row, issue_row = validate_record(row, source_row, accepted_ids)
        if clean_row is not None:  
            clean_rows.append(clean_row)
            accepted_ids.add(row["record_id"])  # Add the record_id to the set of accepted IDs to prevent duplicates
        if issue_row:
            # Turn the list of reasons into a single string for the issue report
            issue_row = "; ".join(issue_row)
            issue_rows.append({"source_row": source_row, "record_id": row["record_id"], "reasons": issue_row})
   
    # Sort the clean rows by record_id and issue rows by source_row 
    clean_rows = sorted(clean_rows, key=lambda x: x["record_id"]) 
    issue_rows = sorted(issue_rows, key=lambda x: x["source_row"])
    return clean_rows, issue_rows


def summarise_oaks(clean_records: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    """Count accepted oak records by species."""
    oak_counts: dict[str, int] = {}
    for row in clean_records:
        if row["genus"] == "Quercus":
            species = row["species"]
            if species not in oak_counts:
                oak_counts[species] = 0
            oak_counts[species] += 1

    return [{"species": species, "count": count} for species, count in sorted(oak_counts.items())]

def write_csv(
    path: Path,
    fieldnames: list[str],
    rows: Iterable[dict[str, str]],
) -> None:
    """Write rows to a CSV file, replacing an older copy."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    """Clean the survey and write the three result files."""
    clean_records, issues = process_records(load_records(INPUT_PATH))
    oak_counts = summarise_oaks(clean_records)

    write_csv(
        RESULTS_DIR / "silwood_trees_clean.csv",
        INPUT_FIELDS,
        clean_records,
    )
    write_csv(
        RESULTS_DIR / "silwood_tree_issues.csv",
        ISSUE_FIELDS,
        issues,
    )
    write_csv(
        RESULTS_DIR / "oak_species_counts.csv",
        OAK_COUNT_FIELDS,
        oak_counts,
    )


if __name__ == "__main__":
    main()
