# Explore the edible potential of Georgia's plants

# Project Charter
1) Mine Foraging Textbook for Edible plant Species, edible parts, Habitat found, and description
2) Collect raw iNaturalist Data set via GBIF API
- Data Includes: Species Name, Longitude, Lattitude, GBIFID (Unique Identifier), hyperlink to Image if any, Altitude, Uncertainty of Location, Observation Quality, Country of Origin
- Reverse Geo-code iNaturalist Longitude/Lattitude to get County Classification
- Combine with SNAP and Poverty data from Atlanta Regional Commission
3) Use LLM for text processing of Mined Textbook data, to classify harvest times of each edible plant part
4) Use caloric estimatnes on types of foods (nuts, lettuce, roots) to get caloric estimate of foods during season
5) Visualize in interactive Dashboard


## What could be visualized
- SNAP benefits, Population, Poverty Rates
- Concentration of observations, coorelated with population
- Seasonality of food availability (by month, by edible part)
- Break down of origin of plants (Native, non native). (shrub, herb, tree, etc...)


