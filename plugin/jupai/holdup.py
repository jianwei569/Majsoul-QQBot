import re

from PIL import ImageFont, ImageDraw, Image as IMG
import os
import random
import numpy as np
from mirai import GroupMessage, Plain, MessageChain, Image

from core import bot, commandpre, commands_map

if not os.path.exists("./images/jupai"):
    os.mkdir("./images/jupai")

__all__ = ['jupai']

def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])

    A = np.matrix(matrix, dtype=np.float)
    B = np.array(pb).reshape(8)

    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)


def imgoutput(senderid: int, textMessage='拉克丝真可爱'):
    print(f"开始创建图片，内容为:{textMessage}")
    try:
        font = ImageFont.truetype('./plugin/jupai/fonts/shs_and_emoji.ttf', 40)
        text = textMessage[0:40]
        pic_list = []
        for i in text:
            width, height = font.getsize(i)
            back = random.choice(os.listdir('./plugin/jupai/jupai'))
            path = f'./plugin/jupai/jupai/{back}'
            img = IMG.open(path)
            # img = img.rotate(23, resample=IMG.BICUBIC, expand=True)
            word = IMG.new('RGBA', (63, 42), (255, 255, 255, 1))
            draw = ImageDraw.Draw(word)
            draw.text((20 - width / 2, 20 - height / 2), i, font=font, fill=(0, 0, 0))
            # word = word.resize((30, 40), IMG.ANTIALIAS)
            # word = word.rotate(-30, resample=IMG.BICUBIC, expand=True)
            coeffs = find_coeffs([(29, 0), (63, 14), (34, 42), (0, 28)], [(0, 0), (63, 0), (63, 42), (0, 42)])
            word = word.transform((63, 42), IMG.PERSPECTIVE, coeffs, IMG.BICUBIC)
            img.paste(word, (14, 9), word)
            pic_list.append(img)
        text_num = len(pic_list) - 1
        lines = int(text_num / 8)
        last = text_num % 8
        if lines == 0:
            x = last * 55 + 80
            y = last * 21 + 165
        else:
            x = lines * 45 + 465
            y = max(lines * 45 + last * 21 + 165, (lines - 1) * 45 + 312)
        out = IMG.new('RGB', (x, y), (255, 255, 255))
        k = 0
        for i in pic_list:
            no_x = k % 8
            no_y = int(k / 8)
            out.paste(i, (no_x * 55 + (lines - no_y) * 45, no_y * 45 + no_x * 21), i)
            k += 1
        # out = out.rotate(-23, resample=IMG.BICUBIC, expand=True)
        out.save(f"./images/jupai/{senderid}.png")
    except OSError:
        print(OSError)




@bot.on(GroupMessage)
async def jupai(event: GroupMessage):
    """创建举牌文字"""
    msg = "".join(map(str, event.message_chain[Plain]))
    m = re.match(
        fr'''^{commandpre}{commands_map['jupai']['jupai']}''', msg.strip())
    if m:

        if len(m.group(1)) > 40:
            await bot.send(event, "最多支持做40个字的举牌哦~")
        imgoutput(event.sender.id, (m.group(1)))
        message_chain = MessageChain([
            await Image.from_local(f'./images/jupai/{event.sender.id}.png')
        ])
        await bot.send(event, message_chain)
