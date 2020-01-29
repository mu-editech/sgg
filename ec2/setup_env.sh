#!/usr/bin/env bash

# 参考：https://qiita.com/tisk_jdb/items/01bd6ef9209acc3a275f
sudo yum update -y
sudo yum install git -y

git clone https://github.com/yyuu/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
source ~/.bash_profile

sudo yum install gcc zlib-devel bzip2 bzip2-devel readline readline-devel sqlite sqlite-devel openssl openssl-devel tk-devel libffi-devel tcl.x86_64 tk.x86_64 -y # Pythonを使うのに必要なものたち
sudo yum install ghostscript ghostscript-devel libSM.x86_64 libXext.x86_64 lzma xz-devel -y # camelot-pyを使うのに必要なものたち

pyenv install 3.6.2
pyenv global 3.6.2
pyenv rehash

# prepare for App
echo "camelot-py[cv]
boto3" > requirements.txt
pip install --update pip
pip install -r requirements.txt

# for unittest
pip install pytest