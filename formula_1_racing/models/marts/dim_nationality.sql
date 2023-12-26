with nationalities as (
  select
    nationality
  from 
    { { ref('stg_constructors') } }
  union all
  select
    nationality
  from 
    { { ref('stg_drivers') } }
)
select 
  distinct nationality
from nationalities