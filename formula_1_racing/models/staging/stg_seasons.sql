{{ config(
    materialized='incremental'
    , incremental_strategy='merge'
    , unique_key=['year']
)}}

with renamed as (
    select
        year,
        url AS season_url
    from
        {{ source('raw', 'seasons') }}
)
select 
    * 
from 
    renamed
{% if is_incremental() %}
where year > (
                    select 
                        max(year) 
                    from 
                        {{ this }}
                    )