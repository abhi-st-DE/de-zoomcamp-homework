import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


# CSV schema control is useful → KEEP
taxi_zone_lookup_dtype = {
    "LocationID": "Int64",
    "Borough": "string",
    "Zone": "string",
    "service_zone": "string"
}


@click.command()
@click.option('--pg-user', required=True, help='PostgreSQL user')
@click.option('--pg-pass', required=True, help='PostgreSQL password')
@click.option('--pg-host', required=True, help='PostgreSQL host')
@click.option('--pg-port', required=True, type=int, help='PostgreSQL port')
@click.option('--pg-db', required=True, help='PostgreSQL database')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db):
    engine = create_engine(
        f"postgresql+psycopg2://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
    )

    # -------------------------
    # Taxi Zone Lookup (CSV)
    # -------------------------
    print("Ingesting taxi zone lookup data...")

    taxi_zone_df = pd.read_csv(
        "taxi_zone_lookup.csv",
        dtype=taxi_zone_lookup_dtype
    )

    taxi_zone_df.to_sql(
        name="taxi_zone_lookup",
        con=engine,
        if_exists="replace",
        index=False
    )

    print("Taxi zone lookup data ingested.")

    # -------------------------
    # Green Taxi Data (Parquet)
    # -------------------------
    print("Ingesting Green taxi data...")

    green_df = pd.read_parquet("green_tripdata.parquet")

    chunksize = 100_000

    for i in tqdm(range(0, len(green_df), chunksize)):
        chunk = green_df.iloc[i:i + chunksize]

        chunk.to_sql(
            name="green_taxi_trips",
            con=engine,
            if_exists="append",
            index=False
        )

    print("Green taxi data ingested successfully.")


if __name__ == "__main__":
    run()
