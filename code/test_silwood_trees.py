#!/usr/bin/env python3
"""Test the validation and cleaning of the synthetic Silwood tree survey."""

from clean_silwood_trees import validate_record

# 1. Test that a valid record passes validation and returns no reasons for rejection
assert validate_record(
    {"record_id": "ST001", "location": "Silwood bottom", "genus": "Quercus", "species": "robur", "distance_m": "10.5", "angle_degrees": "45"}, 1, set()
) == (
    {"record_id": "ST001", "location": "Silwood Bottom", "genus": "Quercus", "species": "robur", "distance_m": "10.5", "angle_degrees": "45"},
    []
)
# 2. Test invalid record_id and distance_m
assert validate_record(
    {"record_id": "st002", "location": "Nash'S Field", "genus": "", "species": "robur", "distance_m": "ten", "angle_degrees": "45"}, 2, set()
) == (None, ["invalid record_id", "missing genus", "invalid distance_m"])
# 3. Test invalid genus/species combination and duplicate record_id
assert validate_record(
    {"record_id": "ST001", "location": "Silwood Bottom", "genus": "Quercus", "species": "excelsior", "distance_m": "10.5", "angle_degrees": "45"}, 3, {"ST001"}
) == (None, ["duplicate record_id", "invalid genus/species combination"])
# 4. distance_m and angle_degrees boundary tests at minimum (which should > but not = 0)
assert validate_record(
    {"record_id": "ST003", "location": "Silwood Bottom", "genus": "Quercus", "species": "robur", "distance_m": "0", "angle_degrees": "0"}, 4, {"ST001"}
) == (None, ["distance_m out of range", "angle_degrees out of range"])
# 4. distance_m and angle_degrees boundary tests at maximum (distance !> 100, angle < 90)
assert validate_record(                                     # distance = 100 would work, but angle = 90 would not work
    {"record_id": "ST003", "location": "Silwood Bottom", "genus": "Quercus", "species": "robur", "distance_m": "100", "angle_degrees": "90"}, 4, {"ST001"}
) == (None, ["angle_degrees out of range"])


from clean_silwood_trees import process_records

assert process_records(
    [{
        "record_id": "ST001",
        "location": "Nash's Field",
        "genus": "Quercus",
        "species": "robur",
        "distance_m": "10.5",
        "angle_degrees": "45"
    }, {
        "record_id": "ST001",
        "location": "Nash's Field",
        "genus": "Quercus",
        "species": "",
        "distance_m": "10.5",
        "angle_degrees": "45"
    }, {
        "record_id": "ST002",
        "location": "Nash's Fields",
        "genus": "Quercus",
        "species": "pseudoplatanus",
        "distance_m": "105",
        "angle_degrees": "zero"
    }]
) ==  (
    # List of cleaned records
    [{
        "record_id": "ST001",
        "location": "Nash's Field",
        "genus": "Quercus",
        "species": "robur",
        "distance_m": "10.5",
        "angle_degrees": "45"
    }],
    # List of issue reports
    [{
        "source_row": 3, 
        "record_id": "ST001",
        "reasons": "duplicate record_id; missing species"
    }, 
    {
        "source_row": 4, 
        "record_id": "ST002",
        "reasons": "invalid location; invalid genus/species combination; distance_m out of range; invalid angle_degrees"
    }]
)

from clean_silwood_trees import summarise_oaks

assert summarise_oaks([
    {"record_id": "ST001", "location": "Nash's Field", "genus": "Quercus", "species": "robur", "distance_m": "10.5", "angle_degrees": "45"},
    {"record_id": "ST002", "location": "Silwood Bottom", "genus": "Quercus", "species": "petraea", "distance_m": "15.0", "angle_degrees": "30"},
    {"record_id": "ST004", "location": "Nash's Field", "genus": "Quercus", "species": "robur", "distance_m": "33.0", "angle_degrees": "78"},
    {"record_id": "ST003", "location": "Manor House", "genus": "Acer", "species": "pseudoplatanus", "distance_m": "20.0", "angle_degrees": "60"},
]) == [
    # List of species counts for genus Quercus sorted by species name
    {"species": "petraea", "count": 1},
    {"species": "robur", "count": 2},
]