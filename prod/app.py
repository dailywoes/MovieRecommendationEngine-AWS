import json
import boto3
import pymysql
import pandas as pd

def lambda_handler(event, context):
    rds_host = 'imdbdataset.cylq1mw66qwl.ca-central-1.rds.amazonaws.com'
    useruser = 'masterUsername'
    userpass = 'masterPassword'
    con = pymysql.connect(host=rds_host,user=useruser,password=userpass,port=3306,database='imdbdataset')
    imdb_movie = pd.read_sql_query('select * from imdb_movie_clean_new;', con)
    imdb_movie_map = pd.read_sql_query('select * from imdb_movie_map;', con, index_col=['index'])

    input_title = 'Iron Man'
    input_year = 2008

    input_coord = imdb_movie_map[(imdb_movie['imdb_title'].str.contains('Iron Man')
                                              & (imdb_movie['imdb_year'] == 2008))]

    for column, contents in imdb_movie_map.items():
        imdb_movie_map[column] = imdb_movie_map[column].subtract(input_coord.iloc[:, imdb_movie_map.columns.
                                                     get_loc(column)].values[0], fill_value=0)
        imdb_movie_map[column] = imdb_movie_map[column].pow(2)
    imdb_movie_map['sum'] = imdb_movie_map.sum(axis=1, skipna=True)
    imdb_movie_map['dist'] = imdb_movie_map['sum'].pow(1. / 2)
    imdb_movie_map['rating'] = imdb_movie['imdb_rating'].multiply(-1)

    result = imdb_movie_map.nsmallest(25, ['dist'])
    result = imdb_movie.loc[result.nsmallest(10, ['rating']).index]
    result = result['imdb_title']

    print(result)
    
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
