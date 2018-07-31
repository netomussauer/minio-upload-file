#!/usr/bin/env python

"""
Written by Neto Mussauer
Github: https://github.com/netomussauer
Email: netomussauer@gmail.com
This script create a Minio bucket and upload some file to Minio S3 storage.
"""

from minio import Minio
from minio.error import *
import getpass
import os


def minio_client(minio_url, minio_access, minio_secret):
  minioClient = Minio(minio_url, access_key=minio_access, secret_key=minio_secret, secure=True)
  return minioClient


def create_bucket(minio_client, bucket_name):
  try:
    minio_client.make_bucket(bucket_name, location='us-east-1')
  except BucketAlreadyOwnedByYou as err:
    print(err.message)


def file_upload(minio_client, bucket_name, file_path):
  try:
    with open(file_path,'rb') as file_data:
      file_stat = os.stat(file_path)
      print(minio_client.put_object(bucket_name, os.path.basename(file_path), file_data, file_stat.st_size))
      print('File upload sucessfully!')
  except ResponseError as err:
    print(err)


def main():
  url = input('Enter Minio URL: ') 
  access = input('Enter Minio Access Key: ')
  key = getpass.getpass('Enter Minio Password: ')
  bucket = input('Enter Bucket Name: ')
  miniocli = minio_client(url, access, key)
  create_bucket(miniocli, bucket)
  file_path = input('Enter File Path: ')
  file_upload(miniocli, bucket, file_path)


if __name__ == '__main__':
  main()