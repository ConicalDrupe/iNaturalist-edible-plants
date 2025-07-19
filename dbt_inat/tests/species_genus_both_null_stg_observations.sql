Select
species,genus
from {{ref('stg_observations')}}
where species is null and genus is null
