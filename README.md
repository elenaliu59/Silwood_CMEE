


Assignment 2
- FILE INPUT: /data/silwood_trees_raw.csv
- Validate every record, separating the cleaned rows from the issue rows, and count the number of each oak species 
- FUNCTIONS
	- validate_record(row, source_row, accepted_ids) -> cleaned_row | None, reasons 
		read in single rows and check whether each column is valid, store and return all invalid reasons
- FILE OUTPUT: /results/
				silwood_trees_clean.csv
				silwood_trees_issues.csv
				oak_species_counts.csv