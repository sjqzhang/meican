# MeiCan 美餐
[![PyPI](https://img.shields.io/pypi/v/meican.svg)](https://pypi.python.org/pypi/meican)
[![Build](https://github.com/LKI/meican/workflows/Build/badge.svg)](https://github.com/LKI/meican)

> 同时支持 Python 3.6+ 与命令行调用的美餐点餐非官方库

山上的朋友！
树上的朋友！
有选择困难症的朋友！
每周都忘记点饭的朋友！
每天都想点同一个套餐的朋友！

:ghost: 懒人们！
快快解放双手来点美餐吧~


## 背景

最开始是因为[我司](https://www.lagou.com/gongsi/j86312.html)用的美餐服务，
所以就写了个命令行脚本内部点餐用。

后来发现其实大家会有自己动手实现点单逻辑的需求，
就做成了这个开源库啦。


## 安装

通过pip:

```bash
pip install meican
```


## 代码调用

```python
from meican import MeiCan, MeiCanLoginFail, NoOrderAvailable

try:
    meican = MeiCan('username@domain', 'hunter2')  # login
    dishes = meican.list_dishes()
    if any(dish for dish in dishes if dish.name == '香酥鸡腿'):
        print('今天有香酥鸡腿 :happy:')
    else:
        print('今天没有香酥鸡腿 :sad:')
except NoOrderAvailable:
    print('今天没有开放点餐')
except MeiCanLoginFail:
    print('用户名或者密码不正确')
```


## 自动点餐示例
```python
#!/usr/bin/env pytho
# -*- coding:utf-8 -*-
import random
from meican import MeiCan, MeiCanLoginFail, NoOrderAvailable
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
    except Exception as er:
        print(er)


def get_tab_dishes(tab_keyword):
    global mc
    tab = None
    for _tab in mc.tabs:
        if str(_tab.title).find(str(tab_keyword)) != -1:
            tab = _tab
            break
    dishes = mc.list_dishes(tab)
    return dishes


if __name__ == '__main__':
    initialize_meican()
    # order_random('楼层关键字','套餐关键字')
    order_random('26', '不辣')

```

```golang
package main

import (
	"fmt"
	"github.com/robfig/cron"
	"os/exec"
)

func order() {

	cmd := exec.Command("/usr/local/bin/meican")
	output, err := cmd.Output()
	if err != nil {
		fmt.Println(err)
	} else {
		fmt.Println(string(output))
	}

}

func main() {
	c := cron.New()
	spec := "50 11 * * MON-FRI"
	_, err := c.AddFunc(spec, func() {
		go order()
	})
	if err != nil {
		panic(err)
	}
	c.Start()

	select {}
}
```

## 命令行调用

```bash
meican  # 查询下次点啥菜
meican -o 香酥  # 点包含 香酥 关键字的菜，比如香酥鸡腿
```


## 贡献

不论是任何疑问、想要的功能~~还是想吃的套餐~~都欢迎[直接提 issue](https://github.com/LKI/meican/issues/new)

假如你们公司是用熙香点餐的，
[隔壁也有熙香的库噢~](https://github.com/LKI/xixiang)

:wink: 欢迎各种 PR


## 协议

宽松的 [MIT](https://github.com/LKI/meican/blob/master/LICENSE) 协议：

- ✔ 支持各种改写
- ✔ 支持你把代码作者都改成自己
- ✖ 不支持每天中午免费吃西贝莜面村
- ✖ 也不支持点大羊腿、掌中宝
