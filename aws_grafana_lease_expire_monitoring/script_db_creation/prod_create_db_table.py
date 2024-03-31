# from db_con import db_con
import os
from connection import db_con

# Establishing a connection to MySQL
conn = db_con()
# Creating a cursor object using the cursor() method
cursor = conn.cursor()

db_name = os.getenv('DB_NAME')
db_table_name =  os.getenv('DB_TABLE_NAME')

create_db_query_prod = f"CREATE DATABASE IF NOT EXISTS {db_name}"
create_table_query_prod =f"""
CREATE TABLE IF NOT EXISTS {db_name}.{db_table_name} (
    Name VARCHAR(255),
    Instance_ID VARCHAR(255),
    AWS_ID VARCHAR(255),
    Zone VARCHAR(255),
    Environment VARCHAR(255),
    Type VARCHAR(255),
    Start_Time VARCHAR(255),
    End_Time VARCHAR(255),
    Lease_Duration INT,
    Remaining_Days VARCHAR(255),
    Status VARCHAR(255),
    Expire VARCHAR(255),
    Time_Remaining INT
)
"""

# Execute the query to create the table
cursor.execute(create_db_query_prod)
cursor.execute(create_table_query_prod)

# Committing the changes
conn.commit()

# Closing the cursor and connection
cursor.close()
conn.close()

print(f"database : {db_name} and table : {db_table_name} created")
