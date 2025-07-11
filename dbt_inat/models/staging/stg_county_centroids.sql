with renamed as (
SELECT
    TRIM(FIPS_CD::varchar(5)) as geoid, -- 5 digit state_fips+county_fips
    TRIM(STATE) as state,
    TRIM(NAME) as county,
    POPULATION as population_2020,
    POP_SQMI as population_per_sq_mile,
    SQMI as area_in_square_miles,
    LATITUDE as lat,
    LONGITUDE as lon,
    ST_POINT(LONGITUDE,LATITUDE,4326) as centroid
    from {{ ref('raw_county_centroids') }}
),

fips_formatted as (
SELECT
    CASE WHEN LENGTH(geoid)=4 THEN CONCAT('0',geoid)
         ELSE geoid
         END as geoid,
    state,
    county,
    population_2020,
    population_per_sq_mile,
    area_in_square_miles,
    lat,
    lon,
    centroid
    from renamed
),

add_state_county as (
SELECT
    geoid,
    state,
    county,
    SUBSTRING(geoid,1,2)::varchar(2) as state_fips,
    SUBSTRING(geoid,3,5)::varchar(3) as county_fips,
    population_2020,
    population_per_sq_mile,
    area_in_square_miles,
    lat,
    lon,
    centroid
    from fips_formatted
)

Select *
from add_state_county

