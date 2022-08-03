# -*- coding: utf-8 -*-
"""
@author: luhx
@date: 2022-8-3 22:06
@describe: 结构形态分析
"""

from typing import List, Union
from collections import OrderedDict
from czsc import analyze
from ..objects import Direction, BI, FakeBI, Signal
from ..enum import Freq
from ..utils.ta import RSQ


def feel_five_bi(bis: List[Union[BI, FakeBI]], freq: Freq, di: int = 1) -> Signal:
    """感知五笔形态

    :param freq: K线周期，也可以称为级别
    :param bis: 由远及近的五笔
    :param di: 最近一笔为倒数第i笔
    :return:
    """
    di_name = f"倒{di}笔"
    v = Signal(k1=freq.value, k2=di_name, k3='攻击形态', v1='其他', v2='其他', v3='其他')

    if len(bis) != 5:
        return v

    bi1, bi2, bi3, bi4, bi5 = bis
    if not (bi1.direction == bi3.direction == bi5.direction):
        print(f"1,3,5 的 direction 不一致，无法识别五段形态；{bi1}{bi3}{bi5}")
        return v

    direction = bi1.direction
    max_high = max([x.high for x in bis])
    min_low = min([x.low for x in bis])
    assert direction in [Direction.Down, Direction.Up], "direction 的取值错误"

    if direction == Direction.Down:
        # aAb式底背驰
        if min(bi2.high, bi4.high) > max(bi2.low, bi4.low) and max_high == bi1.high and bi5.power < bi1.power:
            if (min_low == bi3.low and bi5.low < bi1.low) or (min_low == bi5.low):
                return Signal(k1=freq.value, k2=di_name, k3='攻击形态', v1='底背驰', v2='五笔aAb式')

        # 类趋势底背驰
        if max_high == bi1.high and min_low == bi5.low and bi4.high < bi2.low and bi5.power < max(bi3.power, bi1.power):
            return Signal(k1=freq.value, k2=di_name, k3='攻击形态', v1='底背驰', v2='五笔类趋势')

        # 上颈线突破
        if (min_low == bi1.low and bi5.high > min(bi1.high, bi2.high) > bi5.low > bi1.low) \
                or (min_low == bi3.low and bi5.high > bi3.high > bi5.low > bi3.low):
            return Signal(k1=freq.value, k2=di_name, k3='攻击形态', v1='上颈线突破', v2='五笔')

        # 五笔三买，要求bi5.high是最高点
        if max_high == bi5.high > bi5.low > max(bi1.high, bi3.high) \
                > min(bi1.high, bi3.high) > max(bi1.low, bi3.low) > min_low:
            return Signal(k1=freq.value, k2=di_name, k3='攻击形态', v1='类三买', v2='五笔')

    if direction == Direction.Up:
        # aAb式类一卖
        if min(bi2.high, bi4.high) > max(bi2.low, bi4.low) and min_low == bi1.low and bi5.power < bi1.power:
            if (max_high == bi3.high and bi5.high > bi1.high) or (max_high == bi5.high):
                return Signal(k1=freq.value, k2=di_name, k3='攻击形态', v1='顶背驰', v2='五笔aAb式')

        # 类趋势类一卖
        if min_low == bi1.low and max_high == bi5.high and bi5.power < max(bi1.power, bi3.power) and bi4.low > bi2.high:
            return Signal(k1=freq.value, k2=di_name, k3='攻击形态', v1='顶背驰', v2='五笔类趋势')

        # 下颈线突破
        if (max_high == bi1.high and bi5.low < max(bi1.low, bi2.low) < bi5.high < max_high) \
                or (max_high == bi3.high and bi5.low < bi3.low < bi5.high < max_high):
            return Signal(k1=freq.value, k2=di_name, k3='攻击形态', v1='下颈线突破', v2='五笔')

        # 五笔三卖，要求bi5.low是最低点
        if min_low == bi5.low < bi5.high < min(bi1.low, bi3.low) \
                < max(bi1.low, bi3.low) < min(bi1.high, bi3.high) < max_high:
            return Signal(k1=freq.value, k2=di_name, k3='攻击形态', v1='类三卖', v2='五笔')

    return v


def get_s_attack_xt(c: analyze.CZSC, di: int = 1) -> OrderedDict:
    """倒数第i笔的攻击形态信号

    :param c: CZSC 对象
    :param di: 最近一笔为倒数第i笔
    :return: 信号字典
    """
    assert di >= 1

    bis = c.finished_bis
    freq: Freq = c.freq
    s = OrderedDict()
    v = Signal(k1=str(freq.value), k2=f"倒{di}笔", k3="攻击形态", v1="其他", v2='其他', v3='其他')
    s[v.key] = v.value

    if not bis:
        return s

    if di == 1:
        five_bi = bis[-5:]
        seven_bi = bis[-7:]
    else:
        five_bi = bis[-5 - di + 1: -di + 1]
        seven_bi = bis[-7 - di + 1: -di + 1]

    for v in [feel_five_bi(five_bi, freq, di)]:
        if "其他" not in v.value:
            s[v.key] = v.value
    return s