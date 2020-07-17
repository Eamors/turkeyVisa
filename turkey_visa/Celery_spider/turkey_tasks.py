# -*- coding:utf-8 -*-
# Author: Eamor
# Time: 2020/6/29 10:26


from Celery_spider import turkey_app


@turkey_app.task
def turkey_spider(spider_name, params):
    pass