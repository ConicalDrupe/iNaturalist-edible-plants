-- If a results returns, this means a GENUS has two distinct taxon keys

with taxon_key_counts as (
        Select
        count(DISTINCT A.taxon_key) as key_count, A.scientific_name
        from {{ref('stg_species_info')}} A
        INNER JOIN{{ref('stg_species_info')}} B
        ON A.scientific_name = B.scientific_name
        Where A.taxon_rank = 'GENUS'
        group by A.taxon_key,A.scientific_name
    )

Select * 
from taxon_key_counts
where key_counts > 1
