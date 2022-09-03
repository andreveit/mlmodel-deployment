# Run services
docker build -t lambda_img:latest src/deployment/
docker-compose -f src/deployment/docker-compose.yaml up -d

ERROR_CODE=$?
if [ ${ERROR_CODE} != 0 ]; then
    exit ${ERROR_CODE}
fi

sleep 5

# Setup da infraestrutura
export S3_ENDPOINT=http://localhost:4566

echo -e "\nCreating inference infra"
make inference-infra

echo -e "\nExecuting training pipeline"
make training-pipeline


# Invoke function
echo -e "\nRunning scoring script"
python src/integration-tests/test_lambda.py

# Get logs
echo ""
docker logs deployment_lambda_1
echo ""
ERROR_CODE=$?
if [ ${ERROR_CODE} != 0 ]; then
    docker-compose -f src/deployment/docker-compose.yaml down
    exit ${ERROR_CODE}
fi

echo -e "\n\nAll good\n"

# Clean up
unset S3_ENDPOINT
docker-compose -f src/deployment/docker-compose.yaml down
docker rmi -f $(docker images -q)
