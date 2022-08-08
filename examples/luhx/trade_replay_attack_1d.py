# -*- coding: utf-8 -*-
"""
author: luhx
create_dt: 2022/7/23 11:45
describe: 日线数据回测
"""
import os
from typing import List, Dict, Any
from czsc.strategies_attack_1d import trader_example_attack_1d as strategy_attack_1d
from czsc.utils import BarGenerator
from czsc.traders.utils import trade_replay
from czsc.utils import data_io
from czsc.objects import RawBar
from czsc.utils.user_logbook import user_log
os.environ['czsc_min_bi_len'] = "6"     # 通过环境变量设定最小笔长度，6 对应新笔定义，7 对应老笔定义

"""
有成交情况  2022-8-5
600760.SH
D:\new_jyplug\T0002\export\1d
    bars1 = bars[-1000:-4]  # 取到剩最后50
    bars2 = bars[-4:]
"""


def init_stock_info(stock_code, path)->(Dict[str, Any], List[RawBar]):
    tactic = strategy_attack_1d(stock_code)
    bars: List[RawBar] = data_io.read_1d_data(path, stock_code)
    return tactic, bars


def run_start(tactic, bars):
    base_freq = tactic["base_freq"]
    freqs = tactic["freqs"]
    bg = BarGenerator(base_freq, freqs=freqs)
    bg.base_freq_constraint[base_freq] = freqs
    # bars1 = bars[:400]
    # bars2 = bars[400:]
    bars1 = bars[:-1]
    bars2 = bars[-1:]
    user_log.info("bars1: {}-->{}".format(str(bars1[0].dt), str(bars1[-1].dt)))
    user_log.info("bars2: {}-->{}".format(str(bars2[0].dt), str(bars2[-1].dt)))
    res_path = r"C:\ts_data_czsc\trade_replay_test4"
    for bar in bars1:
        bg.update(bar)
    trade_replay(bg, bars2, strategy_attack_1d, res_path)


if __name__ == '__main__':
    tactic, bars = init_stock_info("600298.SH", r"D:\new_jyplug\T0002\export\1d")
    run_start(tactic, bars)
