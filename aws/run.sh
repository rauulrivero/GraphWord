#!/bin/bash

# VARIABLES
REGION="us-east-1"
DATALAKE_BUCKET="books-datalake"
GRAPH_BUCKET="books-graph"
AMI_ID="ami-01816d07b1128cd2d"
INSTANCE_TYPE="t2.micro"


# VPC CONFIGURATION

# Crear una VPC
VPC_ID=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query "Vpc.VpcId" --output text --region "$REGION")
aws ec2 modify-vpc-attribute --vpc-id "$VPC_ID" --enable-dns-support --region "$REGION"
aws ec2 modify-vpc-attribute --vpc-id "$VPC_ID" --enable-dns-hostnames --region "$REGION"
echo "VPC creada: $VPC_ID"

# Crear subred pública
SUBNET_PUBLIC=$(aws ec2 create-subnet --vpc-id "$VPC_ID" --cidr-block 10.0.1.0/24 --query "Subnet.SubnetId" --output text --region "$REGION")
aws ec2 modify-subnet-attribute --subnet-id "$SUBNET_PUBLIC" --map-public-ip-on-launch --region "$REGION"
echo "Subred pública creada: $SUBNET_PUBLIC"

# Crear subred privada
SUBNET_PRIVATE=$(aws ec2 create-subnet --vpc-id "$VPC_ID" --cidr-block 10.0.2.0/24 --query "Subnet.SubnetId" --output text --region "$REGION")
echo "Subred privada creada: $SUBNET_PRIVATE"

# Crear un Gateway de Internet
INTERNET_GATEWAY=$(aws ec2 create-internet-gateway --query "InternetGateway.InternetGatewayId" --output text --region "$REGION")
aws ec2 attach-internet-gateway --vpc-id "$VPC_ID" --internet-gateway-id "$INTERNET_GATEWAY" --region "$REGION"
echo "Internet Gateway creado y asociado: $INTERNET_GATEWAY"

# Crear tabla de rutas pública
ROUTE_TABLE_PUBLIC=$(aws ec2 create-route-table --vpc-id "$VPC_ID" --query "RouteTable.RouteTableId" --output text --region "$REGION")
aws ec2 create-route --route-table-id "$ROUTE_TABLE_PUBLIC" --destination-cidr-block 0.0.0.0/0 --gateway-id "$INTERNET_GATEWAY" --region "$REGION"
aws ec2 associate-route-table --route-table-id "$ROUTE_TABLE_PUBLIC" --subnet-id "$SUBNET_PUBLIC" --region "$REGION"
echo "Tabla de rutas pública creada y asociada: $ROUTE_TABLE_PUBLIC"

# Crear NAT Gateway
ALLOC_ID=$(aws ec2 allocate-address --query "AllocationId" --output text --region "$REGION")
NAT_GATEWAY_ID=$(aws ec2 create-nat-gateway --subnet-id "$SUBNET_PUBLIC" --allocation-id "$ALLOC_ID" --query "NatGateway.NatGatewayId" --output text --region "$REGION")
echo "NAT Gateway creado: $NAT_GATEWAY_ID"

aws ec2 wait nat-gateway-available --nat-gateway-ids "$NAT_GATEWAY_ID" --region "$REGION"
echo "NAT Gateway disponible: $NAT_GATEWAY_ID"

# Crear tabla de rutas privada
ROUTE_TABLE_PRIVATE=$(aws ec2 create-route-table --vpc-id "$VPC_ID" --query "RouteTable.RouteTableId" --output text --region "$REGION")
aws ec2 create-route --route-table-id "$ROUTE_TABLE_PRIVATE" --destination-cidr-block 0.0.0.0/0 --nat-gateway-id "$NAT_GATEWAY_ID" --region "$REGION"
aws ec2 associate-route-table --route-table-id "$ROUTE_TABLE_PRIVATE" --subnet-id "$SUBNET_PRIVATE" --region "$REGION"
echo "Tabla de rutas privada creada y asociada: $ROUTE_TABLE_PRIVATE"

echo "VPC configurada correctamente."



# EC2 INSTANCES 

# CREATE GUI EC2

# Crear un key pair
aws ec2 create-key-pair --key-name mi-clave-gui-ec2 --query "KeyMaterial" --output text --region "$REGION" > mi-clave-gui-ec2.pem
chmod 400 mi-clave-gui-ec2.pem

