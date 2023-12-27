{{ config(
    materialized='incremental'
    , incremental_strategy='merge'
    , unique_key=['circuit_id']
)}}

with renamed AS (
    select
        circuitId AS circuit_id,
        circuitRef AS circuit_ref,
        name AS circuit_name,
        location AS circuit_location,
        country,
        lat AS latitude,
        lng AS longitude,
        alt AS altitude,
        url AS circuit_url

    from 
        {{ source('raw', 'circuits') }}
)
select 
    * 
from 
    renamed
{% if is_incremental() %}
where circuit_id > (
                    select 
                        max(circuit_id) 
                    from 
                        {{ this }}
                    )
{% endif %}

