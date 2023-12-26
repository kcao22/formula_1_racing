{{ config(
    materialized='incremental'
    , incremental_strategy='merge'
    , unique_key=['constructor_results_id']
)}}

with renamed AS (
    select
        constructorResultsId AS constructor_results_id,
        raceId AS race_id,
        constructorId AS constructor_id,
        points,
        status

    from 
        {{ source('raw', 'constructor_results') }}
)
select 
    * 
from 
    renamed
{% if is_incremental() %}
where constructor_results_id > (
                    select 
                        max(constructor_results_id) 
                    from 
                        { { this } }
                    )
{% endif %}

  