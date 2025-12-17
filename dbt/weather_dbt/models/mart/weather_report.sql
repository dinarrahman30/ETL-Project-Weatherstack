{{ config(
    materialized='table',
    unique_key='id'
) }}

select
    id,
    city,
    temperature,
    weather_description,
    wind_speed,
    utc_offset,
    inserted_at_local
from {{ ref('stg_weather') }}