from google.cloud import bigquery
import pandas as pd
import os
from datetime import datetime

KEY_PATH = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "keys/behnaz-data-engineer-portfolio-553f4e1cc4b4.json")
PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "behnaz-data-engineer-portfolio")
DATASET_ID = "retail_analytics"
today = datetime.today().strftime("%Y-%m-%d")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_PATH
client = bigquery.Client(project=PROJECT_ID)

def create_dataset():
    dataset_id = f"{PROJECT_ID}.{DATASET_ID}"
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "US"
    client.create_dataset(dataset, exists_ok=True)
    print(f"✅ Dataset {DATASET_ID} ready")

def merge_table(csv_file, table_name, unique_key):
    df = pd.read_csv(csv_file)
    temp_table = f"{PROJECT_ID}.{DATASET_ID}.temp_{table_name}"
    
    # Load to temp table
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )
    job = client.load_table_from_dataframe(df, temp_table, job_config=job_config)
    job.result()
    print(f"✅ Loaded {len(df)} rows into temp_{table_name}")

    # Build column list from dataframe
    columns = df.columns.tolist()
    update_set = ", ".join([f"T.{col} = S.{col}" for col in columns if col != unique_key])
    insert_cols = ", ".join(columns)
    insert_vals = ", ".join([f"S.{col}" for col in columns])

    # MERGE into target table
    merge_query = f"""
        MERGE `{PROJECT_ID}.{DATASET_ID}.{table_name}` T
        USING `{PROJECT_ID}.{DATASET_ID}.temp_{table_name}` S
        ON T.{unique_key} = S.{unique_key}
        WHEN MATCHED THEN
            UPDATE SET {update_set}
        WHEN NOT MATCHED THEN
            INSERT ({insert_cols})
            VALUES ({insert_vals})
    """
    client.query(merge_query).result()
    print(f"✅ Merged {len(df)} rows into {table_name}")

    # Delete temp table
    client.delete_table(temp_table, not_found_ok=True)
    print(f"✅ Deleted temp_{table_name}")

if __name__ == "__main__":
    print("Starting ingestion to BigQuery...")
    create_dataset()
    merge_table("data/customers.csv", "raw_customers", "customer_id")
    merge_table("data/products.csv", "raw_products", "product_id")
    merge_table(f"data/orders_{today}.csv", "raw_orders", "order_id")
    print("✅ Ingestion complete!")