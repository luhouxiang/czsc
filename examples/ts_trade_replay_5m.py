# -*- coding: utf-8 -*-
"""
author: luhx
create_dt: 2022/7/23 11:45
describe: 5分钟数据回测
"""
from ts_fast_backtest import dc
from czsc.data import freq_cn2ts
from czsc.strategies_5m import trader_strategy_5m as strategy
from czsc.utils import BarGenerator
from czsc.traders.utils import trade_replay
from czsc.utils import data_io
from czsc.objects import RawBar
from czsc.enum import Freq

tactic = strategy("600036.SH")
base_freq = tactic['base_freq']
# bars = dc.pro_bar_minutes('600000.SH', "20150101", "20220101", freq=freq_cn2ts[base_freq],
#                           asset="E", adj="hfq", raw_bar=True)
bars = data_io.read_5m_data(r"D:\new_jyplug\T0002\export\5m", "600036.SH")
res_path = r"C:\ts_data_czsc\trade_replay_test4"


if __name__ == '__main__':
    bg = BarGenerator(base_freq, freqs=tactic['freqs'])
    bars1 = bars[:8000]
    bars2 = bars[8000:]
    for bar in bars1:
        bg.update(bar)
    trade_replay(bg, bars2, strategy, res_path)
