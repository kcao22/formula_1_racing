{{ config(
    materialized='incremental'
    , incremental_strategy='merge'
    , unique_key=['constructor_id']
)}}

with renamed AS (
    select
        constructorId AS constructor_id,
        constructorRef AS constructor_reference,
        name,
        nationality,
        url AS constructor_url

    from 
        {{ source('raw', 'constructors') }}
)
select 
    * 
from 
    renamed
{% if is_incremental() %}
where constructor_id > (
                    select 
                        max(constructor_id) 
                    from 
                        {{ this }}
                    )
{% endif %}