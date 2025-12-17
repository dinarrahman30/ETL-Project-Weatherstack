IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[weather_data]') AND type in (N'U'))
BEGIN
    CREATE TABLE weather_data (
        id INT IDENTITY(1,1) PRIMARY KEY,
        city VARCHAR(50),
        temperature FLOAT,
        humidity FLOAT,
        weather_description VARCHAR(100),
        observation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
END