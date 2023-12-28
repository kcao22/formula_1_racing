{{ config(
    materialized='incremental'
    , incremental_strategy='merge'
    , unique_key=['driver_key']
)}}

with driver_details as (
  select
    driver_id as driver_key
    , concat(driver_first_name, ' ', driver_last_name) as driver_name
    , datediff(year, cast(driver_date_of_birth as date), getdate()) as driver_age
    , driver_nationality
  from
    {{ ref('stg_drivers') }}
)
select 
  *
from 
  driver_details
{% if is_incremental() %}
where driver_key > (
                    select 
                        max(driver_key)
                    from 
                        {{ this }}
                    )
{% endif %}