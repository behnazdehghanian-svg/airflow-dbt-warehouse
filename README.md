

# Online Retail Analytics Pipeline

End-to-end batch data pipeline for an online retail store using Airflow, dbt, and BigQuery.

## Business Goal
Analyze daily sales data to answer key business questions:
- Which customers spend the most?
- Which products sell the most?
- What are the best sales days?

## Architecture
```
generate_data.py → ingest_to_bigquery.py → dbt models → BigQuery → Looker Studio
```
Orchestrated by Apache Airflow running daily.

## Tech Stack
- **Python** — data generation and ingestion
- **Apache Airflow** — pipeline orchestration
- **dbt** — data transformation
- **BigQuery** — data warehouse
- **Looker Studio** — dashboard and visualization
- **Docker** — local Airflow setup

## Data Model
### Raw Tables (BigQuery)
- `raw_customers` — 100 customers with name, email, city, country
- `raw_products` — 10 products with name, category, price
- `raw_orders` — daily orders with quantity and total amount

### Staging (dbt views)
- `staging_customers` — cleaned customer data
- `staging_products` — cleaned product data
- `staging_orders` — cleaned order data

### Marts (dbt tables)
- `dim_customers` — customer profiles with total orders and spend
- `fact_sales` — complete sales transactions

## Pipeline Flow
1. `generate_data.py` — generates 50 new orders for today
2. `ingest_to_bigquery.py` — loads CSV files to BigQuery
3. dbt staging models — clean raw data
4. dbt mart models — build analytics tables
5. dbt tests — validate data quality

## How to Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/behnazdehghanian-svg/airflow-dbt-warehouse.git
cd airflow-dbt-warehouse
```

### 2. Set up credentials
- Create a GCP service account with BigQuery Admin role
- Download the JSON key file to `keys/` folder

### 3. Start Airflow
```bash
docker-compose up airflow-init
docker-compose up airflow-webserver airflow-scheduler
```

### 4. Open Airflow UI
- Go to http://localhost:8081
- Username: admin / Password: admin
- Trigger `ingest_transform_dag`

### 5. Run dbt manually (optional)
```bash
cd dbt
dbt run
dbt test
```

## Dashboard
View the Looker Studio dashboard: [Online Retail Analytics Dashboard](#)

## Project Structure
```
airflow-dbt-warehouse/
├── airflow/dags/          # Airflow DAG
├── dbt/models/
│   ├── staging/           # Raw data cleaning
│   └── marts/             # Analytics tables
├── scripts/
│   ├── generate_data.py   # Data generator
│   └── ingest_to_bigquery.py  # BigQuery loader
├── keys/                  # GCP credentials (not in git)
├── data/                  # CSV files (not in git)
└── docker-compose.yml     # Airflow setup
```
