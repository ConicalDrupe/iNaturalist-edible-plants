{{ config(
    materialized='table',
    indexes=[
        {'columns': ['occ_point'], 'type':'gist'}
    ]
) 
}}

with reverse_geocoded as 
(
    SELECT 
    obs.gbifid
    ,obs.species
    ,obs.taxon_key
    ,obs.state as ob_state
    ,c.geoid
    ,c.state
    ,c.county
    ,c.state_fips
    ,c.county_fips
    ,obs.coordinate_uncertainty_meters
    ,obs.elevation
    ,obs.elevation_accuracy
    ,obs.identification_date
    ,obs.lon
    ,obs.lat
    ,ST_SetSRID(ST_MakePoint(obs.lon,obs.lat),4326) as occ_point
    ,obs.occurrence_link
    ,obs.rights_holder
    ,ST_DISTANCE(obs.geo_loc,c.geom) as calculated_distance
    ,ROW_NUMBER() OVER (PARTITION BY gbifid order by ST_DISTANCE(obs.geo_loc,c.geom) desc) as distance_rank
    from {{ ref('stg_observations') }} obs
    LEFT JOIN {{ ref('counties') }} c 
    ON ST_DWITHIN(obs.geo_loc,c.geom,0.00000001)
)

SELECT 
    gbifid
    ,species
    ,taxon_key
    ,ob_state
    ,state
    ,county
    ,geoid
    ,state_fips
    ,county_fips
    ,coordinate_uncertainty_meters
    ,elevation
    ,elevation_accuracy
    ,identification_date
    ,lon
    ,lat
    ,occ_point
    ,occurrence_link
    ,rights_holder
from reverse_geocoded
where distance_rank = 1
