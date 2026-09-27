import json
import string
import random
import os
import boto3

dynamodb=boto3.resource(
    "dynamodb",
    endpoint_url=os.environ.get("DYNAMODB_ENDOINT")

)
table=dynamodb.Table("Links")