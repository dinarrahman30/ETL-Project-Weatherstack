import psycopg2
import time
import sys
import os

# --- IMPORT PINTAR (ANTI ERROR) ---
# Trik ini agar bisa jalan baik di VS Code (lokal) maupun Airflow (container)
try:
    from api_requests.api_request import fetch_weather_data
except ImportError:
    from api_request import fetch_weather_data

# Daftar Kota Target
CITIES = ["Jakarta", "Bandung", "Surabaya", "London", "New York", "Tokyo", "Paris", "Singapore"]

# --- FUNGSI DATABASE ---
def connect_to_db():
    print("🔌 Menghubungkan ke database...")
    db_config = {"dbname": "airflow", "user": "airflow", "password": "airflow", "port": "5432"}
    
    try:
        # Coba Internal (Docker)
        return psycopg2.connect(**db_config, host="postgres")
    except psycopg2.OperationalError:
        try:
            # Coba Eksternal (Localhost Laptop)
            print("⚠️ Host 'postgres' gagal. Mencoba 'localhost'...")
            return psycopg2.connect(**db_config, host="localhost")
        except Exception as e:
            print(f"❌ Gagal connect database: {e}")
            raise

def create_table(conn):
    # Pastikan tabel punya constraint UNIQUE agar tidak duplikat
    query = """
    CREATE TABLE IF NOT EXISTS weather_data (
        id SERIAL PRIMARY KEY,
        city TEXT,
        temperature FLOAT,
        weather_description TEXT,
        wind_speed FLOAT,
        time TIMESTAMP,
        inserted_at TIMESTAMP DEFAULT Now(),
        utc_offset TEXT,
        UNIQUE(city, time)
    );
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
    except Exception as e:
        print(f"Error create table: {e}")

def insert_one_record(conn, data):
    # Validasi data
    if not data or not isinstance(data, dict) or 'error' in data:
        print("❌ Data tidak valid/kosong.")
        return

    query = """
    INSERT INTO weather_data (city, temperature, weather_description, wind_speed, time, utc_offset)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (city, time) DO NOTHING;
    """
    try:
        cursor = conn.cursor()
        
        # Parsing (Mengambil nilai dari JSON)
        city = data['location']['name']
        temp = data['current']['temperature']
        desc = data['current']['weather_descriptions'][0] if data['current']['weather_descriptions'] else "Unknown"
        wind = data['current']['wind_speed']
        time_local = data['location']['localtime']
        utc_off = data['location']['utc_offset']

        cursor.execute(query, (city, temp, desc, wind, time_local, utc_off))
        conn.commit()
        cursor.close()
        print(f"💾 Berhasil simpan: {city} | Suhu: {temp}°C")
        
    except Exception as e:
        print(f"❌ Gagal Insert {city}: {e}")
        conn.rollback()

# --- MAIN LOOP ---
def main():
    conn = None
    try:
        conn = connect_to_db()
        create_table(conn)
        
        print("\n--- MULAI PROSES ETL ---")
        for city in CITIES:
            # 1. Panggil fungsi dari file sebelah
            data_json = fetch_weather_data(city)
            
            # 2. Masukkan ke DB
            insert_one_record(conn, data_json)
            
            # 3. Jeda
            time.sleep(0.5)
            
        print("\n🎉 Selesai semua kota!")

    except Exception as e:
        print(f"Error Utama: {e}")
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    main()