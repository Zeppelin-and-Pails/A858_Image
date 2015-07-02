"""
imgur

A package for putting images on imgur

@category   silly
@version    $ID: 1.1.1, 2015-02-19 17:00:00 CST $;
@author     KMR, Jason
@licence    GNU GPL v.3
"""
import re
import pyimgur
from PIL import Image, ImageFont, ImageDraw

class imgur:
    conf = None
    imagePath = None

    def __init__(self, conf):
        self.conf = conf
        self.imagePath = conf['imgPath']

    def makeImg(self, text):
        text = re.sub(r'\s', '', text)
        pixels = len(text) / 6

        xsize = 1
        ysize = 1

        imageRatios = [[16,9],
                       [8,5],
                       [5,4],
                       [5,3],
                       [4,3],
                       [3,2]]

        # check if we can make a square
        if (pixels ** (0.5)) % 1 == 0:
            xsize = pixels ** (0.5)
            ysize = xsize
        else:
            # if not see if it fits another ratio
            for ratio in imageRatios:
                if pixels % ratio[0] == 0 and pixels % ratio[1] == 0:
                    xsize = ratio[0] * ((pixels / (ratio[0] * ratio[1])) ** (0.5))
                    ysize = ratio[1] * ((pixels / (ratio[0] * ratio[1])) ** (0.5))
                    break
            # if it doesn't fit a normal ratio, let's see if we can find one
            if xsize * ysize != pixels:
                for x in range(int(pixels ** (0.5)), (pixels/10), -1):
                    if pixels % x == 0:
                        ysize = x;
                        xsize = pixels / ysize
                        break
            # if we still dont have a ratio let's just do our best (we'll lost a little data but ehh)
            if xsize * ysize != pixels:
                xsize = 5 * ((pixels / 20) ** (0.5))
                ysize = 4 * ((pixels / 20) ** (0.5))

        pix  = self.conf['pixelsize']
        xsize = int(xsize)
        ysize = int(ysize)
        size = (xsize * pix, ysize * pix)
        im   = Image.new('RGB', size )
        draw = ImageDraw.Draw(im)
        p = 0

        for x in range(0, xsize):
                for y in range(0, ysize):
                        r = int( "0x" + text[p+0:p+2], 16 )
                        g = int( "0x" + text[p+2:p+4], 16 )
                        b = int( "0x" + text[p+4:p+6], 16 )
                        p += 6

                        colour = (r, g, b, 255)

                        draw.rectangle(
                            (
                                ((x * pix),(y * pix)),
                                (((x * pix) + pix),
                                (pix + (pix * y)))
                            ),
                            fill=colour
                        )

        im.save(self.conf['imgPath'], 'PNG')
        return im.save(self.conf['imgPath'], 'PNG')

    def uploadImage(self, imageTitle):
        im = pyimgur.Imgur(self.conf['imgurAPI'])
        return im.upload_image(self.conf['imgPath'], title=imageTitle).link