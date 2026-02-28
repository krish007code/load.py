import dlt
from dlt.sources.helpers import requests

# Updated with correct repository paths to avoid 404 errors
REPOS_TO_TRACK = {
    "Orchestration": ["kestra-io/kestra", "dagster-io/dagster", "apache/airflow"],
    "Transformation": ["dbt-labs/dbt-core", "TobikoData/sqlmesh"], # Fixed: sqlmesh -> TobikoData
    "Storage": ["duckdb/duckdb", "apache/iceberg"]
}

@dlt.resource(name="repo_stats", write_disposition="replace")
def fetch_repo_stats():
    for category, repos in REPOS_TO_TRACK.items():
        for repo_path in repos:
            url = f"https://api.github.com/repos/{repo_path}"
            response = requests.get(url)
            # This is where the 404 was occurring; TobikoData/sqlmesh will now return 200
            response.raise_for_status()            
            data = response.json()
            data['mds_category'] = category
            yield data

@dlt.resource(name="repo_events", write_disposition="append")
def fetch_repo_events():
    for category, repos in REPOS_TO_TRACK.items():
        for repo_path in repos:
            url = f"https://api.github.com/repos/{repo_path}/events?per_page=100"
            response = requests.get(url)
            response.raise_for_status()
            events = response.json()
            for event in events:
                event['mds_category'] = category
                event['repo_name'] = repo_path
                yield event

if __name__ == "__main__":
    # Initializing the pipeline for the Medallion Bronze Layer
    pipeline = dlt.pipeline(
        pipeline_name='github_data',
        destination='filesystem',  # Points to MinIO via Kestra env vars
        dataset_name='github_raw'
    )

    # Running both resources
    load_info = pipeline.run([fetch_repo_stats, fetch_repo_events])
    print(load_info)