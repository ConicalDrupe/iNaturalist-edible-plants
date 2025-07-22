-- Goal: create a lookup table for species on key or name. 
-- Has family,genus,species name, taxon_key, rank, and edible parts
with observed_taxon_keys as (
    SELECT 
    DISTINCT 
    taxon_key,
    species,
    genus,
    family
    from {{ ref('stg_observations') }}
),

-- TODO:
-- For species that have unknown values in stg_species_info
-- 1) Check if genus is in stg_species_info, and fill based on this
-- Otherwise: how did this key get in here? Likely from a genus key!

-- stg_species_info has all the ediblity information
-- we will check if there are any that are null

backfill_candidates as (
    SELECT
        info.taxon_key as info_tk,
        info.scientific_name as info_species,
        info.taxon_rank as info_rank,
        obs.taxon_key as obs_tk,
        obs.species as obs_species,
        obs.genus as obs_genus,
        obs.family as obs_family
    from {{ ref('stg_species_info') }} info
    RIGHT JOIN observed_taxon_keys obs -- Full outer join to see what species were not found!
    ON info.taxon_key = obs.taxon_key
    ),


----- Strategy -----
-- 0) Where info_tk is null, do the following
-- 1) join observations on species_info where info.rank = 'GENUS'
-- 2) These observations have the same edibilty as it's genera
-- 3) Create these new records and union to the stg_species_info table before joining on taxon_key

-- 2173/4949 - 43% of the unmatched species were matched to our edible list
taxons_to_union as (
    SELECT
        T1.obs_tk as taxon_key
        ,CASE WHEN T1.obs_species is null then T1.obs_genus 
              ELSE T1.obs_species 
              END as scientific_name
        ,T2.first_of_canonical
        ,CASE WHEN T1.obs_species is null then 'GENUS'
              ELSE 'SPECIES'
              END as taxon_rank
        -- ,T2.scientific_name
        -- ,T2.taxon_rank
        ,T2.book_name
        ,T2.edibles
        ,T2.stems_shoots
        ,T2.leaves_greens
        ,T2.specialized
        ,T2.roots
        ,T2.fruits
        ,T2.pods
        ,T2.flowers_buds
        ,T2.seeds_nuts
        ,T2.bark_sap
        ,T2.e_stem
        ,T2.e_leaves
        ,T2.e_fiddleheads
        ,T2.e_root
        ,T2.e_heart
        ,T2.e_shoots
        ,T2.e_fruit
        ,T2.e_flower
        ,T2.e_seeds
        ,T2.e_cambium
        ,T2.e_needles
        ,T2.e_pollen
        ,T2.e_bark
        ,T2.e_immature_seed
        ,T2.e_tips
        ,T2.e_nuts
        ,T2.e_immature_fruit
        ,T2.e_sap
        ,T2.e_peel
        ,T2.e_immature_seeds
        ,T2.e_buds
        ,T2.e_immature_flower
        ,T2.e_shoot
        ,T2.e_stems
        ,T2.e_immature_buds
        ,T2.e_flowerbuds
        ,T2.e_fruits
        ,T2.e_roots
        ,T2.e_beans
        ,T2.e_galls
        ,T2.e_stalks
        ,T2.e_flowers
        ,T2.e_pith
        ,T2.e_immature_seedpods
        ,T2.e_immature_fruits
        ,T2.edible_source
    from (Select * from backfill_candidates where info_tk is null) T1
    RIGHT JOIN (select * from {{ ref('stg_species_info') }} where taxon_rank='GENUS') T2
    ON T1.obs_genus = T2.scientific_name 
    where T1.obs_tk is not null
),
-- select * from taxons_to_union;

-- Joining on backfill_candidates to get genus and family
final as (
    Select 
        M.taxon_key,
        M.scientific_name,
        T2.obs_genus,
        T2.obs_family, 
        M.taxon_rank,
        M.book_name,
        M.edibles,
        M.species,
        M.species_key,
        M.genus,
        M.genus_key,
        M.family,
        M.family_key,
        M.stems_shoots,
        M.leaves_greens,
        M.specialized,
        M.roots,
        M.fruits,
        M.pods,
        M.flowers_buds,
        M.seeds_nuts,
        M.bark_sap,
        M.e_stem,
        M.e_leaves,
        M.e_fiddleheads,
        M.e_root,
        M.e_heart,
        M.e_shoots,
        M.e_fruit,
        M.e_flower,
        M.e_seeds,
        M.e_cambium,
        M.e_needles,
        M.e_pollen,
        M.e_bark,
        M.e_immature_seed,
        M.e_tips,
        M.e_nuts,
        M.e_immature_fruit,
        M.e_sap,
        M.e_peel,
        M.e_immature_seeds,
        M.e_buds,
        M.e_immature_flower,
        M.e_shoot,
        M.e_stems,
        M.e_immature_buds,
        M.e_flowerbuds,
        M.e_fruits,
        M.e_roots,
        M.e_beans,
        M.e_galls,
        M.e_stalks,
        M.e_flowers,
        M.e_pith,
        M.e_immature_seedpods,
        M.e_immature_fruits
        from (
                Select * from taxons_to_union
                UNION
                Select * from {{ ref('stg_matchback') }}
             ) M
        LEFT JOIN backfill_candidates T2
        on M.taxon_key = T2.obs_tk
)

select * from final
