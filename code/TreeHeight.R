#!/usr/bin/env Rscript
# Read in tree.csv and calculate tree height.

tree_data <- read.csv("data/trees.csv")
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
# inspect all data is finite 
if (any(!is.finite(distance)) || any(!is.finite(angle))) {
  stop("ValueError: The values of Distance.m or Angle.degrees are not finite.")
}
# inspect the data range 
if (any(distance <= 0 | distance > 100) || any(angle <= 0 | angle >= 90)) {
  stop("RangeError: The values of Distance.m or 
    Angle.degrees are out of the expected range.")
}

# calculate tree height in meter 
TreeHeight <- function(distance, angle) {
  # convert angle from degrees to radians and calculate height
  distance * tan(angle * pi / 180)
}

tree_data$height_m <- TreeHeight(distance, angle)

# check the header of the data frame after adding the height column
if (!identical(names(tree_data),
               c("Species", "Distance.m", "Angle.degrees", "height_m"))) {
  stop("HeaderError: height_m column is not added to the data frame.")
}

# create results directory if it doesn't exist 
if (!dir.exists("results")) {
  dir.create("results")
}

# output the file
write.csv(tree_data, "results/TreeHts.csv", row.names = FALSE)