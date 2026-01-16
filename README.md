# medical-telegram-warehouse
End-to-end data pipeline for Telegram medical data in Ethiopia
## Task 2 – Data Modeling & Transformation

### Architecture
This project follows a modern ELT architecture:
- Raw Telegram data is loaded into PostgreSQL (`raw` schema)
- Transformations are performed using dbt
- Clean analytical tables are built in the `analytics` schema

### Star Schema Design
- **Fact Table**: `fct_messages`
  - Grain: one row per Telegram message
- **Dimensions**:
  - `dim_channels`: Telegram channel metadata
  - `dim_dates`: Calendar attributes for time analysis

### Data Quality
dbt tests enforce:
- Primary key uniqueness
- Non-null constraints
- Referential integrity
- Business rules (no future dates, non-negative views)
# Medical Telegram Data Warehouse

An end-to-end ELT data pipeline that scrapes Ethiopian medical Telegram channels,
stores raw data in a data lake, transforms it using dbt, and exposes insights
via an analytical API.
