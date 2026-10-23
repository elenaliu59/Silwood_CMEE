#!/usr/bin/env Rscript
# 

### data input code from data wrang.R
# Load the data ----------------------------------------------------------
# The first rows describe the sampling design, so do not use one as a header yet.
MyData <- as.matrix(read.csv("data/pound_hill_data.csv", header = FALSE))

# The metadata file does have a header and uses semicolons as separators.
MyMetaData <- read.csv("data/pound_hill_meta_data.csv", header = TRUE, sep = ";")

# Inspect the data -------------------------------------------------------
head(MyData)
dim(MyData)
str(MyData)
head(MyMetaData)

# Transpose so species become columns and sampled quadrats become rows.
MyData <- t(MyData) 
head(MyData)
dim(MyData)

# For this dataset, we have been told that blanks are observed absences.
# That knowledge is what allows us to record them as zero rather than NA.
MyData[MyData == ""] <- 0

# Convert the raw matrix to a data frame --------------------------------

TempData <- as.data.frame(MyData[-1, ], stringsAsFactors = FALSE)
colnames(TempData) <- MyData[1, ]
rownames(TempData) <- NULL

# Convert from wide to long form ----------------------------------------
# This script keeps the older reshape2 route because it is still common in
# ecological code. For new work, the chapter introduces tidyr::pivot_longer().
library(reshape2)

MyWrangledData <- melt(
  TempData,
  id = c("Cultivation", "Block", "Plot", "Quadrat"),
  variable.name = "Species",
  value.name = "Count"
)

MyWrangledData[, "Cultivation"] <- as.factor(MyWrangledData[, "Cultivation"])
MyWrangledData[, "Block"] <- as.factor(MyWrangledData[, "Block"])
MyWrangledData[, "Plot"] <- as.factor(MyWrangledData[, "Plot"])
MyWrangledData[, "Quadrat"] <- as.factor(MyWrangledData[, "Quadrat"])
# check that the count is a positive value numeric
count <- suppressWarnings(as.integer(MyWrangledData[, "Count"]))
# invalid strings will turn into NA, so is.na check for non-numeric count
if (any(count < 0) || any(is.na(count))) {
    stop("ValueError: Count must be a valid positive integer")
}
MyWrangledData[, "Count"] <- as.integer(MyWrangledData[, "Count"])

str(MyWrangledData)
head(MyWrangledData)
dim(MyWrangledData)

# Save a derived table while leaving the raw files unchanged.
dir.create("results", showWarnings = FALSE)
write.csv(MyWrangledData, "results/pound_hill_long.csv", row.names = FALSE)


### Explore the data below this line.
library(dplyr)
library(tidyverse)

# determine the number of species
species_number <- length(unique(MyWrangledData$Species))

# quadrat-level table with Richness (count > 0) for each quadrat
quadrat_level_richness <- MyWrangledData %>%
    group_by(Cultivation, Block, Plot, Quadrat) %>% 
    summarise(Richness = sum(Count > 0))
# determine the number of quadrat
quadrat_number <- nrow(quadrat_level_richness)

# plot-level summary of mean richness
plot_level_richness <- quadrat_level_richness %>%
    group_by(Cultivation, Block, Plot) %>%
    summarise(MeanRichness = mean(Richness))
# determine the number of plot
plot_number <- nrow(plot_level_richness)

write.csv(plot_level_richness, "results/pound_hill_plot_richness.csv", row.names = FALSE)

### plot the plot-level mean richness among 3 cultivations
library(ggplot2)

pdf("results/pound_hill_richmess.pdf", 11.7, 8.3)
p <- ggplot(plot_level_richness, aes(x = Cultivation, y = MeanRichness)) +
    geom_boxplot() + geom_point() + 
    labs(x = "Caltivation Treatments", y = "Plot-level Mean Richness")
print(p)
dev.off();

# Cultivation treatment in May has the highest species richness
# Species richness is highly variable within each cultivation treatment, with the lowest variation in October
# The figure alone does not show that cultivation timing CAUSE difference in species richness, it only shows correlation
# There must not be any confounder within each treatment 

## do the same thing for abundance
# quadrat-level table with abundance (number of each species) for each quadrat
quadrat_level_abundance <- MyWrangledData %>%
    group_by(Cultivation, Block, Plot, Quadrat) %>% 
    summarise(Abundance = sum(Count))

# plot-level summary of mean abundance
plot_level_abundance <- quadrat_level_abundance %>%
    group_by(Cultivation, Block, Plot) %>%
    summarise(MeanAbundance = mean(Abundance))

write.csv(plot_level_abundance, "results/pound_hill_plot_abundance.csv", row.names = FALSE)