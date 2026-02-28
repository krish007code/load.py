# GitHub Event Tracker: Medallion Data Pipeline
This project implements a event-driven data pipeline that ingests and analyzes real-time GitHub repository activity (Stars, Pushes) using a **Medallion Architecture**.

## 🏗️ Technical Stack

* **Orchestration:** [Kestra](https://kestra.io/) — Managed event-driven workflow automation.
* **Storage:** [MinIO](https://min.io/) — High-performance S3-compatible object storage for data lakehouse layers.
* **Processing:** [DuckDB](https://duckdb.org/) — An in-process analytical database for high-speed SQL transformations on Parquet.
* **Environment:** Developed on **Fedora Linux** using **uv** for Python package management and **Docker Compose** for infrastructure.

## 🌊 Pipeline Architecture (Medallion)

The pipeline is designed to ensure data quality and reliability through three distinct layers:

1. **Bronze (Ingestion):** Captures raw GitHub API events as compressed JSONL files in MinIO.
2. **Silver (Curated):** Cleans, flattens, and deduplicates the raw data into structured Parquet format using DuckDB.
3. **Gold (Analytical):** Aggregates repo-level metrics (Total Stars, Pushes, Activity) for business intelligence.
4. **Visualization:** Generates an automated terminal dashboard and Markdown report of the Top 10 repositories.

## 📊 Sample Output

The pipeline successfully identifies top developer tools based on real-time community engagement:

| Repository | ⭐ Stars | 🚀 Pushes | 🔥 Total Activity |
| --- | --- | --- | --- |
| TobikoData/sqlmesh | 39 | 5 | 100 |
| kestra-io/kestra | 6 | 17 | 100 |
| duckdb/duckdb | 13 | 9 | 99 |
| *(Data captured during execution on 2026-02-28)*. |  |  |  |

## 📂 Project Structure

```text
.
├── docker-compose.yml 
├── kestra/             
│   ├── bronze.yaml
│   ├── silver.yaml
│   ├── gold.yaml
│   └── viz.yaml
├── load.py             
├── pyproject.toml      
└── README.md          

```

## 🛠️ How to Run

1. **Start Infrastructure:** `docker-compose up -d`.
2. **Access Kestra:** Open `http://localhost:8080`.
3. **Execute:** Import the YAML files from `/kestra` and execute the `bronze` flow. The rest of the pipeline will trigger automatically upon success.
