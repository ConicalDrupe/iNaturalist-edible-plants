{{ config(
    materialized='table',
    indexes=[
        {'columns': ['geo_loc'], 'type':'gist'}
    ]
) 
}}

-- {{ config(
--     materialized='incremental',
--     incremental_strategy='microbatch',
--     event_time='occurrence_date',
--     batch_size='month',
--     begin='2015-01-01',
--     unique_key='gbifID',
--     indexes=[
--         {'columns': ['geo_loc'], 'type':'gist'}
--     ]
-- ) 
-- }}
