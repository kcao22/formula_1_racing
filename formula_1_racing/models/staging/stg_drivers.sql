{{ config(
    materialized='incremental'
    , incremental_strategy='merge'
    , unique_key=['driver_id']
)}}

with renamed as (
    select
        driverId AS driver_id,
        driverRef AS driver_reference,
        number AS driver_number,
        code AS driver_code,
        forename AS driver_first_name,
        surname AS driver_last_name,
        dob AS driver_date_of_birth,
        nationality AS driver_nationality,
        url AS driver_url

    from 
        {{ source('raw', 'drivers') }}
)
select 
    * 
from 
    renamed
{% if is_incremental() %}
where driver_id > (
                    select 
                        max(driver_id) 
                    from 
                        { { this } }
                    )
{% endif %}