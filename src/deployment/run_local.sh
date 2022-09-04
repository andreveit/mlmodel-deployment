cd src/deployment

# Run container
docker build -t lambda_img:latest .
docker run --rm -it -d -p 9000:8080 \
                        -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
                        -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
                        -e ARTIFACT_BUCKET_NAME=$ARTIFACT_BUCKET_NAME \
                        -e INFERENCE_BUCKET_NAME=$INFERENCE_BUCKET_NAME \
                        --name lambda \
                        lambda_img:latest 

# Invoke function
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'

# Get logs
echo ""
docker logs lambda

ERROR_CODE=$?
if [ ${ERROR_CODE} != 0 ]; then
    docker kill lambda
    exit ${ERROR_CODE}
fi

# Clean up
docker stop lambda
docker image rm lambda_img:latest