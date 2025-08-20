
with county_area as (
    Select 
        geoid
        ,state
        ,county
        ,ST_AREA(ST_TRANSFORM(geom,54034)) as area_sq_meters
    from {{ ref('counties') }}
),

grid_counts as (
    Select
        grid.id as gridID
        ,obs.geoid
        ,obs.state
        ,obs.county
        ,obs.species
        ,count(*) as cnt
    from {{ source('qgis','filtered_and_clipped_worldgrid_ersi24034') }} as grid
    INNER JOIN {{ ref('fct_observations') }} as obs
    ON st_contains(grid.geom,st_transform(obs.occ_point,54034))
    group by 
        grid.id 
        ,obs.geoid
        ,obs.state
        ,obs.county
        ,obs.species
)

Select 
    grid.*
    ,area.area_sq_meters
from grid_counts as grid
LEFT JOIN county_area as area
ON grid.geoid = area.geoid
