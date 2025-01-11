#!/bin/bash

# Define la región
REGION="us-east-1"

# Crear un key pair
aws ec2 create-key-pair --key-name mi-clave-api-ec2 --query "KeyMaterial" --output text --region "$REGION" > mi-clave-api-ec2.pem
chmod 400 mi-clave-api-ec2.pem

# Crear un Security Group y capturar su ID
SECURITY_GROUP_ID=$(aws ec2 create-security-group --group-name api-grupo-seguridad --description "Permitir SSH y HTTP" --query "GroupId" --output text --region "$REGION")

echo "Security Group ID creado: $SECURITY_GROUP_ID"

# Configurar reglas de ingreso para el Security Group
aws ec2 authorize-security-group-ingress --group-id "$SECURITY_GROUP_ID" --protocol tcp --port 22 --cidr 0.0.0.0/0 --region "$REGION"
aws ec2 authorize-security-group-ingress --group-id "$SECURITY_GROUP_ID" --protocol tcp --port 5000 --cidr 0.0.0.0/0 --region "$REGION"

# Lanzar una instancia EC2 usando el Security Group creado
aws ec2 run-instances --image-id ami-01816d07b1128cd2d --instance-type t2.micro --key-name mi-clave-api-ec2 --security-group-ids "$SECURITY_GROUP_ID" --region "$REGION"

echo "Instancia EC2 lanzada con el Security Group ID: $SECURITY_GROUP_ID"
