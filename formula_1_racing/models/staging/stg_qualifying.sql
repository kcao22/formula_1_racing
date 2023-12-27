{{ config(
    materialized='incremental'
    , incremental_strategy='merge'
    , unique_key=['qualify_id']
)}}

with renamed as (
    select
        qualifyId AS qualify_id,
        raceId AS race_id,
        driverId AS driver_id,
        constructorId AS constructor_id,
        number,
        position,
        q1,
        q2,
        q3

    from
        {{ source('raw', 'qualifying') }}
)
select 
    * 
from 
    renamed
{% if is_incremental() %}
where qualify_id > (
                    select 
                        max(qualify_id) 
                    from 
                        {{ this }}
                    )