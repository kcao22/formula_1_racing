{{ config(
    materialized='incremental'
    , incremental_strategy='merge'
    , unique_key=['status_id']
)}}

with renamed as (
    select
        statusId AS status_id,
        status

    from
        {{ source('raw', 'status') }}
)
select 
    * 
from 
    renamed
{% if is_incremental() %}
where result_id > (
                    select 
                        max(status_id) 
                    from 
                        {{ this }}
                    )