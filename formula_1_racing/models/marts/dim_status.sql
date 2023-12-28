with status_details as (
  select
    status_id as status_key
    , status as status_desc
  from
    {{ ref('stg_status') }}
)
select 
  *
from 
  status_details
