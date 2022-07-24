# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename:user_logbook.py
import os

import logbook
from logbook import Logger, TimedRotatingFileHandler
from logbook.more import ColorizedStderrHandler

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.00"


def user_handler_log_formatter(record, handler):
    log = "[{dt}][{level}][{filename}][{func_name}][{lineno}] {msg}".format(
        dt=record.time,
        level=record.level_name,  # 日志等级
        filename=os.path.split(record.filename)[-1],  # 文件名
        func_name=record.func_name,  # 函数名
        lineno=record.lineno,  # 行号
        msg=record.message,  # 日志内容
    )
    return log


# 打印到屏幕句柄
user_std_handler = ColorizedStderrHandler(bubble=True)
user_std_handler.formatter = user_handler_log_formatter
# 日志路径，在主工程下生成log目录
LOG_DIR = os.path.join('log')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 打印到文件句柄
user_file_handler = TimedRotatingFileHandler(
    os.path.join(LOG_DIR, '%s.log' % 'server'), date_format='%Y%m%d', bubble=True)
user_file_handler.formatter = user_handler_log_formatter

system_file_handler = TimedRotatingFileHandler(
    os.path.join(LOG_DIR, '%s.log' % 'system'), date_format='%Y%m%d', bubble=True)
system_file_handler.formatter = user_handler_log_formatter

# 用户代码logger日志
user_log = Logger("user_log")

system_log = Logger("system_log")


def init_logger():
    logbook.set_datetime_format("local")
    user_log.handlers = []
    user_log.handlers.append(user_std_handler)
    user_log.handlers.append(user_file_handler)
    system_log.handlers = [system_file_handler]
    err_log.handlers = []
    err_log.handlers.append(user_std_handler2)


def user_handler_log_formatter2(record, handler):
    record.msg = str(record.msg).replace('%s', '{}')
    log = "[{dt}][{level}][{filename}:{lineno}:{func_name}] {msg}".format(
        dt=record.time,
        level=record.level_name,  # 日志等级
        filename=os.path.split(record.filename)[-1],  # 文件名
        func_name=record.func_name,  # 函数名
        lineno=record.lineno,  # 行号
        msg=record.message,  # 日志内容
    )
    # print('-----------------')
    # print(record)
    # print(record.to_dict())
    # print(record.message)
    # print('-----------------')
    return log


# 错误记录logger日志
err_log = Logger('err_log')

# 打印到屏幕句柄
user_std_handler2 = ColorizedStderrHandler(bubble=True)
user_std_handler2.formatter = user_handler_log_formatter2


def init_logger_postfix(postfix: str, backup_count=15):
    user_log.handlers = []
    user_log.handlers.append(user_std_handler2)

    _user_file_handler = TimedRotatingFileHandler(
        os.path.join(LOG_DIR, 'server.log'), date_format='%Y%m%d', bubble=True, backup_count=backup_count)
    _user_file_handler.formatter = user_handler_log_formatter2
    user_log.handlers.append(_user_file_handler)

    file_handler_postfix = TimedRotatingFileHandler(
        os.path.join(LOG_DIR, 'server-{}.log'.format(postfix)), date_format='%Y%m%d', bubble=True,
        backup_count=backup_count)
    file_handler_postfix.formatter = user_handler_log_formatter2
    user_log.handlers.append(file_handler_postfix)

    err_log.handlers = []
    err_log.handlers.append(user_std_handler2)

    _err_file_handler = TimedRotatingFileHandler(
        os.path.join(LOG_DIR, 'server-err.log'), date_format='%Y%m%d', bubble=True, backup_count=backup_count)
    _err_file_handler.formatter = user_handler_log_formatter2
    err_log.handlers.append(_err_file_handler)

    _err_file_handler_postfix = TimedRotatingFileHandler(
        os.path.join(LOG_DIR, 'server-{}-err.log'.format(postfix)), date_format='%Y%m%d', bubble=True,
        backup_count=backup_count)
    _err_file_handler_postfix.formatter = user_handler_log_formatter2
    err_log.handlers.append(_err_file_handler_postfix)


