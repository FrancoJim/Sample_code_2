import logging
import os
from pprint import pprint
from datetime import datetime as dt
from time import sleep

from sample_2.libs.storages import AwsS3
from sample_2.libs.utils import BEA_Wrapper

from botocore.exceptions import NoCredentialsError

# Remove all handlers associated with the root logger.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Reconfigure logging with the desired settings and format.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
)


def main(
    s3_bucket: str,
    file_name: str = "gdp_by_industry",
    dest_path: str = "/tmp",
    delete_bucket: bool = False,
) -> None:

    if delete_bucket:
        AwsS3.delete_bucket_and_contents(bucket=s3_bucket)
        logging.info(f"Deleted bucket {s3_bucket}")
        exit(0)

    try:
        bea = BEA_Wrapper(api_key=os.environ["BEA_API_KEY"])
        df = bea.list_datasets()
        # df = bea.fetch_gdp_by_industry(year="2023")
    except Exception as e:
        logging.error(e)
        # raise e

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    # Create string of the current date and time via number of seconds since epoch
    now = dt.now().strftime("%Y%m%d%H%M%S")

    df.to_pickle(f"{dest_path}/{now}.{file_name}.pkl")
    df.to_csv(f"{dest_path}/{now}.{file_name}.csv")

    try:
        AwsS3.create_bucket(bucket=s3_bucket)
        logging.info(AwsS3.list_buckets())
        AwsS3.copy_to_bucket(bucket=s3_bucket, prefix="/", local_dir=dest_path)
        logging.info(f"Files uploaded to {s3_bucket}.")
        logging.info(
            f"Files in {s3_bucket}: {AwsS3.list_bucket_files(bucket=s3_bucket, prefix='/')}"
        )

    except NoCredentialsError as e:
        logging.error(e)
        # raise e
    except Exception as e:
        logging.error(e)
        # raise e


if __name__ == "__main__":
    s3_bucket_name = "sample-sized-bucket-1"
    main(s3_bucket=s3_bucket_name, dest_path="./data")
    sleep(20)
    main(s3_bucket=s3_bucket_name, delete_bucket=True)
