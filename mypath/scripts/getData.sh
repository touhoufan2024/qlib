#!/bin/bash
wget "https://hk.gh-proxy.org/https://github.com/chenditc/investment_data/releases/latest/download/qlib_bin.tar.gz" -O /tmp/qlib_bin.tar.gz
mv  ~/.qlib/qlib_data/cn_data  ~/.qlib/qlib_data/cn_data_back_$(date +%Y%m%d_%H%M%S)
mkdir -p ~/.qlib/qlib_data/cn_data
tar -zxvf /tmp/qlib_bin.tar.gz -C ~/.qlib/qlib_data/cn_data --strip-components=1