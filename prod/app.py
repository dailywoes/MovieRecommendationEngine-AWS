import json
import boto3
import pymysql
import pandas

def lambda_handler(event, context):
    rds_host = 'imdbdataset.cylq1mw66qwl.ca-central-1.rds.amazonaws.com'
    useruser = 'masterUsername'
    userpass = 'masterPassword'
    con = pymysql.connect(host=rds_host,user=useruser,password=userpass,port=3306,database='imdbdataset')
    imdb_movie = pd.read_sql_query('select * from imdb_movie_clean_new;', con)
    print(imdb_movie)

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
