#!/usr/bin/env bash
# Test get_TreeHeight.R

Rscript code/get_TreeHeight.R data/trees.csv

# stop if encounter any error
if [[ $? -ne 0 ]]; then
    exit 1
fi

