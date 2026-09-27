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

def get_long_url(request):

    try:
        url = request["url"]
    except:
        return "NO url provided",False

    response = table.get_item(
        Key={
            'higest_key': url
        }
    )
    if "Item" in response:
        item = response.get('Item').get("Long_url")
        return item, True
    else:
        return "url do not exist",False


print(get_long_url({"url": "PASTE_A_REAL_CODE_HERE"}))
print(get_long_url({"url": "zzzzzz_not_real"}))

# get_short_url
code, ok = get_short_url({"url": "https://example.com/some/very/long/path"})
print(code, ok)

# get_long_url
long_url, ok = get_long_url({"url": code})
print(long_url, ok)