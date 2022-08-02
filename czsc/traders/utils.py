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
    # reply_before_data_path = os.path.join(res_path, f"replay_before_{strategy.__name__}@{bg.symbol}.html")
    # trader.take_snapshot(reply_before_data_path)
    # user_log.info("save reply_before_data_path: {}".format(reply_before_data_path))
    for bar in raw_bars:
        trader.update(bar)
        # if trader.long_pos and trader.long_pos.pos_changed:
        #     op = trader.long_pos.operates[-1]
        #     _dt = op['dt'].strftime('%Y%m%d#%H%M')
        #     file_name = f"{op['op'].value}_{_dt}_{op['bid']}_{x_round(op['price'], 2)}_{op['op_desc']}.html"
        #     file_html = os.path.join(res_path, file_name)
        #     # trader.take_snapshot(file_html)   # remove by luhx 这儿的回放记录没必要，实在太慢，每记录一次至少2秒 2022-7-25
        #     user_log.info(f'snapshot saved into {file_html}')
        #
        # if trader.short_pos and trader.short_pos.pos_changed:
        #     op = trader.short_pos.operates[-1]
        #     _dt = op['dt'].strftime('%Y%m%d#%H%M')
        #     file_name = f"{op['op'].value}_{_dt}_{op['bid']}_{x_round(op['price'], 2)}_{op['op_desc']}.html"
        #     file_html = os.path.join(res_path, file_name)
        #     # trader.take_snapshot(file_html)
        #     user_log.info(f'snapshot saved into {file_html}')

    # c = CZSC(raw_bars, max_bi_num=10000)
    # kline = [x.__dict__ for x in c.bars_raw]
    # if c.bi_list:
    #     bi = [{'dt': x.fx_a.dt, "bi": x.fx_a.fx} for x in c.bi_list] + \
    #          [{'dt': c.bi_list[-1].fx_b.dt, "bi": c.bi_list[-1].fx_b.fx}]
    # else:
    #     bi = None
    # fx = []
    # for bi_ in c.bi_list:
    #     fx.extend([{'dt': x.dt, "fx": x.fx} for x in bi_.fxs[1:]])

    # 构建 BS 序列
    # bs = []
    # if trader.long_pos:
    #     bs.extend(trader.long_pos.operates)
    # if trader.short_pos:
    #     bs.extend(trader.short_pos.operates)
    # if len(c.zs_list) > 0:
    #     zs = [{'sdt': x.bis[0].sdt, 'edt': x.bis[-1].edt, 'zd': x.zd, 'zg': x.zg} for x in c.zs_list]
    # else:
    #     zs = None
    # zs = zs
    # chart = kline_pro_ex(kline, bi=bi, fx=fx, zs=zs, bs=bs, width="1400px", height='580px',
    #                   title=f"{strategy.__name__} {bg.symbol} 交易回放")
    # reply_strategy_path = os.path.join(res_path, f"replay_{strategy.__name__}@{bg.symbol}.html")
    # chart.render(reply_strategy_path)
    # user_log.info("save reply_strategy_path: {}".format(reply_strategy_path))

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
