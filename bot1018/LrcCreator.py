from PIL import Image, ImageFont, ImageDraw
from ProcessInterface import ProcessInterface
import itchat
from itchat.content import *
from utilities import *

class LrcCreator(ProcessInterface):
    lrc_img = "Temp/wyyyy.jpg"
    font_path = 'src/apple.ttf'
    def process(self, msg, type):
        if type != TEXT:
            return
        content = msg['Content']
        if not content.startswith('/lrc-'):
            return

        group_id, group_name = get_group_info(msg)
        content = content.split('-')
        cover_path = 'src/hebe{}.jpg'.format(content[1])
        title = content[2]
        lrcs = content[3].split('.')
        # title = '——「爱着爱着就永远」'
        # lrcs = ['我又开始写日记了', '我这里天快要亮了', '那里呢', '我这里一切都变了', '而那你呢', '如果我们现在还在一起会是怎样', '我又开始写日记了','我又开始写日记了','我又开始写日记了','我又开始写rwe日记了']
        self.create_lrc_img(cover_path, title, lrcs)
        itchat.send_image(self.lrc_img, group_id)


    def create_lrc_img(self, cover_path, title, lrcs, add_footer=True):
        font = ImageFont.truetype(self.font_path, 32)

        font_color = '#2a2a2a'

        title = '——「{}」'.format(title)

        num = len(lrcs)

        width = 750
        footer_heght = 80 if add_footer else 0
        height = width + footer_heght + num * 60 + 150  #40+50+40+20
        pic_size = (width, height)

        horiz_offset = 40
        uper_offset = width + 40

        img = Image.new("RGB", pic_size, (255, 255, 255))
        dr = ImageDraw.Draw(img)

        for i in range(num):
            # title_size = dr.textsize(lrcs[i], font)
            dr.text((horiz_offset, uper_offset + 60 * i), lrcs[i], font=font, fill=font_color)

        title_size = dr.textsize(title, font)

        uper_offset += 60 * num + 50
        dr.text((width - 15 - title_size[0], uper_offset), title, font=font, fill=font_color)   #title

        img.paste(Image.open(cover_path).resize((width, width)))

        if footer_heght:
            img.paste(Image.open('src/wyy.jpg'), (0, uper_offset + 60))

        # img.show()
        img.save(self.lrc_img)