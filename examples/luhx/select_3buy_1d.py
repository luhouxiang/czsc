# -*- coding: utf-8 -*-
"""
@date: 2022-8-1 23:36
@author: luhx
@describe: 3买日线选股系统
1 遍历A股，取出股票数据和股票代码
2 将每一只股票都请求一遍trade_test, 对于有此行为的，视为3买信号
"""
import os
from typing import List
from czsc.strategies_1d import trader_example_1d as strategy_1d
from czsc.utils import BarGenerator
from czsc.traders.utils import trade_test
from czsc.utils import data_io, file_help
from czsc.objects import RawBar
from czsc.utils.user_logbook import user_log
os.environ['czsc_min_bi_len'] = "6"     # 通过环境变量设定最小笔长度，6 对应新笔定义，7 对应老笔定义


def get_day_file_list(path):
    return file_help.get_file_list(path, file_help.valid_contract_file)

def do_one_contract(path, symbol):

    tactic = strategy_1d(symbol)
    base_freq = tactic['base_freq']
    bars: List[RawBar] = data_io.read_1d_data(path, symbol)
    bg = BarGenerator(base_freq, freqs=tactic['freqs'])
    bars1 = bars[-100:-1]
    bars2 = bars[-1:]
    for bar in bars1:
        bg.update(bar)
    return trade_test(bg, bars2, strategy_1d)

def do_all_contract(path = r"D:\new_jyplug\T0002\export\1d"):
    user_log.info("file_path: {}".format(path))
    file_names = get_day_file_list(path)
    for index,name in enumerate(file_names):
        c = name[:-4].split("#")
        symbol = "{}.{}".format(c[1], c[0])
        if do_one_contract(path, symbol):
            user_log.info("[%d]: 3 buy: {}".format(index+1, symbol))
        if index + 1 % 10 == 0:
            print("have_run_[{:04d}] symbols".format(index+1))


#
# tactic = strategy_1d("000333.SZ")
# base_freq = tactic['base_freq']
# bars: List[RawBar] = data_io.read_1d_data(r"D:\new_jyplug\T0002\export\1d", "000333.SZ")
# res_path = r"C:\ts_data_czsc\trade_replay_test4"
#
#
# if __name__ == '__main__':
#     bg = BarGenerator(base_freq, freqs=tactic['freqs'])
#     bg.base_freq_constraint[base_freq] = tactic['freqs']
#     bars1 = bars[-300:-1]  # 取300根日线
#     bars2 = bars[-1:] # 取最后一根K线
#     user_log.info("bars1: {}-->{}".format(str(bars1[0].dt), str(bars1[-1].dt)))
#     user_log.info("bars2: {}-->{}".format(str(bars2[0].dt), str(bars2[-1].dt)))
#
#     for bar in bars1:
#         bg.update(bar)
#     trade_test(bg, bars2, strategy_1d, res_path)

if __name__ == '__main__':
    do_all_contract()