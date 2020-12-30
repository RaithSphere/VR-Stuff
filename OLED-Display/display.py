import json
import urllib.request
from PIL import Image, ImageFont
from PIL import ImageDraw
from luma.core.interface.serial import spi
from luma.oled.device import ssd1322
from time import sleep

serial = spi(device=0, port=0)
device = ssd1322(serial)
frameSize = (256, 64)
apiurl = "https://www.neosvr-api.com/api/stats/onlineUserStats"


def main():
    while True:
        image = Image.new('RGBA', frameSize, 'white')
        font = ImageFont.truetype("SFSquareHead.ttf", 12, encoding="unic")
        font2 = ImageFont.truetype("OBLIVIOUSFONT.TTF", 10, encoding="unic")
        draw = ImageDraw.Draw(image)

        draw.rectangle([(1, 1), (frameSize[0] - 2, frameSize[1] - 2)], 'black', 'white')

        filenames = [['neos.png', 7, 6]]

        for filename in filenames:
            image_clip = Image.open(filename[0])
            c_x = filename[1]
            c_y = filename[2]
            image.alpha_composite(image_clip, (c_x, c_y))

        draw.text((62, 4), 'NeosVR Online Status', fill='white', font=font)
        with urllib.request.urlopen(apiurl) as url:
            data = json.loads(url.read().decode())
            draw.text((65, 15), "Online Users : %s/%s" % (data['registeredUserCount'], data['instanceCount']),
                      fill="white", font=font2)
            draw.text((65, 26), "VR Users : %s" % (data['vrUserCount']), fill="white", font=font2)
            draw.text((65, 37), "Desktop Users : %s" % (data['screenUserCount']), fill="white", font=font2)
            draw.text((65, 48), "Active Sessions : %s" % (data['activePublicSessionCount']), fill="white", font=font2)

        image_rgb = image.convert('RGB')
        device.display(image_rgb)
        sleep(15)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
