-- Has all scientific name,rank, and edibility indicators

with all_edible_flags as (
SELECT 
    t1.name as book_name,
    t1.edibles,
    t2.STEMS_SHOOTS::smallint, 
    t2.LEAVES_GREENS::smallint, 
    t2.SPECIALIZED::smallint, 
    t2.ROOTS::smallint, 
    t2.FRUITS::smallint, 
    t2.PODS::smallint, 
    t2.FLOWERS_BUDS::smallint, 
    t2.SEEDS_NUTS::smallint, 
    t2.BARK_SAP::smallint,
    t1.e_stem::smallint, 
    t1.e_leaves::smallint, 
    t1.e_fiddleheads::smallint, 
    t1.e_root::smallint, 
    t1.e_heart::smallint, 
    t1.e_shoots::smallint, 
    t1.e_fruit::smallint, 
    t1.e_flower::smallint, 
    t1.e_seeds::smallint, 
    t1.e_cambium::smallint, 
    t1.e_needles::smallint, 
    t1.e_pollen::smallint, 
    t1.e_bark::smallint, 
    t1.e_immature_seed::smallint, 
    t1.e_tips::smallint, 
    t1.e_nuts::smallint, 
    t1.e_immature_fruit::smallint, 
    t1.e_sap::smallint, 
    t1.e_peel::smallint, 
    t1.e_immature_seeds::smallint, 
    t1.e_buds::smallint, 
    t1.e_immature_flower::smallint, 
    t1.e_shoot::smallint, 
    t1.e_stems::smallint, 
    t1.e_immature_buds::smallint, 
    t1.e_flowerbuds::smallint, 
    t1.e_fruits::smallint, 
    t1.e_roots::smallint, 
    t1.e_beans::smallint, 
    t1.e_galls::smallint, 
    t1.e_stalks::smallint, 
    t1.e_flowers::smallint, 
    t1.e_pith::smallint, 
    t1.e_immature_seedpods::smallint, 
    t1.e_immature_fruits::smallint,
    t1.source
    from {{ ref('edible_IM_granular') }} as t1
    inner join {{ ref('edible_IM_broad') }} as t2
    ON t1.name=t2.name
),

-- right join to filter out un-matched names and duplicates, that have been cleaned from the species match service
appended_taxon_keys as (
SELECT
    gbif.usageKey as taxon_key,
    gbif.canonicalname as scientific_name,
    gbif."rank" as taxon_rank,
    t1.*
    from all_edible_flags t1
    right join {{ ref('gbif_species_match_service') }} as gbif
    ON gbif.searchedName = t1.book_name
)

SELECT * 
from appended_taxon_keys
