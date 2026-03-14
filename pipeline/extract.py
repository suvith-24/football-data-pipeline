from minio import Minio
import pandas as pd
from io import BytesIO
import logging
import os

# Configure Logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(BASE_DIR, "logs", "pipeline.log")

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def connect_minio():
    client = Minio(
        "localhost:9000",
        access_key="admin",
        secret_key="admin123",
        secure=False
    )
    logging.info("Connected to MinIO")
    return client

def extract_csv_from_minio(client, bucket_name, file_name):
    try:
        logging.info(f"Extracting {file_name} from {bucket_name}")
        response = client.get_object(bucket_name, file_name)
        data = response.read()
        df = pd.read_csv(BytesIO(data))
        logging.info(f"{file_name} loaded successfully with {len(df)} rows")
        return df
    except Exception as e:
        logging.error(f"Error extracting {file_name}: {str(e)}")
        raise

def extract_data():
    client = connect_minio()
    appearances_df = extract_csv_from_minio(client, "raw-data", "appearances.csv")
    clubs_df = extract_csv_from_minio(client, "raw-data", "clubs.csv")
    return appearances_df, clubs_df
