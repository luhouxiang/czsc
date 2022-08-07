from typing import List, Tuple
import datetime
import requests
import json
import copy
from czsc.utils.user_logbook import user_log as logger
from czsc.objects import RawBar, Freq


class KLine():
    def __init__(self,time=0,open=0,high=0,low=0,close=0,volume=0,oi=0,instrument=""):
        self.time = time
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume
        self.oi = oi
        self.instrument = instrument    #合约号
        self.pls = 0                    #上一个多空信号保存
        self.ls = 0                     #多空信号保存
        self.bt = 0                     #为了画图，给出的底和顶指示。-2是底 2是顶
        self.want = 0                   #期望值，根据未来情况，期望输出的信号

def load_kline(code, period="1m", limit=240000, e_time="", s_time="") -> Tuple[
    List["Kline"], any]:  # 通过接口获取k线数据，增加基础计算
    param = {
        "user": "100000",
        "token": "luhouxiang",
        "code": code,
        "period": period,
        "s_time": s_time,  # 开始时间可以不给出
        "e_time": e_time,  # 结束时间缺省是当前时间
        "count": limit  # 数量在只有结束时间的时候有效，建议不为0
    }
    headers = {'Content-Type': 'application/json;charset=UTF-8', 'Connection': 'keep-alive'}
    logger.info(F"request_kline:param: {json.dumps(param, indent=4)}")
    try:
        url = 'http://192.168.1.100:8086/api/hqqh/kline'
        r = requests.request('POST', url, json=param, headers=headers)
    except Exception as exception:
        logger.error(str(exception))
        try:
            url = 'http://192.168.1.101:8086/api/hqqh/kline'
            r = requests.request('POST', url, json=param, headers=headers)
        except Exception as exception:
            logger.error(str(exception))
    logger.info(F"request_kline:status: {r.status_code},[POST]:{url}")
    j = r.json()

    lists = j["result"]['lists'] if j.get('err_code', -1) == 0 else []

    klines = [KLine(d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7]) for d in lists]

    bars = []
    for index,k in enumerate(klines):
        bar = RawBar(symbol=k.instrument, dt=k.time,
                     id=index, freq=Freq.F30, open=k.open, close=k.close,
                     high=k.high, low=k.low,
                     vol=k.volume,  # 成交量，单位：股
                     amount=k.volume*k.close,  # 成交额，单位：元
                     )
        bars.append(bar)

    logger.info(F"get_remote_kline: {str(datetime.datetime.fromtimestamp(klines[0].time))}"
                F" --> {str(datetime.datetime.fromtimestamp(klines[-1].time))} end.")
    return klines


def get_kline_data(code="rbL9", period="5m", s_time="2022-05-25 22:30:00", e_time="2022-06-06 22:00:00", limit=5000):
    klines = load_kline(code=code, period=period, s_time=s_time, e_time=e_time, limit=limit)
    return klines