FROM centos:7
ENV TZ="Asia/Tokyo"
ENV LANG=ja_JP.UTF8

RUN mkdir /sgg

ADD requirements.txt /sgg/
ADD sgg.py /sgg/
ADD test_sgg.py /sgg/


RUN yum -y update && \
    yum -y groupinstall "Development Tools" && \
    yum -y install \
           kernel-devel \
           kernel-headers \
           gcc-c++ \
           patch \
           libyaml-devel \
           libffi-devel \
           autoconf \
           automake \
           make \
           libtool \
           bison \
           tk-devel \
           zip \
           wget \
           tar \
           gcc \
           zlib \
           zlib-devel \
           bzip2 \
           bzip2-devel \
           readline \
           readline-devel \
           sqlite \
           sqlite-devel \
           openssl \
           openssl-devel \
           git \
           gdbm-devel \
           python-devel \
           ghostscript \
           ghostscript-devel \
           libSM.x86_64 \
           libXext.x86_64 \
           lzma \
           xz-devel



# Python3.5.2をインストール
# Python3.5.2をダウンロード
WORKDIR /root
RUN wget https://www.python.org/ftp/python/3.6.2/Python-3.6.2.tgz && \
    tar xzvf Python-3.6.2.tgz

# makeでインストール
WORKDIR ./Python-3.6.2
RUN ./configure --with-threads && \
    make install

# pipインストール(最新版)
RUN wget https://bootstrap.pypa.io/get-pip.py  && \
    python get-pip.py && \
    pip3 install --upgrade pip && \
    pip3 install -r /sgg/requirements.txt

# ロケール設定をして、日本語ファイル名をあつかえるようにする。
RUN localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG="ja_JP.UTF-8" \
    LANGUAGE="ja_JP:ja" \
    LC_ALL="ja_JP.UTF-8"

CMD python3 /sgg/sgg.py