def init_logger_postfix2(postfix: str, backup_count=15):
    """在目录log下添加子目录存放目志"""
    user_log.handlers = []

    user_log.handlers.append(user_std_handler2)

    _user_file_handler = TimedRotatingFileHandler(
        os.path.join(LOG_DIR, 'server.log'), date_format='%Y%m%d', bubble=True, backup_count=backup_count)
    _user_file_handler.formatter = user_handler_log_formatter2
    user_log.handlers.append(_user_file_handler)

    _LOG_DIR = os.path.join('log/{}'.format(postfix))
    if not os.path.exists(_LOG_DIR):
        os.makedirs(_LOG_DIR)

    _file_handler_postfix = TimedRotatingFileHandler(
        os.path.join(_LOG_DIR, 'server-{}.log'.format(postfix)), date_format='%Y%m%d', bubble=True,
        backup_count=backup_count)
    _file_handler_postfix.formatter = user_handler_log_formatter2
    user_log.handlers.append(_file_handler_postfix)

    err_log.handlers = []
    err_log.handlers.append(user_std_handler2)

    _err_file_handler = TimedRotatingFileHandler(
        os.path.join(LOG_DIR, 'server-err.log'), date_format='%Y%m%d', bubble=True, backup_count=backup_count)
    _err_file_handler.formatter = user_handler_log_formatter2
    err_log.handlers.append(_err_file_handler)

    _err_file_handler_postfix = TimedRotatingFileHandler(
        os.path.join(_LOG_DIR, 'server-{}-err.log'.format(postfix)), date_format='%Y%m%d', bubble=True,
        backup_count=backup_count)
    _err_file_handler_postfix.formatter = user_handler_log_formatter2
    err_log.handlers.append(_err_file_handler_postfix)


def new_timed_rotating_file_handler(parent_dir, file_name, backup_count):
    file_path = os.path.join(parent_dir, file_name)
    handler = TimedRotatingFileHandler(file_path, date_format='%Y%m%d', bubble=True, backup_count=backup_count)
    handler.formatter = user_handler_log_formatter2
    return handler


def init_logger_postfix_v3(parent_dir, postfix, backup_count=15):
    """在目录log下添加子目录存放目志"""
    user_log.handlers = []

    user_log.handlers.append(user_std_handler2)

    root_dir = LOG_DIR
    server_p_file_name = 'server.log'
    server_p_err_file_name = 'server-err.log'
    if parent_dir:
        root_dir = os.path.join(root_dir, parent_dir)
        server_p_file_name = 'server-{}.log'.format(parent_dir)
        server_p_err_file_name = 'server-{}-err.log'.format(parent_dir)

    file_dir = root_dir
    server_file_name = server_p_file_name
    server_err_file_name = server_p_err_file_name
    if postfix:
        file_dir = os.path.join(root_dir, postfix)
        server_file_name = 'server-{}.log'.format(postfix)
        server_err_file_name = 'server-{}-err.log'.format(postfix)

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    _user_file_handler = new_timed_rotating_file_handler(root_dir, server_p_file_name, backup_count)
    user_log.handlers.append(_user_file_handler)

    if root_dir != file_dir:
        _file_handler_postfix = new_timed_rotating_file_handler(file_dir, server_file_name, backup_count)
        user_log.handlers.append(_file_handler_postfix)

    err_log.handlers = []
    err_log.handlers.append(user_std_handler2)

    _err_file_handler = new_timed_rotating_file_handler(root_dir, server_p_err_file_name, backup_count)
    err_log.handlers.append(_err_file_handler)

    if root_dir != file_dir:
        _err_file_handler_postfix = new_timed_rotating_file_handler(file_dir, server_err_file_name.format(postfix),
                                                                    backup_count)
        err_log.handlers.append(_err_file_handler_postfix)

    pass


def init_logger_postfix_only(postfix, backup_count=15):
    """只在目录log下存放日志"""
    root_dir = LOG_DIR
    file_dir = os.path.join(root_dir, postfix)
    server_file_name = 'server-{}.log'.format(postfix)
    server_err_file_name = 'server-{}-err.log'.format(postfix)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    _file_handler_postfix = new_timed_rotating_file_handler(file_dir, server_file_name, backup_count)
    user_log.handlers = [user_std_handler2, _file_handler_postfix]

    _err_file_handler_postfix = \
        new_timed_rotating_file_handler(file_dir, server_err_file_name.format(postfix), backup_count)
    err_log.handlers = [user_std_handler2, _err_file_handler_postfix]


# 初始化日志系统（被默认调用）
init_logger()

if __name__ == '__main__':
    # init_logger_postfix_v3('', '')
    err_log.info('errororororororo')
