import requests
import sys
import json
import pandas as pd
from datetime import datetime

import boto3
import base64
from botocore.exceptions import ClientError
import json

'''
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
export AWS_ACCESS_KEY_ID='WWWWWWW'
export AWS_SECRET_ACCESS_KEY='OOOOOOOOO'
'''

secret_name = "kot"
region_name = "ca-central-1"
session = boto3.session.Session()
client = session.client(
	service_name='secretsmanager',
	region_name=region_name
)
try:
	get_secret_value_response = client.get_secret_value(
		SecretId=secret_name
	)
	secret = json.loads(get_secret_value_response['SecretString'])
except:
	print(sys.exc_info()[0])

try:
	access_token = secret['TWITTER_DEV_ACCESS_TOKEN']
	json_file = secret['TWITTER_DEV_JSON_FILE']
except:
	print('failed to get credentials')
	exit()

search_headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-type': 'application/json'   
}

search_params = {
    'query': 'Toronto Real Estate lang:en',
    'maxResults': '100',
    'fromDate': '202008020000',
    'toDate': '202008102359'
}

try:
    search_url = 'https://api.twitter.com/1.1/tweets/search/fullarchive/'+json_file
    search_resp = requests.post(search_url, headers=search_headers, json=search_params)
    tweets = json.loads(search_resp.text)['results']
    df = pd.DataFrame()
    columns = ['created_at','text','user','quote_count','reply_count','retweet_count','favorite_count','lang']
    for t in tweets:
        series = []
        series.append(pd.to_datetime(t['created_at']))
        series.append(t['text'])
        series.append(t['user']['name'])
        series.append(t['quote_count'])
        series.append(t['reply_count'])
        series.append(t['retweet_count'])
        series.append(t['favorite_count'])
        series.append(t['lang'])
        dfa = pd.DataFrame([series])
        df = df.append(dfa)
    df.columns = columns	
    df.index = pd.to_datetime(df['created_at'])
    df = df.drop(columns=['created_at'])
    filename = 'csv/tweets/tweets-' + datetime.now().strftime("%Y-%m-%d-%H-%M") + '.csv'
    df.to_csv(filename,sep=';')
    print(filename,'saved')
except:
    print("failed to get tweets : ", sys.exc_info()[0],' ', sys.exc_info()[1])