
when start any server run these commands
export AWS_ACCESS_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export AWS_ENDPOINT_URL=http://localhost:4566
export DYNAMODB_ENDPOINT=http://localhost:4566

or 

eval $(floci env)
export DYNAMODB_ENDPOINT=http://localhost:4566



aws dynamodb create-table --table-name Links --attribute-definitions AttributeName=higest_key,AttributeType=S --key-schema AttributeName=higest_key,KeyType=HASH --billing-mode PAY_PER_REQUEST \
--endpoint-url http://localhost:4566
