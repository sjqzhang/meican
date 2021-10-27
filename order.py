#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import random

from meican import MeiCan
from meican.models import TabStatus
from meican.settings import *

mc = MeiCan


def initialize_meican():
    global mc
    settings = MeiCanSetting()
    settings.load_credentials()
    mc = MeiCan(settings.username, settings.password)
    mc.load_tabs()
    return mc


def order_random(tab_keyword, keyword):
    try:
        dishes = get_tab_dishes(tab_keyword)
        if keyword != "":
            dishes2 = list(filter(lambda d: str(d.name).find(keyword) != -1, dishes))
            if len(dishes2) > 0:
                dishes = dishes2
        rid = random.randint(0, len(dishes) - 1)
        mc.order(dishes[rid])
        print('done')
    except Exception as er:
        print(er)


def get_tab_dishes(tab_keyword):
    global mc
    tab = None
    for _tab in mc.tabs:
        if str(_tab.title).find(str(tab_keyword)) != -1 and _tab.status != TabStatus.CLOSED:
            tab = _tab
            break
    dishes = mc.list_dishes(tab)
    return dishes


if __name__ == '__main__':
    initialize_meican()
    # order_random('楼层关键字','套餐关键字')
    order_random('26', '不辣')
