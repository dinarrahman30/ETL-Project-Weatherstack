# 🌦️ Automated Weather Data ETL Pipeline

## End-to-End ETL Pipeline Project Using Podman (Alternate Docker), Airflow, PostgreSQL, and Metabase

## Project Overview
Project ini adalah sistem End-to-End Data Engineering Pipeline yang dirancang untuk mengotomatisasi proses pengambilan (Extract), penyimpanan (Load), dan tranformasi (Transform) data cuaca secara berkala.

Sistem ini mengambil data cuaca real-time dari Weatherstack API untuk 8 kota besar dunia (Jakarta, London, New York, Tokyo, dll), menyimpannya ke dalam Data Warehouse berbasis PostgreSQL, melakukan transformasi data menggunakan dbt (data build tool) untuk kebutuhan analitik, dan diorkestrasi sepenuhnya menggunakan Apache Airflow.

Tech Stack:
- Orchestrasion: Apache Airlfow (Running on Podman)
- Language: Python 3.10 (Custom Scripting)
- Data Warehouse: PostgreSQL 13
- Transformation: dbt (data build tool) Core
- Visualization: Metabase (Dashboarding)
- Insfrastucture: Podman Containerization
- External API: Weatherstack API 

Arsitektur & Alur Data (Data Flow)
1. Ingestion (Extract & Load)
    - Apache Airflow memicu task Python (api-weather-ingest) sesuai jadwal.
    - Script Python melakukan request ke API cuaca (mendukung mode Live API dan Mock Data untuk efisiensi kuota).
    - Data mentah (Raw Data) disimpan ke tabel weather_data di PostgreSQL dengan penanganan duplikasi (ON CONFLICT DO NOTHING).
2. Transformation (Transform)
    - Setelah data masuk, Airflow memicu task dbt (dbt-weather-transformation).
    - dbt membersihkan data (stg_weather), menghitung agregat seperti rata-rata suhu harian (daily_avg), dan menyusun tabel laporan final (weather_report).
    - Data Quality Tests dijalankan otomatis oleh dbt untuk memastikan integritas data.

3. Visualization
    - Data yang sudah bersih dihubungkan ke Metabase untuk visualisasi tren suhu dan cuaca antar kota.

### Fitur Utama (Key Features)
- Smart API Handling: Memiliki fitur toggle untuk beralih antara data Live (API) dan data Mock (Dummy) guna menghemat kuota API saat pengembangan.
- Idempotency: Pipeline dirancang agar aman dijalankan berulang kali tanpa membuat data duplikat di database.
- Modular Code: Pemisahan logika ekstraksi (Python) dan transformasi (SQL/dbt) sesuai prinsip Separation of Concerns.
- Containerized Environment: Seluruh infrastruktur berjalan di dalam container (Docker/Podman) sehingga mudah direplikasi di mesin manapun.

Using API from [wetherstack API](https://weatherstack.com/) (free)

##### Looks project
[Project](https://youtu.be/CmyIwga2ZGI)
