{{ config(materialized='table',
          partition_by = {"field": "trending_date_timestamp","data_type": "timestamp","granularity": "day"},
          cluster_by = "categoryId"
          )}}

with youtube_data as (
    select *,
    cast(trending_date as timestamp) AS trending_date_timestamp
    from {{ ref('stg_youtube_trends') }}
) 
select 
*
from youtube_data
