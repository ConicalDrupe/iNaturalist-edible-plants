Select
scientific_name,genus
from {{ref('observations')}}
where scientific_name is null and genus is null
