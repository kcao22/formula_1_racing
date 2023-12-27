{{ config(
    materialized='incremental'
    , incremental_strategy='merge'
    , unique_key=['constructor_key']
)}}

with constructor_details as (
  select
    constructor_id as constructor_key
    , name as constructor_name
    , nationality as constructor_nationality
  from
    {{ ref('stg_constructors') }}
)
select 
  *
from 
  constructor_details
{% if is_incremental() %}
where constructor_key > (
                    select 
                        max(constructor_key)
                    from 
                        {{ this }}
                    )
{% endif %}