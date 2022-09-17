"""
:Author:  jianwei569
:Create:  2022/9/17 2:13
:Update: /
:Describe: 今天吃什么
:Version: 0.0.1
"""
import re
from mirai import GroupMessage, Plain
from core import bot, config, bot_cfg
from utils.MessageChainBuilder import messagechain_builder
import random
import yaml


def eating():
    with open(r'./config/WhatToEatToday/default_eating.yml', 'r', encoding='utf-8') as f:
    #with open(r'default_eating.yml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        foods = config['basic_food']
    food_index = random.randint(0, 70) * 5
    food = foods[food_index]
    #print(food)
    return food

def drinking():
    with open(r'./config/WhatToEatToday/default_drinks.yml', 'r', encoding='utf-8') as f:
    #with open(r'default_drinks.yml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        all_items = config['All_items']
        all_shop_items = all_items['all_shop_items']  
    shop_index = random.randint(0, 5)
    drink_length = len(all_shop_items[shop_index]['shop_items'])
    shop_name = all_shop_items[shop_index]['shop_name']
    drink_index = random.randint(0, drink_length) - 1
    drink = all_shop_items[shop_index]['shop_items'][drink_index]
    shop_drink = shop_name + '的' + drink
    #print(shop_drink)
    return shop_drink

@bot.on(GroupMessage)  # 当群聊事件发生时
async def what2eat(event: GroupMessage):
    msg = "".join(map(str, event.message_chain[Plain])) # 获取消息的文本内容
    m = re.match(fr"^.*吃什么.*", msg.strip()) # 用正则进行匹配指令
    if m:
        food = eating()
        await bot.send(event, messagechain_builder(at=event.sender.id,text=f"今天吃" + food))        

@bot.on(GroupMessage)  # 当群聊事件发生时
async def what2drink(event: GroupMessage):
    msg = "".join(map(str, event.message_chain[Plain])) # 获取消息的文本内容
    m = re.match(fr"^.*喝什么.*", msg.strip()) # 用正则进行匹配指令
    if m:
        drink = drinking()
        await bot.send(event, messagechain_builder(at=event.sender.id,text=f"今天喝" + drink))  