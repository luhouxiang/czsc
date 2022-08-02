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

file_list, name_list = get_day_file_list(r"D:\new_jyplug\T0002\export\1d")
print("file_number: {}".format(len(name_list)))
for file in name_list:
    print(file)

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