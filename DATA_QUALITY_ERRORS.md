# Data Quality Errors

1) Observations have null counties
    - counties and observation join had no result. Where are these coordinates?

2) Species Lookup Table needs matchback service
    - There are many taxon keys in observations that are not in species lookup table
    - Are there any species in the book that are only the family? I think not...
    - Ex. Rosa genus 

    - Current solution: 
        1) Filter out FAMILY rank in stg_species_lookup
        2) Filter out where genus is null in stg_observations
