#!/usr/bin/env bash
aws dynamodb create-table \
    --table-name sgg-salary-income \
    --attribute-definitions \
        AttributeName=income_month,AttributeType=S \
    --key-schema AttributeName=income_month,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
    --region=ap-northeast-1

aws dynamodb create-table \
    --table-name sgg-salary-bonus \
    --attribute-definitions \
        AttributeName=income_month,AttributeType=S \
    --key-schema AttributeName=income_month,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
    --region=ap-northeast-1

aws dynamodb list-tables --region='ap-northeast-1' # テーブル名の取得

