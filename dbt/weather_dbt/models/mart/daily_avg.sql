{{ config(
    materialized='table',
    unique_key='id'
) }}

select
    city,
    date(time) as date,
    round(avg(temperature)::numeric, 2) as avg_temperature,
    round(avg(wind_speed)::numeric, 2) as avg_wind_speed
from {{ ref('stg_weather') }}
group by city, DATE(time)
order by date DESC, city