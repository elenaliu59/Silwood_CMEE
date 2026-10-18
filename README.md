Author: Elena Shuyue Liu

Assignment 2
- FILE INPUT: /data/silwood_trees_raw.csv
- PURPOSE: Validate every record, separating the cleaned rows from the issue rows, and count the number of each oak species 
- FUNCTIONS
	- validate_record(row, source_row, accepted_ids) -> cleaned_row | None, reasons 
		read in single rows and check whether each column is valid, store and return all invalid reasons
	- process_records(row) -> clean_rows, issue_rows
		separate clean rows (sort by record_id) and issue rows (sort by source_row) 
	- summarise_oaks(clean_records) -> list of oak_counts
		count the number of each Quercus species 
- FILE OUTPUT: /results/
				silwood_trees_clean.csv
				silwood_trees_issues.csv
				oak_species_counts.csv
- COMMAND
	running program: code/clean_silwood_trees.py
	testing program: code/test_silwood_trees.py