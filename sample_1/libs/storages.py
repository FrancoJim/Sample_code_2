import logging
from pathlib import Path
import os

import boto3

logging.basicConfig(level=logging.INFO)


def create_s3_bucket(bucket):
    """
    Create an S3 bucket
    :param bucket: S3 bucket name
    """

    s3 = boto3.resource("s3")
    if s3.Bucket(bucket) in s3.buckets.all():
        logging.info(f"Bucket {bucket} already exists")
        return

    s3.create_bucket(Bucket=bucket)
    logging.info(f"Bucket {bucket} created")


def list_s3_buckets():
    """
    List all S3 buckets
    :return: List of all S3 buckets
    """
    s3 = boto3.client("s3")
    response = s3.list_buckets()
    buckets = [bucket["Name"] for bucket in response["Buckets"]]
    return buckets


def list_s3_files(bucket, prefix):
    """
    List files in S3 bucket with the specified prefix
    :param bucket: S3 bucket name
    :param prefix: Prefix of the files to list
    :return: List of files in the S3 bucket with the specified prefix
    """
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    files = [content["Key"] for content in response["Contents"]]
    return files


def copy_from_s3(bucket, prefix, local_dir):
    """
    Copy files from S3 bucket to local directory
    :param bucket: S3 bucket name
    :param prefix: Prefix of the files to copy
    :param local_dir: Local directory to copy files to
    """
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket)
    for obj in bucket.objects.filter(Prefix=prefix):
        key = obj.key
        local_file = local_dir + key
        bucket.download_file(key, local_file)
        logging.info(f"File {key} downloaded to {local_file}")


def copy_to_s3(bucket, prefix, local_dir):
    """
    Copy files from local directory to S3 bucket
    :param bucket: S3 bucket name
    :param prefix: Prefix of the files to copy
    :param local_dir: Local directory to copy files from
    """

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket)
    for path in Path(local_dir).rglob("*"):
        if path.is_file():
            key = prefix + path.name
            bucket.upload_file(str(path), key)
            logging.info(f"File {path} uploaded to {bucket}/{key}")


def delete_bucket_and_contents(bucket):
    """
    Delete an S3 bucket and all of its contents
    :param bucket: S3 bucket name
    """

    s3 = boto3.resource("s3")

    if s3.Bucket(bucket) not in s3.buckets.all():
        logging.info(f"Bucket {bucket} does not exist")
        return

    bucket = s3.Bucket(bucket)
    bucket.objects.all().delete()
    bucket.delete()
    logging.info(f"Bucket {bucket} deleted")
