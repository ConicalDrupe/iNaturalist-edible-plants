{{ config(
    materialized='table'
)}}

-- ~49k observations have dim_species values are null, signify a failed reverse geocode. Plotting these observations shows boundaries with the ocean. Likely the high resolution shapefile does not stretch this far.
-- Observations are filtered to where coordinate uncertainty is under 5 miles.
SELECT
    obs.gbifid
    ,obs.taxon_key
    ,sp.taxon_rank
    ,sp.scientific_name
    ,sp.genus
    ,sp.family
    ,obs.identification_date
    ,obs.geoid
    ,obs.county
    ,obs.state
    ,obs.county_fips
    ,obs.state_fips
    ,sp.edibles
    ,sp.stems_shoots
    ,sp.leaves_greens
    ,sp.specialized
    ,sp.roots
    ,sp.fruits
    ,sp.pods
    ,sp.flowers_buds
    ,sp.seeds_nuts
    ,sp.bark_sap
    ,sp.e_stem
    ,sp.e_leaves
    ,sp.e_fiddleheads
    ,sp.e_root
    ,sp.e_shoots
    ,sp.e_fruit
    ,sp.e_flower
    ,sp.e_seeds
    ,sp.e_cambium
    ,sp.e_needles
    ,sp.e_pollen
    ,sp.e_bark
    ,sp.e_immature_seed
    ,sp.e_tips
    ,sp.e_nuts
    ,sp.e_immature_fruit
    ,sp.e_sap
    ,sp.e_peel
    ,sp.e_immature_seeds
    ,sp.e_buds
    ,sp.e_immature_flower
    ,sp.e_shoot
    ,sp.e_stems
    ,sp.e_immature_buds
    ,sp.e_flowerbuds
    ,sp.e_fruits
    ,sp.e_roots
    ,sp.e_beans
    ,sp.e_galls
    ,sp.e_stalks
    ,sp.e_flowers
    ,sp.e_pith
    ,sp.e_immature_seedpods
    ,sp.e_immature_fruits
    ,obs.coordinate_uncertainty_meters
    ,obs.elevation
    ,obs.elevation_accuracy
from {{ref('fct_observations')}} obs
Left Join {{ref('dim_species')}} sp
ON obs.taxon_key = sp.taxon_key
WHERE 1=1
    AND obs.county_fips is not null -- Where dim_species values are null, signify a failed reverse geocode. Plotting these observations shows boundaries with the ocean. Likely the high resolution shapefile does not stretch this far.
    AND obs.coordinate_uncertainty_meters < 8049 -- coordinate uncertainty is under 5 miles

