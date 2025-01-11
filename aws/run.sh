#!/bin/bash

# Define la región
REGION="us-east-1"
DATALAKE_BUCKET="books-datalake"
GRAPH_BUCKET="books-graph"


# CREATE API EC2

# Crear un key pair
aws ec2 create-key-pair --key-name mi-clave-api-ec2 --query "KeyMaterial" --output text --region "$REGION" > mi-clave-api-ec2.pem
chmod 400 mi-clave-api-ec2.pem

# Crear un Security Group y capturar su ID
SECURITY_GROUP_ID_API=$(aws ec2 create-security-group --group-name api-grupo-seguridad --description "Permitir SSH y HTTP" --query "GroupId" --output text --region "$REGION")

echo "Security Group ID creado: $SECURITY_GROUP_ID_API"

# Configurar reglas de ingreso para el Security Group
aws ec2 authorize-security-group-ingress --group-id "$SECURITY_GROUP_ID_API" --protocol tcp --port 22 --cidr 0.0.0.0/0 --region "$REGION"
aws ec2 authorize-security-group-ingress --group-id "$SECURITY_GROUP_ID_API" --protocol tcp --port 5000 --cidr 0.0.0.0/0 --region "$REGION"

# Lanzar una instancia EC2 usando el Security Group creado
aws ec2 run-instances --image-id ami-01816d07b1128cd2d --instance-type t2.micro --key-name mi-clave-api-ec2 --security-group-ids "$SECURITY_GROUP_ID_API" --region "$REGION" 

echo "Instancia EC2 lanzada con el Security Group ID: $SECURITY_GROUP_ID_API"


# CREATE GUI EC2

# Crear un key pair
aws ec2 create-key-pair --key-name mi-clave-gui-ec2 --query "KeyMaterial" --output text --region "$REGION" > mi-clave-gui-ec2.pem
chmod 400 mi-clave-gui-ec2.pem

# Crear un Security Group y capturar su ID
SECURITY_GROUP_ID_GUI=$(aws ec2 create-security-group --group-name gui-grupo-seguridad --description "Permitir SSH y HTTP" --query "GroupId" --output text --region "$REGION")

echo "Security Group ID creado: $SECURITY_GROUP_ID_GUI"

# Configurar reglas de ingreso para el Security Group
aws ec2 authorize-security-group-ingress --group-id "$SECURITY_GROUP_ID_GUI" --protocol tcp --port 22 --cidr 0.0.0.0/0 --region "$REGION"
aws ec2 authorize-security-group-ingress --group-id "$SECURITY_GROUP_ID_GUI" --protocol tcp --port 8501 --cidr 0.0.0.0/0 --region "$REGION"

# Configurar reglas de salida para el Security Group
aws ec2 authorize-security-group-egress --group-id "$SECURITY_GROUP_ID_GUI" --protocol tcp --port 80 --cidr 0.0.0.0/0 --region "$REGION"

# Lanzar una instancia EC2 usando el Security Group creado
aws ec2 run-instances --image-id ami-01816d07b1128cd2d --instance-type t2.micro --key-name mi-clave-gui-ec2 --security-group-ids "$SECURITY_GROUP_ID_GUI" --region "$REGION"

echo "Instancia EC2 lanzada con el Security Group ID: $SECURITY_GROUP_ID_GUI"

# CREATE DATALAKE BUCKET

aws s3 mb s3://"$DATALAKE_BUCKET" --region "$REGION"

echo "Bucket S3 "$DATALAKE_BUCKET" creado en la región $REGION"

# CREATE GRAPH BUCKET

aws s3 mb s3://"$GRAPH_BUCKET" --region "$REGION"

echo "Bucket S3 "$GRAPH_BUCKET" creado en la región $REGION"