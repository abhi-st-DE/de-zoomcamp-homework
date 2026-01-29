import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import pyarrow.parquet as pq  # Added for handling Parquet files

# Define dtype for the Green Taxi data (same structure as Yellow Taxi)
green_taxi_dtype = {
    "VendorID": "Int64",
    "store_and_fwd_flag": "string",
    "RatecodeID": "Int64",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "payment_type": "Int64",
    "trip_type": "Int64",
    "congestion_surcharge": "float64",
    "cbd_congestion_fee": "float64"
}

# Define dtype for the Taxi Zone Lookup data
taxi_zone_lookup_dtype = {
    "LocationID": "Int64",    # integer
    "Borough": "string",      # text
    "Zone": "string",         # text
    "service_zone": "string"  # text
}

# Define parse dates for Green Taxi data
green_taxi_parse_dates = [
    "lpep_pickup_datetime",  # Green Taxi pickup datetime
    "lpep_dropoff_datetime"  # Green Taxi dropoff datetime
]

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--year', default=2025, type=int, help='Year of the data')
@click.option('--month', default=11, type=int, help='Month of the data')
@click.option('--green-target-table', default='green_taxi_data', help='Target table name for Green taxi data')
@click.option('--taxi-zone-table', default='taxi_zone_lookup', help='Target table name for taxi zone lookup data')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for reading data')

def run(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, green_target_table, taxi_zone_table, chunksize):
    # Define prefix URL for Green Taxi data
    green_taxi_prefix = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
    green_taxi_url = f'{green_taxi_prefix}/green_tripdata_{year}-{month:02d}.parquet'

    taxi_zone_lookup_url = 'https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv'

    # Create a PostgreSQL engine
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    # Ingest taxi zone lookup data
    print("Ingesting taxi zone lookup data...")
    taxi_zone_df_iter = pd.read_csv(taxi_zone_lookup_url,
				dtype=taxi_zone_lookup_dtype,
				iterator=True,
				chunksize=chunksize)

    first = True
    for df_chunk in tqdm(taxi_zone_df_iter):
        if first:
            df_chunk.head(0).to_sql(name=taxi_zone_table,
				con=engine,
				if_exists='replace')
            first = False
        df_chunk.to_sql(name=taxi_zone_table,
			con=engine,
			if_exists='append')
    print(f"Taxi zone lookup data ingested into table: {taxi_zone_table}")

    # Ingest Green Taxi data
    print("Ingesting Green taxi data...")
    green_df_iter = pd.read_parquet(green_taxi_url,
				dtype=green_taxi_dtype,
				parse_dates=green_taxi_parse_dates,
				iterator=True,
				chunksize=chunksize)

    first = True
    for df_chunk in tqdm(green_df_iter):
        if first:
            df_chunk.head(0).to_sql(name=green_target_table,
				con=engine,
				if_exists='replace')
            first = False
        df_chunk.to_sql(name=green_target_table,
			con=engine,
			if_exists='append')
    print(f"Green taxi data ingested into table: {green_target_table}")

if __name__ == '__main__':
    run()
