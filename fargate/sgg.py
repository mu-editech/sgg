import camelot
import boto3
import re
import os
import tempfile
import csv
import json
import logging
from pprint import pprint

region_name = 'ap-northeast-1'
s3 = boto3.resource('s3', region_name=region_name)
ssm = boto3.client('ssm', region_name=region_name)
s3c = boto3.client('s3', region_name=region_name)
dynamodb = boto3.resource('dynamodb', region_name=region_name)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def mv_file_in_s3(from_file_path, s3_target_path, bucket_name, file_name):

    from_file_path_with_filename = os.path.join(from_file_path, file_name)
    copy_source = {
        'Bucket': bucket_name,
        'Key': from_file_path_with_filename
    }
    s3.meta.client.copy(copy_source, bucket_name, os.path.join(s3_target_path, file_name))
    s3c.delete_object(Bucket=bucket_name, Key=from_file_path_with_filename)


def download_raw_file(bucket_name, target_path, file_name):
    """
    S3からファイルを取得する。
    sample of target_path : raw/income/1-給与明細書-20190524.pdf
    :param target_path: text
    :return: None
    """
    s3.Bucket(bucket_name).download_file(target_path, file_name)


def ssm_get_param(key):
    res = ssm.get_parameter(Name=key, WithDecryption=True)
    return res['Parameter']['Value']


def get_list_s3(bucket, prefix):
    """
    指定した prefix のすべての key の配列を返す
    :param bucket: string 取得先のS3バケット名
    :param prefix: 取得先のS3のバケット以下のパス
    :return: list: S3の指定パス内にある全ファイル名
    <!> __s3はboto3.clientのs3
    """
    paginator = s3c.get_paginator('list_objects')
    back = {'Bucket': bucket,
            'Prefix': prefix}
    pages = paginator.paginate(**back)

    # backフォルダ内のオブジェクトのキーのリストを作成
    file_list = []
    for page in pages:
        if 'Contents' in page:
            for obj in page['Contents']:
                file_list.append(obj['Key'])
        else:
            continue

    return [os.path.basename(file_name) for file_name in file_list]


class SalaryGraphGeneratorParameters():
    def __init__(self, ssm_parameters_key):
        # ssm_params = json.loads(ssm_get_param('sgg_s3_path'))
        ssm_params = json.loads(ssm_get_param(ssm_parameters_key))

        self.bucket_name = ssm_params['bucket_name']  # 'salary-gg'
        self.s3_path_add = ssm_params['s3_path_add']  # 'salary-add'
        self.s3_path_integrate = ssm_params['s3_path_integrate']  # 'salary'
        self.s3_path_storage = ssm_params['s3_path_storage']  # input-storage
        self.s3_path_error = ssm_params['s3_path_error']
        self.s3_path_raw = ssm_params['s3_path_raw']
        self.dynamo_table_name_income = ssm_params['dynamo_table_name_income']
        self.dynamo_table_name_bonus = ssm_params['dynamo_table_name_bonus']


