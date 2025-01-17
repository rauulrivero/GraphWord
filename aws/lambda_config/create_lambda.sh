#!/bin/bash

# LAMBDA FUNCTIONS

# CREATE LAMBDA FUNCTION (CRAWLER)


LAMBDA_ROLE=$(aws iam get-role --role-name lambda-run-role --query "Role.Arn" --output text)

aws lambda create-function --function-name CrawlerLambdaFunction --runtime python3.10 --role "$LAMBDA_ROLE" --handler lambda_function.lambda_handler --zip-file fileb://../crawler/deployment.zip --timeout 15 --memory-size 128
echo "Lambda Function CrawlerLambdaFunction created"

# CREATE LAMBDA FUNCTION (GRAPH)

aws lambda create-function --function-name GraphLambdaFunction --runtime python3.10 --role "$LAMBDA_ROLE" --handler lambda_function.lambda_handler --zip-file fileb://../graphify/deployment.zip --timeout 15 --memory-size 128
echo "Lambda Function GraphLambdaFunction created"



echo "Infrastructure successfully configured."