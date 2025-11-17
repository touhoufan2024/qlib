#!/bin/bash

# gh-proxy options:
urlA="https://gh-proxy.org"
urlB="https://hk.gh-proxy.org"
urlC="https://cdn.gh-proxy.org"
urlD="https://edgeone.gh-proxy.org"

wget "${urlC}/https://github.com/chenditc/investment_data/releases/latest/download/qlib_bin.tar.gz" -O /tmp/qlib_bin.tar.gz
mv  ~/.qlib/qlib_data/cn_data  ~/.qlib/qlib_data/cn_data_back_$(date +%Y%m%d_%H%M%S)
mkdir -p ~/.qlib/qlib_data/cn_data
tar -zxvf /tmp/qlib_bin.tar.gz -C ~/.qlib/qlib_data/cn_data --strip-components=1