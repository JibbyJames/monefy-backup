import sqlite3
import pandas as pd
from IPython.display import display, HTML

# Connect to the SQLite database
conn = sqlite3.connect('monefy_backup_decrypted.db')

# Read the SQL query from a file
with open('MyQuery.sql', 'r') as f:
    query = f.read()

# Execute the SQL query and convert the result to a DataFrame
df = pd.read_sql_query(query, conn)

# Print the df as a string to the console
#df["formatted_datetime"] = pd.to_datetime(df["createdOn"], unit='ms')
print(df)

csv_file_path = 'query_output.csv'
df.to_csv(csv_file_path, index=False)