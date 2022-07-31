# -*- coding: utf-8 -*-
"""
@author: luhx
@email: luhouxiang@hotmail.com
create_dt: 2022-7-16 19:17
describe: 以 Tushare 数据为例编写的最简单的入门
"""
import os
import pandas as pd
from typing import List
from collections import OrderedDict

from czsc import CZSC

os.environ['czsc_verbose'] = "1"        # 是否输出详细执行信息，0 不输出，1 输出
os.environ['czsc_min_bi_len'] = "6"     # 通过环境变量设定最小笔长度，6 对应新笔定义，7 对应老笔定义
pd.set_option('mode.chained_assignment', None)
pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 20)

from czsc.utils import data_io
from czsc.objects import RawBar

bars: List[RawBar] = data_io.read_5m_data(r"D:\new_jyplug\T0002\export\5m", "600160.SH")
c = CZSC(bars)
c.open_in_browser()

