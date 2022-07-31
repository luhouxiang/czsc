# -*- coding: utf-8 -*-
"""
author: luhx
create_dt: 2022/7/31 17:52
describe: 提供一些策略的编写案例

以 trader_ 开头的是择时交易策略案例
"""
from czsc import signals
from czsc.objects import Freq, Operate, Signal, Factor, Event
from collections import OrderedDict
from czsc.traders import CzscAdvancedTrader
from czsc.objects import PositionLong, PositionShort, RawBar


def trader_standard(symbol, T0=False, min_interval=3600*4):
    """择时策略编写的一些标准说明

    输入参数：
    1. symbol 是必须要有的，且放在第一个位置，策略初始化过程指明交易哪个标的
    2. 除此之外的一些策略层面的参数可选，比如 T0，min_interval 等

    :param symbol: 择时策略初始化的必须参数，指明交易哪个标的
    :param T0:
    :param min_interval:
    :return:
    """
    pass


def trader_example_1d(symbol, T0=False, min_interval=3600 * 4):
    """A股市场择时策略样例，支持按交易标的独立设置参数

    :param symbol:
    :param T0: 是否允许T0交易
    :param min_interval: 最小开仓时间间隔，单位：秒
    :return:
    """
    def get_signals(cat: CzscAdvancedTrader) -> OrderedDict:
        s = OrderedDict({"symbol": cat.symbol, "dt": cat.end_dt, "close": cat.latest_price})
        s.update(signals.pos.get_s_long01(cat, th=100))
        s.update(signals.pos.get_s_long02(cat, th=100))
        s.update(signals.pos.get_s_long05(cat, span='月', th=500))

        for _, c in cat.kas.items():
            s.update(signals.bxt.get_s_d0_bi(c))
            s.update(signals.bxt.get_s_base_xt(c, 1))
            s.update(signals.bxt.get_s_like_bs(c, 1))
            if c.freq in [Freq.D, Freq.W]:
                s.update(signals.other.get_s_zdt(c, di=1))
                s.update(signals.other.get_s_op_time_span(c, op='开多', time_span=('13:00', '14:50')))
                s.update(signals.other.get_s_op_time_span(c, op='平多', time_span=('09:35', '14:50')))
            if c.freq in [Freq.D, Freq.W]:
                s.update(signals.ta.get_s_macd(c, di=1))
        return s

    # 定义多头持仓对象和交易事件
    long_pos = PositionLong(symbol, hold_long_a=1, hold_long_b=1, hold_long_c=1,
                            T0=T0, long_min_interval=min_interval)

    long_events = [
        Event(name="开多", operate=Operate.LO, factors=[
            # Factor(name="七笔", signals_all=[
            #     # Signal("开多时间范围_13:00_14:50_是_任意_任意_0"),
            #     # Signal("30分钟_倒1K_ZDT_非涨跌停_任意_任意_0"),
            #     # Signal("30分钟_倒1K_MACD多空_多头_任意_任意_0"),
            #     Signal("5分钟_倒1笔_基础形态_类三买_七笔_任意_0"),
            #     # Signal("30分钟_倒0笔_方向_向上_任意_任意_0"),
            #     # Signal("30分钟_倒0笔_长度_5根K线以下_任意_任意_0"),
            # ]),
            Factor(name="五笔", signals_all=[
                # Signal("开多时间范围_13:00_14:50_是_任意_任意_0"),
                # Signal("30分钟_倒1K_ZDT_非涨跌停_任意_任意_0"),
                # Signal("30分钟_倒1K_MACD多空_多头_任意_任意_0"),
                Signal("日线_倒1笔_基础形态_类三买_五笔_任意_0"),
                # Signal("30分钟_倒0笔_方向_向上_任意_任意_0"),
                # Signal("30分钟_倒0笔_长度_5根K线以下_任意_任意_0"),
            ]),
        ]),

        Event(name="平多", operate=Operate.LE, factors=[
            Factor(name="持有资金", signals_all=[
                # Signal("平多时间范围_09:35_14:50_是_任意_任意_0"),
                Signal("日线_倒1K_ZDT_非涨跌停_任意_任意_0"),
            ], signals_not=[
                # Signal("30分钟_倒0笔_方向_向上_任意_任意_0"),
                # Signal("30分钟_倒1K_MACD多空_多头_任意_任意_0"),
            ]),
        ]),
    ]

    tactic = {
        "base_freq": '日线',
        "freqs": ['日线', '周线', '月线'],  # '日线', '周线', '月线'
        "get_signals": get_signals,
        "signals_n": 0,

        "long_pos": long_pos,
        "long_events": long_events,

        # 空头策略不进行定义，也就是不做空头交易
        "short_pos": None,
        "short_events": None,
    }

    return tactic

