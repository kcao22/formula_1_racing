{{ config(
    materialized='incremental'
    , incremental_strategy='merge'
    , unique_key=['result_id']
)}}

with source as (
      select * from 
),
renamed as (
    select
        resultId AS result_id,
        raceId AS race_id,
        driverId AS driver_id,
        constructorId AS constructor_id,
        number AS lap_number,
        grid,
        position,
        positionText AS position_text,
        positionOrder AS position_order,
        points,
        laps,
        time,
        CAST(milliseconds AS BIGINT) / 1000.0 AS seconds,
        fastestLap AS fastest_lap,
        fastestLapTime AS fastest_lap_time,
        statusId AS status_id

    from
        {{ source('raw', 'sprint_results') }}
)
select 
    * 
from 
    renamed
{% if is_incremental() %}
where result_id > (
                    select 
                        max(result_id) 
                    from 
                        {{ this }}
                    )