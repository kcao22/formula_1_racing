{{ config(
    materialized='incremental'
    , incremental_strategy='merge'
    , unique_key=['constructor_standings_id']
)}}

with renamed as (
    select
        constructorStandingsId AS constructor_standings_id,
        raceId AS race_id,
        constructorId AS constructor_id,
        points,
        position,
        positionText AS position_text,
        wins

    from 
        {{ source('raw', 'constructor_standings') }}
)
select 
    * 
from 
    renamed
{% if is_incremental() %}
where constructor_standings_id > (
                    select 
                        max(constructor_standings_id) 
                    from 
                        {{ this }}
                    )
{% endif %}

  