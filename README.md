# iNaturalist-edible-plants
An end-to-end data project for Hacklytics 2025. What are the edible plants of the USA?

# Text Extractor

*Add 10% margin to correct names - many of them were correct and just needed additional name*
Number of manual name entries: 378
Number of correct name entries: 211
Name extraction accuracy: 35.82%


Number of manual edibles entries: 294
Number of correct edibles entries: 295
Edible extraction accuracy: 50.08%

# PostgresSQL and Data Warehousing
Reverse Geocoding
Staging using dbt
Species Matchback (Genus returns many species not in original text)

## Extensions
- PostGIS
- pg_parquet

# Cenusus Data
Combined food-atlas data from 2019 to gauge county level poverty and SNAP benefits.
Food-Atlas Data comes in a finer grain, the CensusTract level. But we aggregated to county level, and recalculated margin of error to track accuracy of estimates.
Further joined population census data from 2024.

# Estimate Species Population By County
We use quadrant estimation to estimate the number of each species on a per-county basis.
This is done by laying a grid over the county where each grid box has area A, and randomly selecting grids and counting the number of observations of each species within the grid area A.
The distribution of observations in each grid are expeceted to follow a Poisson distribution.
This is then extrapolated to the entire area of the county. 
This workflow was done in QGIS - an open source Geographical Information System software.

# Dashboard

# Results

# Further Improvments
## Text Extraction
Text extraction could be improved in a variety of ways. Improve photo quality, refined promp engineering, giving an agent access to the gui tool.

## Estimations of Edible plants
Observed values are an underestimate of the size of plant communities
Baysian methods using a non-homogenous poisson proccess could get more feasable estimates of plant populations.

## Plant Nutrition
Calories were intuitively decided.
However foraged plants are known to have more vitimns and minerals than some agriculturally produced vegetables, which have delpeted soil health. And thus a less-nutritious product.

## GeoCoding
- Data near the boarders were unable to be matched
- Some observations had a high uncertainty, these were removed pre-proccess
