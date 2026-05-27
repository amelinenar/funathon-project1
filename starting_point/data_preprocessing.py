import duckdb
import pandas as pd

# con = duckdb.connect()
# con.sql("SELECT 42 AS x").show()

trans = pd.read_parquet("https://minio.lab.sspcloud.fr/projet-funathon/2026/project1/data/1_input/transactions_EN.parquet")
trans.shape