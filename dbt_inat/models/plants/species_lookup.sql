-- Goal: create a lookup table for species on key or name

with observed_taxon_keys as (
    SELECT 
    DISTINCT 
    taxon_key,
    species,
    genus,
    family,
    taxon_rank
    from {{ ref('stg_observations') }}
),


-- stg_species_info has all the ediblity information
-- we will check if there are any that are null
Select
info.taxon_key as info_tk,
info.scientific_name as info_species,
obs.taxon_key as obs_tk,
obs.species as obs_species,
obs.genus as obs_genus,
obs.family as obs_family
from {{ ref('stg_species_info') }} info
OUTER JOIN observed_taxon_keys obs
ON info.taxon_key = obs.taxon_key
