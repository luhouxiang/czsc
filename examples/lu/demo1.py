# -*- coding: utf-8 -*-
"""
@author: luhx
@email: luhouxiang@hotmail.com
create_dt: 2022-7-16 19:17
describe: 以 Tushare 数据为例编写的最简单的入门
"""
import os
import pandas as pd
from collections import OrderedDict
from czsc import CZSC, CzscAdvancedTrader, Freq
from czsc.utils import BarGenerator
from czsc import signals
from czsc.traders.ts_backtest import TsDataCache

os.environ['czsc_verbose'] = "1"        # 是否输出详细执行信息，0 不输出，1 输出
os.environ['czsc_min_bi_len'] = "6"     # 通过环境变量设定最小笔长度，6 对应新笔定义，7 对应老笔定义
pd.set_option('mode.chained_assignment', None)
pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 20)

# 需要先设置 Tushare Token，否则报错，无法执行
# TsDataCache 是统一的 tushare 数据缓存入口，适用于需要重复调用接口的场景
dc = TsDataCache(data_path=r"C:\ts_data", sdt='2000-01-02', edt='2022-07-16')


# 在浏览器中查看单标的单级别的分型、笔识别结果
bars = dc.pro_bar(ts_code='000768.SZ', asset='E', start_date='20210306', end_date="20220716", freq='D')
c = CZSC(bars)
c.open_in_browser()

