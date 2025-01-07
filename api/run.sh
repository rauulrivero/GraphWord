# docker run --rm -p 4566:4566 -p 4510-4559:4510-4559 localstack/localstack

aws ec2 create-key-pair --key-name mi-clave-ec2 --query "KeyMaterial" --output text > mi-clave-ec2.pem
 
chmod 400 mi-clave-ec2.pem

aws ec2 create-security-group --group-name mi-grupo-seguridad --description "Permitir SSH y HTTP"
aws ec2 authorize-security-group-ingress --group-id sg-035579a2c984b2a63 --protocol tcp --port 22 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id sg-035579a2c984b2a63 --protocol tcp --port 5000 --cidr 0.0.0.0/0

aws ec2 run-instances --image-id ami-0ff8a91507f77f867 --instance-type t2.micro --key-name mi-clave-ec2 --security-group-ids sg-035579a2c984b2a63 --user-data file://./user_script.sh