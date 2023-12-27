{{ config(
    materialized='incremental'
    , incremental_strategy='merge'
    , unique_key=['race_key']
)}}

with race_details as (
    select
        R.race_id as race_key
        , R.year as race_year
        , R.round_number as race_round_number
        , R.race_name
        , R.date as race_date
        , R.time as race_time
        , C.race_circuit_name
        , C.location as race_circuit_location
        , C.country as race_country
    from {{ ref('stg_races') }} R
        join {{ ref('stg_circuits' )}} C on
            R.circuit_id = C.circuit_id
)
select 
    *
from race_details
{% if is_incremental() %}
where race_key > (
                    select 
                        max(race_key)
                    from 
                        {{ this }}
                    )
{% endif %}