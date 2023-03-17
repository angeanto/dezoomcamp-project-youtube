{{ config(materialized='view') }}

with youtube_data as 
(
  select *
  from {{ source('staging','youtube_trends') }}
)
select
*
from youtube_data

-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=False) %}

  limit 100

{% endif %}
