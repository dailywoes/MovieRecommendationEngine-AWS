import json
import boto3
def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb',region_name='ca-central-1')
    table = dynamodb.Table('webpage')
    item = table.get_item(
        Key={
            "pageId":0,
        }
        )
    table.update_item(
        Key={
            "pageId":0,
        },
        UpdateExpression='SET quantity = :val1',
        ExpressionAttributeValues={
            ':val1': item['Item']['quantity'] + 1
        }
    )
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        #Lambda thinks the entry is a decimal for some reason, cast
        #the value to an integer since json doesnt accept decimal
        "body": json.dumps(int(item['Item']['quantity']))
    }
