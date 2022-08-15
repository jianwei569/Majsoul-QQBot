import re
import aiohttp
from mirai import GroupMessage, MessageChain, Plain, Image

# from plugin import bot, config
from core import bot,config

last_bvid = {}

settings = config['settings']
silencegroup = config['silencegroup']

@bot.on(GroupMessage)
# 哔哩哔哩解析
async def bili_resolve(event: GroupMessage):
    if not settings['silence']:
        if event.group.id not in silencegroup:
            global last_bvid
            text = str(event.message_chain.as_mirai_code)
            text = text.replace('\\n', '').replace('\\', '')
            if 'b23.tv/' in text:
                b23_url = re.findall('b23.tv/[A-Za-z0-9]+', text)[0]
                url = f'https://{b23_url}'
                async with aiohttp.ClientSession() as session:
                    async with session.get(url=url,allow_redirects=False) as resp:
                        text = await resp.text()
            if 'BV' in text:
                bvid = re.findall('BV[A-Za-z0-9]+', text)[0]
            else:
                return
            if event.group.id in last_bvid.keys():
                if bvid == last_bvid[event.group.id]:
                    return
            # if event.message_chain.has("www.bilibili.com/video"):
            #     bvid = re.findall('BV[A-Za-z0-9]',"".join(map(str, event.message_chain[Plain])).strip())[0]
            last_bvid[event.group.id] = bvid
            bv_url = f'http://api.bilibili.com/x/web-interface/view?bvid={bvid}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url=bv_url) as resp:
                    data = await resp.json()
            if data['code'] != 0:
                return
            img_url = data['data']['pic']
            author = data['data']['owner']['name']
            title = data['data']['title']
            msg = f'{bvid}\nUP主:{author}\n标题:{title}'
            '''if event.message_chain[1].type == 'App':
                app = event.message_chain[1].as_json()
                url = app['meta']['detail_1']['preview']
                img_url = f'http://{url}'''
            message_chain = MessageChain(
                [Image(url=img_url), Plain(text=msg)])
            return await bot.send(event, message_chain)