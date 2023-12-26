{{
  config(
    materialized = 'incremental',
    unique_key = 'id',
    merge_update_columns = ['column_name']
  )
}}


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