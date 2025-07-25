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

3) Some species/genus from raw gbif_matchback_service has incorrect rank labeling:
 taxon_key | scientific_name  | taxon_rank | first_of_canonical 
-----------+------------------+------------+--------------------
  11599995 | Acer             | SPECIES    | Acer

4) In Matchback Engine, it is possible for a species/genus to have several taxon_keys.
- It is possible this issue would be eliminated upon upgrade the match api from v1 to v2 gbif/species/match/v2 
- There is also likely an api that matches homonym keys to a singular key
- Perphaps tho Inclusion of SPECIES_KEY, GENUS_KEY ,or FAMILY_KEY could help. if taxon_key == SPECIES_KEY then it is a species, same for genus,family,etc..
    - Use the /species/{usageKey}/parent/ api!
