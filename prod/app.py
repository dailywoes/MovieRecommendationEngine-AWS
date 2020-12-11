import json
import boto3
import rds_config
import pymysql

rds_host = 'imdbdataset.cylq1mw66qwl.ca-central-1.rds.amazonaws.com'
username = rds_config.masterUsername
password = rds_config.masterPassword
database = rds_config.imdbdataset

try:
    con = pymysql.connect(rds_host, user=username, passwd=password, db=database, connect_timeout=5)
except pymysql.MySQLError as e:
    print('whoops')

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
    rds = boto3.resource('rds')
    #input_title = event['title']
    #input_year = event['year']
    #event["queryStringParameters"]['title']
    #print(input_title)
    print('')
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        #Lambda thinks the entry is a decimal for some reason, cast
        #the value to an integer since json doesnt accept decimal
        "body": json.dumps(event["queryStringParameters"]['title'])
    }
