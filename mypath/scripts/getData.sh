#!/bin/bash
wget -e use_proxy=yes -e https_proxy=127.0.0.1:10808 https://github.com/chenditc/investment_data/releases/latest/download/qlib_bin.tar.gz -O /tmp/qlib_bin.tar.gz
mv  ~/.qlib/qlib_data/cn_data  ~/.qlib/qlib_data/cn_data_back
mkdir -p ~/.qlib/qlib_data/cn_data
tar -zxvf /tmp/qlib_bin.tar.gz -C ~/.qlib/qlib_data/cn_data --strip-components=1