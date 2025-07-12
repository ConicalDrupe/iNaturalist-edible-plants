Select 
obs.gbif_id
,obs.state as ob_state
,c.county
,c.county_fips
,c.state as state_matched
from {{ ref('stg_observations') }} obs
LEFT JOIN {{ ref('counties') }} c 
ON ST_DWITHIN(obs.geo_loc::geography,c.geom::geography,10)
