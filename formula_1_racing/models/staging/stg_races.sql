{{ config(
    materialized='incremental'
    , incremental_strategy='merge'
    , unique_key=['race_id']
)}}

with renamed as (
    select
        raceId AS race_id,
        year,
        round AS round_number,
        circuitId AS circuit_id,
        name AS race_name,
        date,
        time,
        url AS race_url,
        fp1_date,
        fp1_time,
        fp2_date,
        fp2_time,
        fp3_date,
        fp3_time,
        quali_date AS qualification_date,
        quali_time AS qualification_time,
        sprint_date,
        sprint_time

    from
        {{ source('raw', 'races') }}
)
select 
    * 
from 
    renamed
{% if is_incremental() %}
where race_id > (
                    select 
                        max(race_id) 
                    from 
                        { { this } }
                    )