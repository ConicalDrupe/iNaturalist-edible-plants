-- Species that are only one word long
SELECT
*
from {{ref('stg_species_info')}}
where 1=1
AND first_of_canonical=scientific_name
AND taxon_rank = 'SPECIES'
