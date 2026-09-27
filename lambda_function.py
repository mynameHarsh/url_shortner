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

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))

def get_short_url(request):
    try:
        url = request["url"]
    except:
        return "NO url provided", False

    code = generate_short_code(length=32)

    response = table.get_item(
        Key={
            'higest_key': code
        }
    )
    while "Item" in response:
        code = generate_short_code(length=32)
        response = table.get_item(
            Key={
                'higest_key': code
            }
        )

    try:
        response = table.put_item(
            Item={                      # <-- was ITEM, boto3 requires exact casing "Item"
                "higest_key": code,
                'Long_url': url,
            }
        )
    except Exception as e:              # <-- was bare "except:", now shows the real error
        print(e)
        return "failed to generate code", False

    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return code, True

    return "failed to generate code", False

