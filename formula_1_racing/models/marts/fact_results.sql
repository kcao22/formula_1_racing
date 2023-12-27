{{ config(
    materialized='incremental'
    , incremental_strategy='merge'
    , unique_key=['result_id']
)}}

with result_details as (
    select
        R.result_id as result_key
        , R.race_id as race_key
        , R.driver_id as driver_key
        , R.constructor_id as constructor_key
        , R.lap_number
        , R.grid as starting_grid_position
        , case
            when is_numeric(try_cast(R.position_text) as int) = 1 then R.position_text 
            else 
        , 
    from {{ ref('stg_results') }} R
        join 
)
select 
    *
from result_details
{% if is_incremental() %}
where result_key > (
                    select 
                        max(result_key)
                    from 
                        {{ this }}
                    )
{% endif %}