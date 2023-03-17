{{ config(materialized='table') }}

with youtube_data as (
    select *
    from {{ ref('stg_youtube_trends.sql') }}
) 
select 
*
from youtube_data
