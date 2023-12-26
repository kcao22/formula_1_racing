{{ config(
    materialized='incremental'
    , incremental_strategy='merge'
    , unique_key=['race_id']
)}}

with renamed as (
    select
        raceId AS race_id,
        driverId AS driver_id,
        stop,
        lap,
        time,
        duration,
        CAST(milliseconds AS BIGINT) / 1000.0 AS seconds

    from 
        {{ source('raw', 'pit_stops') }}
)
select 
    * 
from 
    renamed
{% if is_incremental() %}
where race_id > (
                    select 
                        max(race_id) 
                    from 
                        { { this } }
                    )