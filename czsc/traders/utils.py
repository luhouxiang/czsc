# -*- coding: utf-8 -*-
"""
author: zengbin93
email: zeng_bin8888@163.com
create_dt: 2021/12/12 21:49
"""
import os
import dill
from tqdm import tqdm
from typing import List, Callable
from czsc.analyze import CZSC
from czsc.utils import x_round, BarGenerator, kline_pro_ex
from czsc.objects import RawBar
from czsc.traders.advanced import CzscAdvancedTrader
from czsc.utils.user_logbook import user_log


def trade_replay(bg: BarGenerator, raw_bars: List[RawBar], strategy: Callable, res_path):
    """交易策略交易过程回放"""
    os.makedirs(res_path, exist_ok=True)
    trader = CzscAdvancedTrader(bg, strategy)
    for bar in raw_bars:
        trader.update(bar)

    reply_strategy_all_data_path = os.path.join(res_path, f"replay_{strategy.__name__}@{bg.symbol}_all.html")
    trader.take_snapshot(reply_strategy_all_data_path)
    user_log.info("save reply_strategy_all_data_path: {}".format(reply_strategy_all_data_path))

    dill.dump(trader, open(os.path.join(res_path, "trader.pkl"), 'wb'))
    user_log.info("{},{}".format(trader.strategy.__name__, trader.results['long_performance']))


def trade_test(bg: BarGenerator, raw_bars: List[RawBar], strategy: Callable) ->bool:
    """交易策略测试"""
    trader = CzscAdvancedTrader(bg, strategy)
    for bar in raw_bars:
        trader.update(bar)
    return len(trader.results['long_operates']) > 0


def trader_fast_backtest(bars: List[RawBar],
                         init_n: int,
                         strategy: Callable,
                         html_path: str = None,
                         ):
    """纯 CTA 择时系统快速回测，多空交易通通支持

    :param bars: 原始K线序列
    :param init_n: 用于初始化 BarGenerator 的K线数量
    :param strategy: 策略定义函数
    :param html_path: 交易快照保存路径，默认为 None 的情况下，不保存快照
        注意，保存HTML交易快照非常耗时，建议只用于核对部分标的的交易买卖点时进行保存
    :return: 操作列表，交易对，性能评估
    """
    ts_code = bars[0].symbol
    tactic = strategy(ts_code)

    base_freq = tactic['base_freq']
    freqs = tactic['freqs']
    bg = BarGenerator(base_freq, freqs, max_count=5000)
    for bar in bars[:init_n]:
        bg.update(bar)

    ct = CzscAdvancedTrader(bg, strategy)

    signals = []
    for bar in tqdm(bars[init_n:], desc=f"{ts_code} bt"):
        ct.update(bar)
        signals.append(ct.s)
        if ct.long_pos:
            if ct.long_pos.pos_changed and html_path:
                op = ct.long_pos.operates[-1]
                file_name = f"{op['op'].value}_{op['bid']}_{x_round(op['price'], 2)}_{op['op_desc']}.html"
                file_html = os.path.join(html_path, file_name)
                ct.take_snapshot(file_html)
                user_log.info(f'snapshot saved into {file_html}')

        if ct.short_pos:
            if ct.short_pos.pos_changed and html_path:
                op = ct.short_pos.operates[-1]
                file_name = f"{op['op'].value}_{op['bid']}_{x_round(op['price'], 2)}_{op['op_desc']}.html"
                file_html = os.path.join(html_path, file_name)
                ct.take_snapshot(file_html)
                user_log.info(f'snapshot saved into {file_html}')

    res = {"signals": signals}
    res.update(ct.results)
    return res
