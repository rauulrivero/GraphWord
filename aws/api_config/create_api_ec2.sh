#!/bin/bash

# Define la región
REGION="us-east-1"


# CREATE API EC2

# Crear a key pair
aws ec2 create-key-pair --key-name my-api-ec2-key --query "KeyMaterial" --output text --region "$REGION" > my-api-ec2-key.pem
chmod 400 my-api-ec2-key.pem

# Create Security Group for API
SECURITY_GROUP_API=$(aws ec2 create-security-group --group-name api-sg --description "API Security Group" --vpc-id "$VPC_ID" --query "GroupId" --output text --region "$REGION")
aws ec2 authorize-security-group-ingress --group-id "$SECURITY_GROUP_API" --protocol tcp --port 5000 --source-group "$SECURITY_GROUP_GUI" --region "$REGION"
aws ec2 authorize-security-group-ingress --group-id "$SECURITY_GROUP_API" --protocol tcp --port 22 --source-group "$SECURITY_GROUP_GUI" --region "$REGION"
echo "Security Group API creado: $SECURITY_GROUP_API"

# Launch EC2 instance for API in the private subnet
INSTANCE_API=$(aws ec2 run-instances --image-id ami-01816d07b1128cd2d --instance-type t2.micro --key-name my-api-ec2-key --security-group-ids "$SECURITY_GROUP_API" --subnet-id "$SUBNET_PRIVATE" --query "Instances[0].InstanceId" --output text --region "$REGION")
echo "Instancia API lanzada: $INSTANCE_API"
