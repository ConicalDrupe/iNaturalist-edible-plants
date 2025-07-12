-- Goal: Convert lat/lon to point and create gist indexes




with renamed as (
    Select
    A."gbifID" as gbifID
    ,A."occurrenceID" as occurrence_link
    ,A.family
    ,A.genus
    ,A.species
    ,A."taxonKey" as taxon_key
    ,A.state_providence as state
    ,A.lat
    ,A.lon
    ,A.coord_uncertainty as coordinate_uncertainty_meters
    ,A.coord_precision as coordinate_precision
    ,A.elevation
    ,A.elevation_accuracy
    ,A.occurrence_date
    ,A.identification_date
    ,"rightsHolder" as rights_holder
from {{ source('gbif','raw_obs') }} A
),

make_points as (
    Select
    R.gbifID::bigint
    ,R.occurrence_link::varchar(255)
    ,R.family
    ,R.genus
    ,R.species
    ,R.taxon_key::bigint
    ,R.state
    ,R.lat
    ,R.lon
    ,ST_POINT(R.lon,R.lat,4326) as geo_loc
    ,R.coordinate_uncertainty_meters
    ,R.elevation
    ,R.elevation_accuracy
    ,R.occurrence_date::date
    ,R.identification_date::date
    ,R.rights_holder
    from renamed R
)


Select *
from make_points
