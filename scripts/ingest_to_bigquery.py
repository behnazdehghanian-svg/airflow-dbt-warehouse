from google.cloud import bigquery
import pandas as pd
import os
from datetime import datetime  # ADD THIS LINE

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

def delete_todays_orders():
    query = f"""
        DELETE FROM `{PROJECT_ID}.{DATASET_ID}.raw_orders`
        WHERE order_date = '{today}'
    """
    client.query(query).result()
    print(f"✅ Deleted today's existing orders for {today}")    

def load_csv_to_bigquery(csv_file, table_name):
    df = pd.read_csv(csv_file)
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
        if table_name != "raw_orders"
        else bigquery.WriteDisposition.WRITE_APPEND
    )
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
    print(f"✅ Loaded {len(df)} rows into {table_name}")

if __name__ == "__main__":
    print("Starting ingestion to BigQuery...")
    create_dataset()
    load_csv_to_bigquery(f"data/orders_{today}.csv", "raw_orders")
    load_csv_to_bigquery("data/customers.csv", "raw_customers")
    load_csv_to_bigquery("data/products.csv", "raw_products")
    print("✅ Ingestion complete!")