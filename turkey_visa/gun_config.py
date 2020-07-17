import os
import gevent.monkey
gevent.monkey.patch_all()

import multiprocessing

debug = False
loglevel = 'debug'
bind = '0.0.0.0:5000'
pidfile = 'log/gunicorn.pid'
logfile = 'log/debug.log'
threads=300
# 启动的进程数
workers = multiprocessing.cpu_count() * 2 + 1
# workers = 4
worker_class = 'gevent'

x_forwarded_for_header = 'X-FORWARDED-FOR'
