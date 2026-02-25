##############################################################################
# glue/jobs/example_etl.py
#
# Example AWS Glue ETL job — reads from S3 raw zone, transforms, writes to
# processed zone in the data lake.
#
# This script is synced to:
#   s3://de1-{env}-glue-scripts/jobs/example_etl.py
# and referenced by the Glue Job created in de1-infrastructure.
##############################################################################

import sys
import logging
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# ── Job arguments ─────────────────────────────────────────────────────────────
args = getResolvedOptions(sys.argv, [
    "JOB_NAME",
    "environment",
])

environment = args["environment"]

# ── Logging ───────────────────────────────────────────────────────────────────
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ── Glue context setup ────────────────────────────────────────────────────────
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# ── S3 paths (per environment) ────────────────────────────────────────────────
DATA_LAKE_BUCKET = f"de1-{environment}-data-lake"
RAW_PATH = f"s3://{DATA_LAKE_BUCKET}/raw/example/"
PROCESSED_PATH = f"s3://{DATA_LAKE_BUCKET}/processed/example/"

logger.info(f"Starting ETL | env={environment} | source={RAW_PATH}")

# ── Read from raw zone ────────────────────────────────────────────────────────
raw_df = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [RAW_PATH]},
    format="json",
)

logger.info(f"Read {raw_df.count()} records from raw zone")

# ── Transform ─────────────────────────────────────────────────────────────────
# Add your transformation logic here
# Example: drop nulls, rename fields, cast types
transformed_df = raw_df.dropNulls()

# ── Write to processed zone ───────────────────────────────────────────────────
glueContext.write_dynamic_frame.from_options(
    frame=transformed_df,
    connection_type="s3",
    connection_options={"path": PROCESSED_PATH},
    format="parquet",
)

logger.info(f"Written to processed zone: {PROCESSED_PATH}")

job.commit()