class SalaryGraphGenerator():

    def __init__(self, file_name):
        self.file_name = file_name
        self.file_type = None
        self.file_date = None
        self.table = None


    def set_file_type(self):
        """
        処理対象ファイルの種類を判定する。
        file_type が 1 == 給与明細書
        file_type が 2 == 賞与明細書
        file_type が 3 == その他不明なファイル
        :return: None
        """
        if self.file_name[0] == '1':
            self.file_type = 1
        elif self.file_name[0] == '2':
            self.file_type = 2
        else:
            self.file_type = 3


    def chk_format_file_name(self):
        """
        ファイル名のバリデーション
        給与明細書か賞与明細書の判定も行う。
        ファイル名のサンプル：'1-給与明細書-20190524.pdf'
        :return: None
        """
        pattern = re.compile("^[1-2]{1}-.{5}-[0-9]{8}.pdf$")
        if re.match(pattern, self.file_name):
            self.set_file_type()
            if self.file_type in [1, 2]:
                return True
        return False


    def get_file_date(self):
        """
        ファイル名から、対象ファイルの年月を取得する。
        :return: text(YYYY-MM)
        """
        return '{0}-{1}'.format(self.file_name[8:12], self.file_name[12:14])


    def get_data_as_table(self):
        self.table = camelot.read_pdf(self.file_name)


    def read_csv(self, file_name):
        """
        行列を二次元配列に読み込むための方法
        :param file_name: text
        :return: list(二次元)
        """
        with open(file_name, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',')
            return [i for i in reader]


    def create_add_data(self, input_csv_file_name, max_records, add_data):
        """
        camelotで取り出したDataFrameをdictに変換する。
        :param input_csv_file_name: text
        :param max_records: int
        :param add_data: list
        :return:
        """
        _work_table = self.read_csv(input_csv_file_name)
        for i in range(0, max_records, 2):
            for column_name, value in zip(_work_table[i], _work_table[i + 1]):
                add_data[column_name] = value
        return add_data


    def update_void_to_none(self, table_dict):
        for k in table_dict.keys():
            if table_dict[k] == '':
                table_dict[k] = None

        return table_dict


    def create_add_income_record(self, parent_path, file_date):
        """
        給与明細の増分データ作成
        以下二つのメンバ変数に値を集約させる
        add_income_record_header：ヘッダー
        add_income_record_data：値

        :param file_date: text(YYYY-MM)
        :return: None
        """

        self.table[1].df.to_csv(os.path.join(parent_path, 'output1.csv'), index=False, encoding='utf-8', header=None, quoting=csv.QUOTE_ALL)
        self.table[2].df.to_csv(os.path.join(parent_path, 'output2.csv'), index=False, encoding='utf-8', header=None, quoting=csv.QUOTE_ALL)
        self.table[3].df.to_csv(os.path.join(parent_path, 'output3.csv'), index=False, encoding='utf-8', header=None, quoting=csv.QUOTE_ALL)

        table_dict = {'income_month': file_date}

        table_dict = self.create_add_data(input_csv_file_name=os.path.join(parent_path, 'output1.csv'), max_records=6, add_data=table_dict)
        table_dict = self.create_add_data(input_csv_file_name=os.path.join(parent_path, 'output2.csv'), max_records=8, add_data=table_dict)
        table_dict = self.create_add_data(input_csv_file_name=os.path.join(parent_path, 'output3.csv'), max_records=8, add_data=table_dict)

        del table_dict['']
        table_dict = self.update_void_to_none(table_dict=table_dict)

        return table_dict


    def insert_data(self, add_data, dynamo_table_name):
        """
        DynamoDBにデータをinsertする
        :param add_data: dict
        :param dynamo_table_name: text
        :return:
        """
        dynamo_table = dynamodb.Table(dynamo_table_name)
        return dynamo_table.put_item(
            Item=add_data
        )


if __name__ == '__main__':


    try:
        # パラメータストアから値を取得。パラメータストアとの接続が接続されたときExceptionできるように。
        sgg_params = SalaryGraphGeneratorParameters(ssm_parameters_key='sgg_s3_path')

        input_files = get_list_s3(bucket=sgg_params.bucket_name, prefix=sgg_params.s3_path_raw)

        if input_files:

            for input_file_name in input_files:

                try:

                    # インスタンス作成
                    sgg = SalaryGraphGenerator(file_name=input_file_name)

                    # ファイル名のバリデーション
                    if not sgg.chk_format_file_name():
                        raise ValueError('Validation Error of file name')

                    # 操作対象ファイルをS3のローデータ置き場からローカルへ取得
                    raw_file_path = os.path.join(sgg_params.s3_path_raw, sgg.file_name)
                    download_raw_file(bucket_name=sgg_params.bucket_name, target_path=raw_file_path, file_name=sgg.file_name)

                    # pdfをimportして、DataFrameに変換
                    sgg.get_data_as_table()

                    # データの日付をピックアップ
                    file_date = sgg.get_file_date()

                    # 増分のデータ作成＋S3へアップロード
                    with tempfile.TemporaryDirectory() as dir:
                        add_data = sgg.create_add_income_record(dir, file_date)
                        dynamo_table_name = sgg_params.dynamo_table_name_income if sgg.file_type == 1 else sgg_params.dynamo_table_name_bonus
                        res = sgg.insert_data(add_data=add_data, dynamo_table_name=dynamo_table_name)

                    mv_file_in_s3(
                        from_file_path=sgg_params.s3_path_raw,
                        s3_target_path=sgg_params.s3_path_storage,
                        bucket_name=sgg_params.bucket_name,
                        file_name=sgg.file_name
                    )

                except Exception as e:

                    logger.error(e)
                    mv_file_in_s3(
                        from_file_path=sgg_params.s3_path_raw,
                        s3_target_path=sgg_params.s3_path_error,
                        bucket_name=sgg_params.bucket_name,
                        file_name=input_file_name
                    )

        else:
            logger.info('There is no files in S3 {}'.format(sgg_params.s3_path_raw))
            exit()

    except Exception as e:
        logger.error(e)
