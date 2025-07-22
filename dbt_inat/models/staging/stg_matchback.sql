-- Edible genus in
with edible_genus as (
    Select *
    from public_staging.stg_species_info
    where taxon_rank = 'GENUS'
),

-- Appending edibles. Note not all records were able to be matched
edibles_appended as (
    Select 
    unk.*, 
    eg.stems_shoots,
    eg.leaves_greens,
    eg.specialized,
    eg.roots,
    eg.fruits,
    eg.pods,
    eg.flowers_buds,
    eg.seeds_nuts,
    eg.bark_sap,
    eg.e_stem,
    eg.e_leaves,
    eg.e_fiddleheads,
    eg.e_root,
    eg.e_heart,
    eg.e_shoots,
    eg.e_fruit,
    eg.e_flower,
    eg.e_seeds,
    eg.e_cambium,
    eg.e_needles,
    eg.e_pollen,
    eg.e_bark,
    eg.e_immature_seed,
    eg.e_tips,
    eg.e_nuts,
    eg.e_immature_fruit,
    eg.e_sap,
    eg.e_peel,
    eg.e_immature_seeds,
    eg.e_buds,
    eg.e_immature_flower,
    eg.e_shoot,
    eg.e_stems,
    eg.e_immature_buds,
    eg.e_flowerbuds,
    eg.e_fruits,
    eg.e_roots,
    eg.e_beans,
    eg.e_galls,
    eg.e_stalks,
    eg.e_flowers,
    eg.e_pith,
    eg.e_immature_seedpods,
    eg.e_immature_fruits
    from public_raw.gbif_species_unknown_matchback unk
    INNER JOIN edible_genus eg
    ON unk.genus_key = eg.genus_key
)

Select * 
from edibles_appended
