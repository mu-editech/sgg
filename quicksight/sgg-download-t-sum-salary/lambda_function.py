

import boto3
import json
import logging
import pandas as pd

logger = logging.getLogger()
logger.setLevel(logging.INFO)

region_name = 'ap-northeast-1'
ssm = boto3.client('ssm', region_name=region_name)
dynamodb = boto3.resource('dynamodb', region_name=region_name)


def ssm_get_param(key):
    res = ssm.get_parameter(Name=key, WithDecryption=True)
    return res['Parameter']['Value']


def scan_all_table_data(table_name):
    table = dynamodb.Table(table_name)

    res = table.scan()
    table_data = res['Items']
    # table_datas = []

    while 'LastEvaluatedKey' in res:
        res = table.scan(
            ExclusiveStartKey=res['LastEvaluatedKey']
        )
        table_data.extend(res[('Items')])

    return table_data

# 辞書データをcsvに変換するためのメソッド追記。pandasを使うとできるらしい。
def convert_json_to_csv(dict_data):
    pass


def lambda_handler(event, context):
    logger.info(event)
    ssm_params = json.loads(ssm_get_param('sgg_s3_path'))

    bucket_name = ssm_params['bucket_name']
    dynamo_table_name_income = ssm_params['dynamo_table_name_income']
    dynamo_table_name_bonus = ssm_params['dynamo_table_name_bonus']
    data = scan_all_table_data(dynamo_table_name_bonus)

    # TODO
    # 辞書データをcsvに変換するためのメソッド追記。pandasを使うとできるらしい。
    convert_json_to_csv(dict_data=data)