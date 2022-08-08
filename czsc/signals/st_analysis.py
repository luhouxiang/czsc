# -*- coding: utf-8 -*-
"""
@author: luhx
@date: 2022-8-3 22:06
@describe: 结构形态分析
"""

from typing import List, Union
from collections import OrderedDict
from czsc import analyze
from ..objects import Direction, BI, FakeBI, Signal,RawBar,WeiBI
from ..enum import Freq
from ..utils.ta import RSQ


def get_abc(ks: List[RawBar],N=5) -> List[WeiBI]:
    hs,ls=[x.high for x in ks],[x.low for x in ks]
    sel = 0
    M = len(ks)
    tbs = []
    for i in range(M):
        mx = max(hs[max(i-N,0):min(i+N,M)])
        mn = min(ls[max(i-N,0):min(i+N,M)])
        if sel <= 0:# 找到底后找顶
            if hs[i] == mx:
                if sel == 0:tbs.append([0,-1])
                tbs.append([i,1])  #顶
                sel = 1
            if tbs and ls[i] == mn and ls[i] < ls[tbs[-1][0]]:# 找到更低的底
                tbs[-1][0] = i
        if sel >= 0:
            if ls[i] == mn:
                if sel == 0:tbs.append([0,1])
                tbs.append([i,-1])
                sel = -1
            if tbs and hs[i] == mx and hs[i] > hs[tbs[-1][0]]:#
                tbs[-1][0] = i
    bi_list: List[WeiBI] = []
    for i in range(len(tbs)-1):
        line: List[RawBar] = []
        for j in range(tbs[i][0], tbs[i+1][0]+1):
            line.append(ks[j])
        bi_list.append(WeiBI(symbol=ks[0].symbol, direction=Direction.Up if tbs[i][1] == -1 else Direction.Down, bars=line))
    return bi_list

def feel_five_bi(c: analyze.CZSC, bis: List[Union[BI, FakeBI]], freq: Freq, di: int = 1) -> Signal:
    """感知五笔形态

    :param freq: K线周期，也可以称为级别
    :param bis: 由远及近的五笔
    :param di: 最近一笔为倒数第i笔
    :return:
    """
    di_name = f"倒{di}笔"
    v = Signal(k1=freq.value, k2=di_name, k3='攻击形态', v1='其他', v2='其他', v3='其他')

    # if len(bis) != 5:
    #     return v
    #
    # bi1, bi2, bi3, bi4, bi5 = bis
    # if not (bi1.direction == bi3.direction == bi5.direction):
    #     print(f"1,3,5 的 direction 不一致，无法识别五段形态；{bi1}{bi3}{bi5}")
    #     return v

    # direction = bi1.direction
    # # max_high = max([x.high for x in bis])
    # # min_low = min([x.low for x in bis])
    # assert direction in [Direction.Down, Direction.Up], "direction 的取值错误"
    if c.zs_list:   # 存在中枢
        if c.bars_input[-1].low < c.zs_list[-1].zg: # 当前已进入中枢，退出
            return v
        # if c.bars_input[-1].low > c.zs_list[-1].zg and c.bars_input[-30] < c.zs_list[-1].zg:    # 不应离开中枢太久，最多不超过30个周期
        try:
            abc_list = get_abc(c.bars_input[-45:], N=6)
            c.wbi_list = abc_list
        except Exception as e:
            print(e)
        if abc_list[-1].direction != Direction.Down:
            return v
        try:
            if abc_list[-2].low > c.zs_list[-1].zg:
                return v
        except Exception as e:
            print(e)
        if abc_list[-3].high > abc_list[-2].high:   # A段的最高 > B段的最高（即B段的最高不是最高）
            return v
        if (abc_list[-2].high - abc_list[-2].low)/abc_list[-2].low > 0.40:  # 涨幅大于40%,直接忽略
            return v
        if abc_list[-1].low < c.zs_list[-1].zg:  # C段的最低低于中枢的上沿
            return v

        if len(abc_list[-1].bars) > 10: # C段的调整》10个交易日，久盘必跌
            return v

        if c.bars_input[-1].id - abc_list[-1].bars[-1].id >= 4:
            return v

        return Signal(k1=freq.value, k2=di_name, k3='攻击形态', v1='类三买', v2='五笔')

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

    for v in [feel_five_bi(c, five_bi, freq, di)]:
        if "其他" not in v.value:
            s[v.key] = v.value
    return s