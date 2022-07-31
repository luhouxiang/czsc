# -*- coding: utf-8 -*-
"""
date: 2022-7-23 21:45
@author: luhx
@describe: 读取5分钟数据
"""
import datetime
import pandas as pd
from typing import List
from czsc.objects import RawBar,Freq
def read_5m_data(path, symbol) -> List[RawBar]:
    """
    :param kline:
    :return: 转换好的K线数据
    """
    # path = r"D:\new_jyplug\T0002\export\5m"
    # symbol = "600000.SH"
    file_name = path + "/" + symbol.split(".")[1] + "#" + symbol.split(".")[0] + ".txt"
    df = pd.read_csv(file_name, encoding="gbk", header=1, sep='\t',
                     names=["date", "time", "open", "high", "low", "close", "volume", "amount"])
    df.drop([len(df)-1], inplace=True)
    bars = []
    for index, row in df.iterrows():
        # 将每一根K线转换成 RawBar 对象
        minutes = int(row['time']/100)*60 + int(row['time']%100)
        dt =pd.to_datetime(row["date"]) + datetime.timedelta(minutes=minutes)
        bar = RawBar(symbol=symbol, dt= dt,
                     id=index, freq=Freq.F5, open=row['open'], close=row['close'],
                     high=row['high'], low=row['low'],
                     vol=row['volume'],          # 成交量，单位：股
                     amount=row['amount'],    # 成交额，单位：元
                     )
        bars.append(bar)
    return bars


def read_1d_data(path, symbol) -> List[RawBar]:
    """
    :param kline:
    :return: 转换好的K线数据
    """
    # path = r"D:\new_jyplug\T0002\export\5m"
    # symbol = "600000.SH"
    file_name = path + "/" + symbol.split(".")[1] + "#" + symbol.split(".")[0] + ".txt"
    df = pd.read_csv(file_name, encoding="gbk", header=1, sep='\t',
                     names=["date", "open", "high", "low", "close", "volume", "amount"])
    df.drop([len(df)-1], inplace=True)
    bars = []
    for index, row in df.iterrows():
        # 将每一根K线转换成 RawBar 对象
        dt =pd.to_datetime(row["date"])
        bar = RawBar(symbol=symbol, dt= dt,
                     id=index, freq=Freq.D, open=row['open'], close=row['close'],
                     high=row['high'], low=row['low'],
                     vol=row['volume'],          # 成交量，单位：股
                     amount=row['amount'],    # 成交额，单位：元
                     )
        bars.append(bar)
    return bars