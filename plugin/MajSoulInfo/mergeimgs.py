from PIL import Image as IMG


def mergeimgs(urls: list, senderid: int) -> IMG:
    imgback = IMG.new("RGBA", (1020, 420), (255, 255, 255, 1))
    for i in range(10):
        img = IMG.open(f'./plugin/MajSoulInfo/{urls[i]}').convert("RGBA")
        size = img.size

        if size[0] > 180 or size[1] > 180:
            img = img.resize((180, 180), IMG.ANTIALIAS)
        posx = 20 + (i % 5) * 200
        posy = 20 + (i // 5) * 200
        imgback.paste(img, (posx, posy, posx + img.size[0], posy + img.size[1]))
        imgback.save(fp=f"./images/MajSoulInfo/{senderid}.png")
    return imgback
