{{ config(
    materialized='incremental'
    , incremental_strategy='merge'
    , unique_key=['driver_standings_id']
)}}

with renamed as (
    select
        driverStandingsId AS driver_standings_id, 
        raceId AS race_id,
        driverId AS driver_id,
        points,
        position,
        positionText AS position_text,
        wins

    from 
        {{ source('raw', 'driver_standings') }}
)
select 
    * 
from 
    renamed
{% if is_incremental() %}
where driver_standings_id > (
                    select 
                        max(driver_standings_id) 
                    from 
                        { { this } }
                    )
{% endif %}