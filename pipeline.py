from dagster import op, job

@op
def scrape_telegram_data():
    print("Scraping Telegram data...")

@op
def load_raw_to_postgres():
    print("Loading raw data into Postgres...")

@op
def run_dbt_transformations():
    print("Running dbt transformations...")

@op
def run_yolo_enrichment():
    print("Running YOLO enrichment...")

@job
def medical_pipeline():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()
