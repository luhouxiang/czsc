# -*- coding: utf-8 -*-
"""
@date: 2022-7-16
@author: luhx
@funcs: 测试tushare的可用性
"""
import pytest

def test_tushare():
    import tushare as ts
    import time
    ts.set_token("93aa1639b2e9b370d0ad87346e8b812d973f4e0c653a9541d4f213e1")
    # pro = ts.pro_api('93aa1639b2e9b370d0ad87346e8b812d973f4e0c653a9541d4f213e1')
    # print("will sleep 3 seconds...")
    df = ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20180101', end_date='20181011')
    print(df)
    assert len(df) == 187



