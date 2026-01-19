from dagster import op, job, schedule

@op
def scrape_telegram_data(context):
    context.log.info("Scraping Telegram data")

@op
def load_raw_to_postgres(context):
    context.log.info("Loading raw data into Postgres")

@op
def run_dbt_transformations(context):
    context.log.info("Running dbt transformations")

@op
def run_yolo_enrichment(context):
    context.log.info("Running YOLO enrichment")

@job
def medical_pipeline():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()

@schedule(
    cron_schedule="0 2 * * *",
    job=medical_pipeline,
    execution_timezone="Africa/Addis_Ababa"
)
def daily_medical_pipeline():
    return {}
