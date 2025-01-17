#!/bin/bash


# S3 BUCKETS

# CREATE DATALAKE BUCKET

aws s3 mb s3://"$DATALAKE_BUCKET" --region "$REGION"
echo "S3 Bucket "$DATALAKE_BUCKET" created in region $REGION"

# CREATE GRAPH BUCKET

aws s3 mb s3://"$GRAPH_BUCKET" --region "$REGION"
echo "S3 Bucket "$GRAPH_BUCKET" created in region $REGION"
