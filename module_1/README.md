# Data Engg Zoomcamp – Homework – Module 1 : Docker, SQL, Terraform

## Prerequisites

- Docker (for running PostgreSQL and pgAdmin)
- Python 3.13 recommended
- Terminal and browser (GitHub Codespaces or local setup both work)

---

## Installation

1. You do not need to clone the full Zoomcamp repository for this module.
2. Install Docker (not required if using Codespaces).
3. Make sure Python is installed on your system (install 3.13 for testing if needed).

---

## Running the Project

### 1) Set up the virtual environment

Create a working directory and move into it:

```bash
mkdir pipeline
cd pipeline


Check Python:

python --version


Install uv:

pip install uv


Initialize the project and virtual environment:

uv init --python 3.13


Verify Python inside the virtual environment:

uv run python -V

2) Install dependencies

Run these commands in the same folder as pyproject.toml:

uv add pandas
uv add pyarrow
uv add sqlalchemy
uv add tqdm
uv add click
uv add psycopg2-binary

3) Select the virtual environment interpreter (VS Code / Codespaces)

Press F1

Select Python: Select Interpreter

Choose Enter interpreter path

Click Find

Navigate to:

.venv/bin/python


Select that Python.

4) Copy required files

Copy the following files from module_1/code into your working directory:

ingest_data.py

Dockerfile

docker-compose.yaml

docker_ingestion.txt

5) Build the Docker image

Make sure you are in the project directory:

docker build -t taxi_ingest:v001 .

6) Start PostgreSQL and pgAdmin
docker compose up


To run in detached mode:

docker compose up -d


If your Docker version is older:

docker-compose up

7) Open a new terminal (if running detached)

Either continue in the same terminal or open a new terminal tab.

8) Check Docker network
docker network ls


Docker automatically creates a network named:

<folder_name>_default


Example:

pipeline_default


Note this name.

9) Run data ingestion

Open docker_ingestion.txt.

Update the network name if needed, then run the command:

docker run -it --rm \
  --network=pipeline_default \
  taxi_ingest:v001 \
    --pg-user=postgres \
    --pg-pass=postgres \
    --pg-host=db \
    --pg-port=5432 \
    --pg-db=ny_taxi


This will ingest:

Taxi zone lookup CSV

Green taxi Parquet data

into PostgreSQL.

Access pgAdmin

Open in browser:

http://localhost:8080


Login credentials (from docker-compose):

Email: pgadmin@pgadmin.com

Password: pgadmin

Cleanup (optional)

After finishing:

docker compose down
docker system prune


This stops containers and removes unused Docker resources.
