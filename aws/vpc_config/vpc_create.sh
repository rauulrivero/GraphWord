# Define la región
REGION="us-east-1"


# VPC CONFIGURATION

# Create a VPC
VPC_ID=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query "Vpc.VpcId" --output text --region "$REGION")
aws ec2 modify-vpc-attribute --vpc-id "$VPC_ID" --enable-dns-support --region "$REGION"
aws ec2 modify-vpc-attribute --vpc-id "$VPC_ID" --enable-dns-hostnames --region "$REGION"
echo "VPC created: $VPC_ID"

# Create a public subnet
SUBNET_PUBLIC=$(aws ec2 create-subnet --vpc-id "$VPC_ID" --cidr-block 10.0.1.0/24 --query "Subnet.SubnetId" --output text --region "$REGION")
aws ec2 modify-subnet-attribute --subnet-id "$SUBNET_PUBLIC" --map-public-ip-on-launch --region "$REGION"
echo "Public subnet created: $SUBNET_PUBLIC"

# Create a private subnet
SUBNET_PRIVATE=$(aws ec2 create-subnet --vpc-id "$VPC_ID" --cidr-block 10.0.2.0/24 --query "Subnet.SubnetId" --output text --region "$REGION")
echo "Private subnet created: $SUBNET_PRIVATE"

# Create an Internet Gateway
INTERNET_GATEWAY=$(aws ec2 create-internet-gateway --query "InternetGateway.InternetGatewayId" --output text --region "$REGION")
aws ec2 attach-internet-gateway --vpc-id "$VPC_ID" --internet-gateway-id "$INTERNET_GATEWAY" --region "$REGION"
echo "Internet Gateway created and attached: $INTERNET_GATEWAY"

# Create a public route table
ROUTE_TABLE_PUBLIC=$(aws ec2 create-route-table --vpc-id "$VPC_ID" --query "RouteTable.RouteTableId" --output text --region "$REGION")
aws ec2 create-route --route-table-id "$ROUTE_TABLE_PUBLIC" --destination-cidr-block 0.0.0.0/0 --gateway-id "$INTERNET_GATEWAY" --region "$REGION"
aws ec2 associate-route-table --route-table-id "$ROUTE_TABLE_PUBLIC" --subnet-id "$SUBNET_PUBLIC" --region "$REGION"
echo "Public route table created and associated: $ROUTE_TABLE_PUBLIC"

# Create a NAT Gateway
ALLOC_ID=$(aws ec2 allocate-address --query "AllocationId" --output text --region "$REGION")
NAT_GATEWAY_ID=$(aws ec2 create-nat-gateway --subnet-id "$SUBNET_PUBLIC" --allocation-id "$ALLOC_ID" --query "NatGateway.NatGatewayId" --output text --region "$REGION")
echo "NAT Gateway created: $NAT_GATEWAY_ID"

aws ec2 wait nat-gateway-available --nat-gateway-ids "$NAT_GATEWAY_ID" --region "$REGION"
echo "NAT Gateway is available: $NAT_GATEWAY_ID"

# Create a private route table
ROUTE_TABLE_PRIVATE=$(aws ec2 create-route-table --vpc-id "$VPC_ID" --query "RouteTable.RouteTableId" --output text --region "$REGION")
aws ec2 create-route --route-table-id "$ROUTE_TABLE_PRIVATE" --destination-cidr-block 0.0.0.0/0 --nat-gateway-id "$NAT_GATEWAY_ID" --region "$REGION"
aws ec2 associate-route-table --route-table-id "$ROUTE_TABLE_PRIVATE" --subnet-id "$SUBNET_PRIVATE" --region "$REGION"
echo "Private route table created and associated: $ROUTE_TABLE_PRIVATE"

# Create VPC Endpoint for S3
S3_ENDPOINT=$(aws ec2 create-vpc-endpoint \
    --vpc-id "$VPC_ID" \
    --service-name "com.amazonaws.$REGION.s3" \
    --route-table-ids "$ROUTE_TABLE_PRIVATE" \
    --query "VpcEndpoint.VpcEndpointId" \
    --output text \
    --region "$REGION")
echo "S3 VPC Endpoint creado: $S3_ENDPOINT"

echo "VPC configurada correctamente."



