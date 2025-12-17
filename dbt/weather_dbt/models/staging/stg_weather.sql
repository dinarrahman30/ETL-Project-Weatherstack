{{ config(
    materialized='table', 
    unique_key='id'
) }}

WITH raw_data AS (
    SELECT *
    FROM {{ source('weather_source', 'weather_data') }}
),

ranked_data AS (
    SELECT
        id,
        city,
        temperature,
        weather_description,
        wind_speed,
        time,
        utc_offset,
        inserted_at,
        -- LOGIKA UTAMA: Unik berdasarkan Kota DAN Waktu
        ROW_NUMBER() OVER (
            PARTITION BY city, time 
            ORDER BY inserted_at DESC
        ) AS rn
    FROM raw_data
)

SELECT 
    id,
    city,
    temperature,
    weather_description,
    wind_speed,
    time,
    utc_offset,
    inserted_at,
    -- Syntax Postgres untuk menambah jam (asumsi utc_offset adalah angka jam, misal: 7)
    (inserted_at + (utc_offset::text || ' hours')::interval) as inserted_at_local
FROM ranked_data
WHERE rn = 1