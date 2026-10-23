Author: Elena Shuyue Liu
Root Directory: CMEE

Assignment 2 (Tree-survey)
- COMMAND: running using Python3
	running program: code/clean_silwood_trees.py
	testing program: code/test_silwood_trees.py
- INPUT FILE: data/silwood_trees_raw.csv
- PURPOSE: Validate every record, separating the cleaned rows from the issue rows, and count the number of each oak species 
- FUNCTIONS
	- validate_record(row, source_row, accepted_ids) -> cleaned_row | None, reasons 
		read in single rows and check whether each column is valid, store and return all invalid reasons
	- process_records(row) -> clean_rows, issue_rows
		separate clean rows (sort by record_id) and issue rows (sort by source_row) 
	- summarise_oaks(clean_records) -> list of oak_counts
		count the number of each Quercus species 
- TESTING FILE: code/test_silwood_trees.py
- OUTPUT FILE: results/
				silwood_trees_clean.csv
				silwood_trees_issues.csv
				oak_species_counts.csv

	
		
Assignment 3 
1. Tree Height 
- COMMAND: bash code/run_get_TreeHeight.sh
				will run get_TreeHeight.R
			Rscript code/TreeHeight.R 
- INPUT FILE: data/trees.csv
- PURPOSE: Inspect the original file has valid column name, valid values and then calculate the tree height 
- FUNCTION
	- TreeHeight(distance, angle)
		calculate tree height using distance and angle data from the input csv 
- OUTPUT FILE: results/TreeHts.csv

2. Pound Hill
- COMMAND:Rscript code/pound_hill_analysis.R
- INPUT FILE: data/pound_hill_data.csv
- PURPOSE: Transpose the raw data into long table format and summarize species richness and abundance in qudrate- and plot-level tables and print out the plot-level summary boxplot in pdf
- OUTPUT FILE: results/
	pound_hill_plot_richness.csv
	pound_hill_plot_richness.pdf
	pound_hill_plot_abundance.csv