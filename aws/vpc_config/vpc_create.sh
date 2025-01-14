# Define la región
REGION="us-east-1"

# Crear una VPC
VPC_ID=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query "Vpc.VpcId" --output text --region "$REGION")
aws ec2 modify-vpc-attribute --vpc-id "$VPC_ID" --enable-dns-support "{\"Value\":true}" --region "$REGION"
aws ec2 modify-vpc-attribute --vpc-id "$VPC_ID" --enable-dns-hostnames "{\"Value\":true}" --region "$REGION"
echo "VPC creada: $VPC_ID"

# Crear subred pública
SUBNET_PUBLIC=$(aws ec2 create-subnet --vpc-id "$VPC_ID" --cidr-block 10.0.1.0/24 --query "Subnet.SubnetId" --output text --region "$REGION")
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