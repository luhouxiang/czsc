# -*- coding: utf-8 -*-
"""
author: luhx
create_dt: 2022/7/23 11:45
describe: 5分钟数据回测
"""
from typing import List
from czsc.strategies_sm_5m import trader_example_sm_5m as strategy
from czsc.utils import BarGenerator
from czsc.traders.utils import trade_replay
from czsc.utils import data_io
from czsc.objects import RawBar

tactic = strategy("600160.SH")
base_freq = tactic['base_freq']
bars: List[RawBar] = data_io.read_5m_data(r"D:\new_jyplug\T0002\export\small_5m", "600160.SH")
res_path = r"C:\ts_data_czsc\trade_replay_test4"


if __name__ == '__main__':
    bg = BarGenerator(base_freq, freqs=tactic['freqs'])
    bg.base_freq_constraint[base_freq] = tactic['freqs']
    bars1 = bars[:8000]
    bars2 = bars[8000:]
    for bar in bars1:
        bg.update(bar)
    trade_replay(bg, bars2, strategy, res_path)
