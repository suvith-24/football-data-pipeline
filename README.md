# Football Data Engineering Pipeline & Analytics Dashboard

## Project Overview

This project is an **end-to-end football analytics data pipeline** that extracts raw football match appearance data, processes it through a structured **ETL pipeline**, loads it into a **PostgreSQL data warehouse**, and visualizes club performance using an interactive **Streamlit dashboard**.

The system is designed to simulate a **real-world data engineering workflow**, incorporating object storage, data transformation, quality validation, and analytical visualization.

The pipeline processes over **1.7 million player appearance records**, transforms them into a **star schema warehouse**, and enables users to analyze club performance metrics through multiple graphical views.

---

# Architecture

The project follows a modern **data engineering architecture**:

```
Raw CSV Data
      │
      ▼
MinIO Object Storage
      │
      ▼
Python ETL Pipeline
 (Extract → Transform → Quality Checks → Load)
      │
      ▼
PostgreSQL Data Warehouse
      │
      ▼
Streamlit Analytics Dashboard
```

### Components

| Component               | Purpose                                                         |
| ----------------------- | --------------------------------------------------------------- |
| **MinIO**               | Stores raw football datasets (object storage similar to AWS S3) |
| **Python ETL Pipeline** | Extracts, cleans, transforms and loads data                     |
| **PostgreSQL**          | Stores structured analytical data in a star schema              |
| **Streamlit**           | Web dashboard for club performance analytics                    |
| **Docker**              | Runs PostgreSQL and MinIO containers                            |

---

# Dataset

The project processes two datasets:

### 1. Player Appearances

Contains player match statistics.

Key fields:

* appearance_id
* player_id
* player_club_id
* game_id
* competition_id
* goals
* assists
* yellow_cards
* red_cards
* minutes_played
* date

Total records: **~1.7 million**

---

### 2. Clubs

Contains club information.

Key fields:

* club_id
* club name
* competition_id

Total records: **451 clubs**

---

# Data Warehouse Design

The warehouse follows a **Star Schema** optimized for analytics.

## Fact Table

### `fact_player_appearances`

Stores player match statistics.

| Column                   | Description                       |
| ------------------------ | --------------------------------- |
| appearance_id            | Unique appearance record          |
| player_id                | Player identifier                 |
| club_id                  | Club identifier                   |
| competition_id           | Competition identifier            |
| date_id                  | Match date                        |
| goals                    | Goals scored                      |
| assists                  | Assists                           |
| yellow_cards             | Yellow cards                      |
| red_cards                | Red cards                         |
| minutes_played           | Minutes played                    |
| goal_contribution        | goals + assists                   |
| goals_per_90             | Goals normalized per 90 minutes   |
| assists_per_90           | Assists normalized per 90 minutes |
| goal_contribution_per_90 | Total contribution per 90 minutes |

---

## Dimension Tables

### `dim_club`

| Column         | Description     |
| -------------- | --------------- |
| club_id        | Club identifier |
| club_name      | Name of club    |
| competition_id | Competition     |

---

### `dim_date`

| Column  | Description |
| ------- | ----------- |
| date_id | Date        |
| year    | Year        |
| month   | Month       |
| day     | Day         |

---

### `dim_competition`

| Column         | Description            |
| -------------- | ---------------------- |
| competition_id | Competition identifier |

---

# ETL Pipeline

The pipeline consists of four major stages.

---

## 1. Extract

Raw CSV files are stored in **MinIO object storage**.

The pipeline connects to MinIO and downloads:

* appearances.csv
* clubs.csv

Technologies used:

* MinIO Python SDK
* Pandas

---

## 2. Transform

Data transformation includes:

* Cleaning invalid records
* Handling missing values
* Removing duplicates
* Feature engineering
* Joining datasets

New analytical features created:

* goal_contribution
* goals_per_90
* assists_per_90
* goal_contribution_per_90

---

## 3. Data Quality Checks

The pipeline validates:

* No null player IDs
* Valid minutes played
* Successful club joins
* Data consistency

If a validation fails, the pipeline stops to prevent bad data entering the warehouse.

---

## 4. Load

The cleaned dataset is loaded into PostgreSQL.

Loading method:

* Bulk loading using **PostgreSQL COPY command**
* Incremental loading based on `appearance_id`

Tables loaded:

* dim_club
* dim_date
* dim_competition
* fact_player_appearances

---

# Dashboard Features

The Streamlit dashboard allows users to explore club performance.

### Features

Users can:

* Select clubs
* View performance statistics
* Analyze match contributions
* Compare metrics across competitions

### Visualizations

The dashboard displays:

* Goals per club
* Assists per club
* Minutes played
* Goal contribution trends
* Performance metrics per 90 minutes

Charts are interactive and update dynamically based on the selected club.

---

# Project Structure

```
football-data-pipeline
│
├── docker
│   └── docker-compose.yml
│
├── pipeline
│   ├── extract.py
│   ├── transform.py
│   ├── quality_checks.py
│   ├── load.py
│   └── main_pipeline.py
│
├── Sql
│   └── create_tables.sql
│
├── web_dashboard
│   └── app.py
│
├── logs
│   └── pipeline.log
│
├── requirements.txt
└── README.md
```

---

# How to Run the Project

## 1. Clone the repository

```
git clone <repository-url>
cd football-data-pipeline
```

---

# 2. Create Virtual Environment

```
python -m venv venv
```

Activate it:

### Windows

```
venv\Scripts\activate
```

---

# 3. Install Dependencies

```
pip install -r requirements.txt
```

Key libraries used:

* pandas
* sqlalchemy
* psycopg2
* minio
* streamlit

---

# 4. Start Docker Containers

Navigate to the docker folder.

```
cd docker
docker-compose up -d
```

This starts:

* PostgreSQL database
* MinIO object storage

Check containers:

```
docker ps
```

---

# 5. Create Data Warehouse Tables

Connect to PostgreSQL:

```
psql -h localhost -p 5433 -U postgres -d football_dw
```

Run:

```
\i ../Sql/create_tables.sql
```

This creates the warehouse schema.

---

# 6. Upload Raw Data to MinIO

Open the MinIO interface:

```
http://localhost:9001
```

Login credentials:

```
username: admin
password: admin123
```

Create a bucket:

```
raw-data
```

Upload:

* appearances.csv
* clubs.csv

---

# 7. Run the Data Pipeline

From the project root:

```
python pipeline/main_pipeline.py
```

The pipeline will:

1. Extract data from MinIO
2. Transform and clean the data
3. Run data quality checks
4. Load the data into PostgreSQL

Expected output:

```
Pipeline completed successfully
```

---

# 8. Run the Dashboard

Start the Streamlit application:

```
streamlit run web_dashboard/app.py
```

Open the dashboard in your browser:

```
http://localhost:8501
```

---

# Example Workflow

1. Upload raw football data to MinIO
2. Run the ETL pipeline
3. Load structured data into PostgreSQL
4. Launch the dashboard
5. Explore club performance analytics

---

# Technologies Used

* **Python**
* **Pandas**
* **PostgreSQL**
* **MinIO**
* **Docker**
* **Streamlit**
* **SQLAlchemy**

---

# Future Improvements

Possible enhancements include:

* Player performance dashboards
* Competition comparison analytics
* Automated pipeline scheduling
* Airflow orchestration
* Advanced statistical models
* Real-time data ingestion

---

# Conclusion

This project demonstrates the full lifecycle of a **data engineering pipeline**, from raw data ingestion to analytical visualization. It showcases best practices such as structured ETL workflows, data validation, scalable storage, and interactive dashboards for sports analytics.
