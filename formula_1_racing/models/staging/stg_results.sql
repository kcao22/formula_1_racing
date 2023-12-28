{{ config(
    materialized='incremental'
    , incremental_strategy='merge'
    , unique_key=['result_id']
)}}

with renamed as (
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
        time AS lap_time,
        TRY_CAST(milliseconds AS BIGINT) / 1000.0 AS seconds,
        fastestLap AS fastest_lap,
        rank,
        fastestLapTime AS fastest_lap_time,
        fastestLapSpeed AS fastest_lap_speed,
        statusId AS status_id

    from 
        {{ source('raw', 'results') }}
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
{% endif %}