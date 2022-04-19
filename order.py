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


def order_random(tab_keyword, expect_keyword,unexpect_keyword):
    try:
        dishes = get_tab_dishes(tab_keyword)
        dishes1=set()
        dishes2=set()
        if expect_keyword != "":
            kws=expect_keyword.split('|')
            for kw in kws:
                if kw=='':
                    continue
                for dish in dishes:
                    if kw in dish.name:
                        dishes1.add(dish)
        if unexpect_keyword != "":
            kws=unexpect_keyword.split('|')
            for kw in kws:
                if kw=='':
                    continue
                for dish in dishes:
                    if kw not in dish.name:
                        dishes2.add(dish)
                # dishes2 = list(filter(lambda d: str(d.name).find(kw) != -1, dishes))
        dishes2=dishes1.intersection(dishes2)
        if len(dishes2) > 0:
            dishes = list(dishes2)
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
    order_random('26', '不辣','沙拉')
