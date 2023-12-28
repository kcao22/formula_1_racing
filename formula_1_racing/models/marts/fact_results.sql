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
        , case 
            when R.lap_number = '\N' then 0
            else R.lap_number
        end as lap_number
        , R.grid as starting_grid_position
        , case
            when isnumeric(try_cast(R.position_text as int)) = 1 then R.position_order
            else 0
        end as position_num_key
        , case
            when R.position_text = 'D' then 1
            when R.position_text = 'E' then 2
            when R.position_text = 'F' then 3
            when R.position_text = 'N' then 4
            when R.position_text = 'R' then 5
            when R.position_text = 'W' then 6
            else 0
        end as position_text_key
        , points
        , case
            when R.rank = '\N' then 0 
            else R.rank 
        end as fastest_lap_rank
        , R.status_id as status_key
    from {{ ref('stg_results') }} R
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