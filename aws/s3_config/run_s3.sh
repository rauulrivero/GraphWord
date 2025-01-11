#!/bin/bash


aws s3 mb s3://books-datalake --region us-east-1

echo "Bucket S3 books-datalake creado en la región us-east-1"

aws s3 mb s3://books-graph --region us-east-1

echo "Bucket S3 books-graph creado en la región us-east-1"
