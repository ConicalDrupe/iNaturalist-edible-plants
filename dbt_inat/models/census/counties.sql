
with joined as (
SELECT 
    B.geoid::varchar(5)
    ,A.state
    ,B.name as county
    ,TRIM(B.statefp) as state_fips
    ,TRIM(B.countyfp) as county_fips
    ,A.centroid
    ,ST_TRANSFORM(B.geom,4326) as geom --translate to EPSG:4326
    from {{ ref('stg_county_centroids') }} A
    RIGHT JOIN {{ source('census', 'counties_shp') }} B 
    ON A.geoid = B.geoid
),

state_map as (
    SELECT 
    DISTINCT
    STATE
    ,state_fips
    from joined
    where STATE is not null
),

state_backfill as (
    SELECT
    A.geoid
    ,CASE WHEN A.state_fips = '60' THEN 'American Samoa'
          WHEN A.state_fips = '72' THEN 'Puerto Rico'
          WHEN A.state_fips = '66' THEN 'Guam'
          WHEN A.state_fips = '69' THEN 'Northern Marina Island'
          WHEN A.state_fips = '78' THEN 'Virgin Islands'
          ELSE B.state
          END as state
    ,A.county
    ,A.state_fips
    ,A.county_fips
    ,A.centroid
    ,A.geom
    ,CASE WHEN A.state_fips in ('60','72','66','69','78','02','15') then 'Outside Mainland'
          ELSE 'Mainland'
          end as mainland_flag
    from joined A
    left join state_map B
    on A.state_fips = B.state_fips
)

select *
from state_backfill
