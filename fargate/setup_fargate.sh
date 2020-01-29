#!/usr/bin/env bash
# onedayで行った、EC2にDockerを仕込んで起動するまでのシェル
rpm -qa | grep docker # dockerが入っていないか確認。
yum install -y yum-utils device-mapper-persistent-data lvm2 # Dockerをインストールするのに必要なyumを入れる。
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo # yumで取ってくるアドレス先の設定。これでDOker公式からパッケージをダウンロードできるように設定した。
yum install -y docker-ce docker-ce-cli containerd.io # Docker CE のインストール
# --- ここまではお勉強用メモ。実際はここから

#Dockerをダウンロード＆インストール
yum install -y docker

#ひょっとしたらいらないかも。
sudo ln -s /usr/lib/systemd/system/docker.service /etc/systemd/system/

#Docker エンジンを起動する。
sudo systemctl start docker

#Dockerイメージを作成する。
sudo docker build -t sgg .

#???のところにインプットとなる帳票の名前を入れる
sudo docker run -e file_name=??? -t sgg
sudo docker run -e file_name=1-給与明細書-20170425.pdf -t sgg

sudo docker run -t sgg

#コンテナの仲に入れる
sudo docker run -it sgg /bin/bash

# ECR編
#ECR新規作成
aws ecr create-repository --repository-name sgg --region ap-northeast-1

#{
#    "repository": {
#        "registryId": "991305605809",
#        "repositoryName": "sgg",
#        "repositoryArn": "arn:aws:ecr:ap-northeast-1:991305605809:repository/sgg",
#        "createdAt": 1577437763.0,
#        "repositoryUri": "991305605809.dkr.ecr.ap-northeast-1.amazonaws.com/sgg"
#    }
#}


#Dockerイメージ名変更。リポジトリとイメージは同じ名前である必要がある。リポジトリのIDはレスポンスのrepositoryUriでわかる。
sudo docker tag sgg 991305605809.dkr.ecr.ap-northeast-1.amazonaws.com/sgg

#おまじない（トークンの払い出し）
aws ecr get-login --no-include-email --region=ap-northeast-1

#上のコマンドがログインコマンドになっている。それを鬱。管理者権限必要。
sudo docker login -u AWS -p eyJwY.....== https://991305605809.dkr.ecr.ap-northeast-1.amazonaws.com

#dockerイメージをプッシュする。（ログインしておかないとプッシュできん）
sudo docker push 991305605809.dkr.ecr.ap-northeast-1.amazonaws.com/sgg

