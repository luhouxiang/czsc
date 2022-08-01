# -*- coding: utf-8 -*-
"""
author: luhx
create_dt: 2022/7/23 11:45
describe: 日线数据回测
"""
import os
from typing import List
from czsc.strategies_1d import trader_example_1d as strategy_1d
from czsc.utils import BarGenerator
from czsc.traders.utils import trade_replay
from czsc.utils import data_io
from czsc.objects import RawBar
from czsc.utils.user_logbook import user_log
os.environ['czsc_min_bi_len'] = "6"     # 通过环境变量设定最小笔长度，6 对应新笔定义，7 对应老笔定义


tactic = strategy_1d("000333.SZ")
base_freq = tactic['base_freq']
bars: List[RawBar] = data_io.read_1d_data(r"D:\new_jyplug\T0002\export\1d", "000333.SZ")
res_path = r"C:\ts_data_czsc\trade_replay_test4"


if __name__ == '__main__':
    bg = BarGenerator(base_freq, freqs=tactic['freqs'])
    bg.base_freq_constraint[base_freq] = tactic['freqs']
    bars1 = bars[-80:-50]  # 取到剩最后50
    bars2 = bars[-50:]  # 最后的50个
    user_log.info("bars1: {}-->{}".format(str(bars1[0].dt), str(bars1[-1].dt)))
    user_log.info("bars2: {}-->{}".format(str(bars2[0].dt), str(bars2[-1].dt)))

    for bar in bars1:
        bg.update(bar)
    trade_replay(bg, bars2, strategy_1d, res_path)
