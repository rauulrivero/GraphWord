```markdown
# GraphWord Project

This README describes the necessary steps to run the **GraphWord** project, including setting up environments, dependencies, AWS infrastructure, and deploying EC2 instances for the API and graphical interface.

---

## 1. Create a Virtual Environment

First, create a virtual environment to isolate the project dependencies and avoid conflicts with other projects. Use the following commands:

```bash
python -m venv myenv
source myenv/bin/activate # On Linux/MacOS
myenv\Scripts\activate # On Windows
```

## 2. Install Dependencies

The `requirements.txt` file contains all the libraries needed to run the project. Install them by running:

```bash
pip install -r requirements.txt
```

## 3. Create ZIP Files for Lambda Functions

To deploy Lambda functions in AWS, you need to create a ZIP file containing the code and required dependencies. Follow these steps:

```bash
cd <project>

export PATH=$PATH:/c/msys64/usr/bin

mkdir packages
pip install --no-user -r requirements.txt -t packages/

cd packages/
zip -r ../deployment.zip .
cd ..

zip -g deployment.zip lambda_function.py
zip -r deployment.zip src/
```

### Included Lambda Functions
- **crawler**: Responsible for downloading books.
- **graphify**: Processes and creates graphs from downloaded books.

## 4. Configure AWS Credentials

To enable the project to interact with AWS services, configure your credentials in the `~/.aws/credentials` file:

```ini
[default]
aws_access_key_id=YOUR_ACCESS_KEY
aws_secret_access_key=YOUR_SECRET_KEY
aws_session_token=YOUR_SESSION_TOKEN
```

## 5. Initialize AWS Infrastructure

The aws directory contains a script called `run.sh` to initialize the AWS infrastructure. Ensure it has execution permissions and then run it:

```bash
chmod +x run.sh
./run.sh
```

## 6. Configure EC2 Instances

To configure the EC2 instances, you will need two open terminals: one for the API and one for the graphical interface (GUI).

### Transfer SSH Keys

First, transfer the necessary keys:

```bash
scp -i my-gui-ec2-key.pem my-api-ec2-key.pem ec2-user@<GUI_IP_PUBLIC>:/home/ec2-user/
```

### Configuration in Terminal 1 (API EC2)

1. Connect to the EC2 instance for the API:

```bash
ssh -i my-gui-ec2-key.pem ec2-user@<GUI_IP_PUBLIC>
chmod 400 my-api-ec2-key.pem
ssh -i my-api-ec2-key.pem ec2-user@<API_IP_PRIVATE>
```

2. Install dependencies and clone the project:

```bash
sudo yum update -y
sudo yum install python3-pip -y
sudo yum install git -y
sudo yum install awscli -y

git clone https://github.com/rauulrivero/GraphWord.git
cd GraphWord/api
pip install -r requirements.txt
```

3. Configure AWS credentials and environment variables:

```bash
aws configure
nano ~/.aws/credentials # Copy and paste AWS credentials

nano .env # Set environment variables
```

Example environment variables:

```env
FLASK_ENV=development # or production or test

GRAPH_BUCKET_NAME=books-graph
JSON_FILE_KEY=graph.json

CRAWLER_LAMBDA_NAME=CrawlerLambdaFunction
GRAPH_LAMBDA_NAME=GraphLambdaFunction
```

4. Deploy the API:

```bash
python3 app.py
```

### Configuration in Terminal 2 (GUI EC2)

1. Connect to the EC2 instance for the GUI:

```bash
ssh -i my-gui-ec2-key.pem ec2-user@<GUI_IP_PUBLIC>
```

2. Install dependencies and clone the project:

```bash
#!/bin/bash -xeu

sudo yum update -y
sudo yum install python3-pip -y
sudo yum install git -y
sudo yum install awscli -y

git clone https://github.com/rauulrivero/GraphWord.git
cd GraphWord/streamlit

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Configure AWS credentials:

```bash
aws configure
nano ~/.aws/credentials # Copy and paste AWS credentials
```

4. Deploy the graphical interface:

```bash
streamlit run streamlit_app.py
```

---

With these steps, you will have the necessary infrastructure and EC2 instances configured for the proper functioning of the **GraphWord** project.
```

