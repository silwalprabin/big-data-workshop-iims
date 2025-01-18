from pyflink.table import EnvironmentSettings, TableEnvironment
from pyflink.table.expressions import col
from datetime import datetime

# Set up the TableEnvironment for streaming mode
env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)

# Define a simple in-memory sensor data source
sensor_data = [
    ("sensor-1", 35.5, "2025-01-13T10:00:00Z"),
    ("sensor-2", 36.8, "2025-01-13T10:01:00Z"),
    ("sensor-3", 33.2, "2025-01-13T10:02:00Z"),
    ("sensor-1", 34.9, "2025-01-13T10:03:00Z"),
    ("sensor-2", 37.1, "2025-01-13T10:04:00Z"),
]

# Create a table from the sensor data
source_table = table_env.from_elements(sensor_data, ["sensor_id", "temperature", "timestamp1"])

# Print the input data (sensor data)
print("### Input Sensor Data ###")
source_table.execute().print()

# Example of performing an analysis: Calculate average temperature by sensor
table_env.create_temporary_view("sensor_data", source_table)

# SQL query to compute average temperature by sensor
avg_temp_by_sensor = table_env.sql_query("""
    SELECT sensor_id, AVG(temperature) AS avg_temperature
    FROM sensor_data
    GROUP BY sensor_id
""")

# Print the result of the analysis
print("### Average Temperature by Sensor ###")
avg_temp_by_sensor.execute().print()

# Example of filtering data: Get sensors with temperature greater than 36
filtered_data = table_env.sql_query("""
    SELECT sensor_id, temperature, timestamp1
    FROM sensor_data
    WHERE temperature > 36
""")

# Print filtered data
print("### Sensors with Temperature > 36 ###")
filtered_data.execute().print()