# Crear Security Group para la GUI
SECURITY_GROUP_GUI=$(aws ec2 create-security-group --group-name gui-sg --description "GUI Security Group" --vpc-id "$VPC_ID" --query "GroupId" --output text --region "$REGION")
aws ec2 authorize-security-group-ingress --group-id "$SECURITY_GROUP_GUI" --protocol tcp --port 22 --cidr 0.0.0.0/0 --region "$REGION"
aws ec2 authorize-security-group-ingress --group-id "$SECURITY_GROUP_GUI" --protocol tcp --port 8501 --cidr 0.0.0.0/0 --region "$REGION"
echo "Security Group GUI creado: $SECURITY_GROUP_GUI"

# Lanzar instancia EC2 para la GUI en la subred pública
INSTANCE_GUI=$(aws ec2 run-instances --image-id ami-01816d07b1128cd2d --instance-type t2.micro --key-name mi-clave-gui-ec2 --security-group-ids "$SECURITY_GROUP_GUI" --subnet-id "$SUBNET_PUBLIC" --query "Instances[0].InstanceId" --output text --region "$REGION")
echo "Instancia GUI lanzada: $INSTANCE_GUI"


# CREATE API EC2

# Crear un key pair
aws ec2 create-key-pair --key-name mi-clave-api-ec2 --query "KeyMaterial" --output text --region "$REGION" > mi-clave-api-ec2.pem
chmod 400 mi-clave-api-ec2.pem

# Crear Security Group para la API
SECURITY_GROUP_API=$(aws ec2 create-security-group --group-name api-sg --description "API Security Group" --vpc-id "$VPC_ID" --query "GroupId" --output text --region "$REGION")
aws ec2 authorize-security-group-ingress --group-id "$SECURITY_GROUP_API" --protocol tcp --port 5000 --source-group "$SECURITY_GROUP_GUI" --region "$REGION"
aws ec2 authorize-security-group-ingress --group-id "$SECURITY_GROUP_API" --protocol tcp --port 22 --source-group "$SECURITY_GROUP_GUI" --region "$REGION"
echo "Security Group API creado: $SECURITY_GROUP_API"

# Lanzar instancia EC2 para la API en la subred privada
INSTANCE_API=$(aws ec2 run-instances --image-id ami-01816d07b1128cd2d --instance-type t2.micro --key-name mi-clave-api-ec2 --security-group-ids "$SECURITY_GROUP_API" --subnet-id "$SUBNET_PRIVATE" --query "Instances[0].InstanceId" --output text --region "$REGION")
echo "Instancia API lanzada: $INSTANCE_API"



# S3 BUCKETS

# CREATE DATALAKE BUCKET

aws s3 mb s3://"$DATALAKE_BUCKET" --region "$REGION"

echo "Bucket S3 "$DATALAKE_BUCKET" creado en la región $REGION"

# CREATE GRAPH BUCKET

aws s3 mb s3://"$GRAPH_BUCKET" --region "$REGION"

echo "Bucket S3 "$GRAPH_BUCKET" creado en la región $REGION"



# LAMBDA FUNCTIONS

# CREATE LAMBDA FUNCTION (CRAWLER)


LAMBDA_ROLE=$(aws iam get-role --role-name lambda-run-role --query "Role.Arn" --output text)

aws lambda create-function --function-name CrawlerLambdaFunction --runtime python3.10 --role "$LAMBDA_ROLE" --handler lambda_function.lambda_handler --zip-file fileb://../crawler/deployment.zip --timeout 15 --memory-size 128

aws lambda create-function-url-config \
    --function-name CrawlerLambdaFunction \
    --auth-type NONE \
    --cors AllowCredentials=false,AllowHeaders=*,AllowMethods=POST,GET,PUT,AllowOrigins=*



echo "Lambda Function CrawlerLambdaFunction creada"

# CREATE LAMBDA FUNCTION (GRAPH)

aws lambda create-function --function-name GraphLambdaFunction --runtime python3.10 --role "$LAMBDA_ROLE" --handler lambda_function.lambda_handler --zip-file fileb://../graphify/deployment.zip --timeout 15 --memory-size 128

aws lambda create-function-url-config \
    --function-name GraphLambdaFunction \
    --auth-type NONE \
    --cors AllowCredentials=false,AllowHeaders=*,AllowMethods=POST,GET,PUT,AllowOrigins=*


echo "Lambda Function GraphLambdaFunction creada"



echo "Infraestructura configurada correctamente."