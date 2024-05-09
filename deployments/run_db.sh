export IMAGE_NAME=postgresql_image
docker build -t $IMAGE_NAME -f ./deployments/dockerfile.postgresql
docker run \
    --name $IMAGE_NAME \
    -e POSTGRES_DB=$POSTGRES_DB \
    -e POSTGRES_USER=$POSTGRES_USER \
    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    -p 5432:5432 \
    -d postgres:latest