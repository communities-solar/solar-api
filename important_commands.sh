#!/bin/bash

################################################################################
# PART 1: Configure NodeJs, Python and CDK libraries
################################################################################

# Install NodeJs and Python
# -->  https://nodejs.org/en/download/
# -->  https://www.python.org/downloads/

# Verify that NodeJs/npm is installed correctly
node --version
npm --version

# Verify that Python/pip is installed correctly
python --version || python3 --version
pip --version || pip3 --version

# Install AWS-CDK (on NodeJs)
sudo npm install -g aws-cdk

# Verify correct install of AWS-CDK
npm list --global | grep aws-cdk

# Install AWS construct library on Python
pip install aws-cdk-lib


################################################################################
# PART 2: Initial Project Setup (Only run these at the beginning)
################################################################################

# Configure AWS credentials (follow steps)
aws configure

# Bootstrap CDK (provision initial resources to work with CDK.. S3, roles, etc)
#! Change "ACCOUNT-NUMBER-1" and "REGION-1" to your needed values 
cdk bootstrap aws://ACCOUNT-NUMBER-1/REGION-1

# Create the CDK project's folder
mkdir cdk-solar-api
cd cdk-solar-api || echo "Make sure that the folder exists"

# Initialize project
cdk init --language python

# If the virtual environment didn't create, do it manually
python3 -m venv ./.venv

# Access the virtual environment and install its dependencies
source .venv/bin/activate || echo "Make sure that virtual env exists"
pip install -r requirements.txt || pip3 install -r requirements.txt


################################################################################
# PART 3: Main CDK commands (most used)
################################################################################

cdk bootstrap

# Setup environment (choose one)
export ENVIRONMENT="dev"
export ENVIRONMENT="prod"

# Storage Stack RDS
cdk synthesize --app "python3 app_storage_rds.py"
cdk diff --app "python3 app_storage_rds.py"
cdk deploy --app "python3 app_storage_rds.py"
cdk destroy --app "python3 app_storage_rds.py"

# Compute Stack API-Lambda (requires Storage Stacks already deployed)
cdk synthesize --app "python3 app_compute_api_lambda.py"
cdk diff --app "python3 app_compute_api_lambda.py"
cdk deploy --app "python3 app_compute_api_lambda.py"
cdk destroy --app "python3 app_compute_api_lambda.py"


################################################################################
# PART 4: Other CDK usefull commands
################################################################################

# Help
cdk --help
cdk deploy --help

# Lists the stacks in the app
cdk list

# Synthesizes and prints the CloudFormation template for the specified stack(s)
cdk synthesize

# Deploys the CDK Toolkit staging stack (necessary resources in AWS account)
cdk bootstrap

# Deploys the specified stack(s)
cdk deploy

# Destroys the specified stack(s)
cdk destroy

# Compares the specified stack with the deployed stack or a local CloudFormation template
cdk diff

# Displays metadata about the specified stack
cdk metadata

# Creates a new CDK project in the current directory from a specified template
cdk init

# Manages cached context values
cdk context

# Opens the CDK API reference in your browser
cdk docs

# Checks your CDK project for potential problems
cdk doctor
