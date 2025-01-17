#!/bin/bash

# Define la región
REGION="us-east-1"


# CREATE GUI EC2

# Crear a key pair
aws ec2 create-key-pair --key-name my-gui-ec2-key --query "KeyMaterial" --output text --region "$REGION" > my-gui-ec2-key.pem
chmod 400 my-gui-ec2-key.pem

# Create Security Group for GUI
SECURITY_GROUP_GUI=$(aws ec2 create-security-group --group-name gui-sg --description "GUI Security Group" --vpc-id "$VPC_ID" --query "GroupId" --output text --region "$REGION")
aws ec2 authorize-security-group-ingress --group-id "$SECURITY_GROUP_GUI" --protocol tcp --port 22 --cidr 0.0.0.0/0 --region "$REGION"
aws ec2 authorize-security-group-ingress --group-id "$SECURITY_GROUP_GUI" --protocol tcp --port 8501 --cidr 0.0.0.0/0 --region "$REGION"
echo "Security Group GUI creado: $SECURITY_GROUP_GUI"

# Launch EC2 instance for GUI in the public subnet
INSTANCE_GUI=$(aws ec2 run-instances --image-id ami-01816d07b1128cd2d --instance-type t2.micro --key-name my-gui-ec2-key --security-group-ids "$SECURITY_GROUP_GUI" --subnet-id "$SUBNET_PUBLIC" --query "Instances[0].InstanceId" --output text --region "$REGION")
echo "Instancia GUI lanzada: $INSTANCE_GUI"