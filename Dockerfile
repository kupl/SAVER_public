FROM ubuntu:20.04

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install -y \
        build-essential \
        git \
        wget \
        python \
        python3 \
        tzdata \
        libtinfo5 \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/list/*

ENV TZ=Asia/Seoul

RUN wget https://github.com/kupl/SAVER_public/releases/download/saver/SAVER-1.0-SR.tar.gz -O SAVER-1.0-SR.tar.gz \
    && tar -xvf SAVER-1.0-SR.tar.gz

# dependecy for clang-9.0
RUN apt-get install -y libz3-dev

ENV PATH=/saver-1.0/infer/bin:${PATH}

WORKDIR /home

COPY . .

# initialize benchmarks with the cached pre-analysis results
RUN cd benchmarks && python3 initialize.py
