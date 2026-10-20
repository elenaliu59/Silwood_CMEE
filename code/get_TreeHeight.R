#!/usr/bin/env Rscript
# Take the csv as an argument to calculate tree height.

argument <- commandArgs(trailingOnly = TRUE)
# report for no or extra argument
if (length(argument) == 0 || length(argument) > 1) {
    stop("ArgumentError: Missing argument or extra arguments")
}
# report for missing file
if (!file.exists(argument)) {
    stop("MissingFile: File not found")
}

# read in csv
tree_data <- read.csv(argument)


# reuse parts of TreeHeight code
distance <- tree_data$Distance.m
angle <- tree_data$Angle.degrees

# inspect header of the data 
if (!identical(names(tree_data), c("Species", "Distance.m", "Angle.degrees"))) {
  stop("HeaderError: The header of the data is not as expected.")
}
# inspect the data type is numeric
if (!is.numeric(distance) || !is.numeric(angle)) {
  stop("TypeError: The values of Distance.m or Angle.degrees are not numeric.")
}
# inspect the data is finite 
if (any(!is.finite(distance)) || any(!is.finite(angle))) {
  stop("ValueError: The values of Distance.m or Angle.degrees are not finite.")
}
# inspect the data range 
if (any(distance <= 0 | distance > 100) || any(angle <= 0 | angle >= 90)) {
  stop("RangeError: The values of Distance.m or 
    Angle.degrees are out of the expected range.")
}

# calculate tree height in meter 
calculate_tree_height <- function(distance, angle) {
  # convert angle from degrees to radians and calculate height
  distance * tan(angle * pi / 180)
}

tree_data$height_m <- calculate_tree_height(distance, angle)

# check the header of the data frame after adding the height column
if (!identical(names(tree_data),
               c("Species", "Distance.m", "Angle.degrees", "height_m"))) {
  stop("HeaderError: height_m column is not added to the data frame.")
}


# extract the file name of the input 
# reference: https://stackoverflow.com/questions/29113973/get-filename-without-extension-in-r
basename <- tools::file_path_sans_ext(basename(argument))

# output the csv in basename_treeheight.csv
write.csv(tree_data, file.path("results", paste0(basename, "_treeheights.csv")), row.names = FALSE)


