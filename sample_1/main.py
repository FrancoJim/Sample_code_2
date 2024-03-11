import logging
import os
from pprint import pprint
from datetime import datetime as dt

from .libs.storages import (
    copy_to_s3,
    list_s3_files,
    create_s3_bucket,
    list_s3_buckets,
    delete_bucket_and_contents,
)
from .libs.utils import BEA_Wrapper

from botocore.exceptions import NoCredentialsError

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def main(
    s3_bucket: str, file_name: str = "gdp_by_industry", dest_path: str = "/tmp"
) -> None:

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
        # Only for Dev purposes
        # delete_bucket_and_contents(bucket=s3_bucket)
        # exit(0)

        create_s3_bucket(bucket=s3_bucket)
        logging.info(list_s3_buckets())
        copy_to_s3(bucket=s3_bucket, prefix="/", local_dir=dest_path)
        list_s3_files(bucket=s3_bucket, prefix="/")
    except NoCredentialsError as e:
        logging.error(e)
        # raise e
    except Exception as e:
        logging.error(e)
        # raise e


if __name__ == "__main__":
    main(s3_bucket="sample-sized-bucket-2", dest_path="./data")
