#!/bin/bash

cd "$(dirname "$0")"

# Cria repositório se não exista
aws ecr describe-repositories --repository-names lambdas-repo \
        || aws ecr create-repository --repository-name lambdas-repo

# Obtem URI
REPO_URI=$(aws ecr describe-repositories --repository-names lambdas-repo --query "repositories[0].repositoryUri" --output text)

echo -e "URI = $REPO_URI"

# Push image
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
docker build -t lambdas-repo .
docker tag lambdas-repo:latest $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/lambdas-repo:latest
docker push $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/lambdas-repo:latest