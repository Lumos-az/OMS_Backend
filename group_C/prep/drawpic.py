# coding:utf-8
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random
import base64
import io


class AddText:
    def image_to_base64(self, img):
        output_buffer = io.BytesIO()
        img.save(output_buffer, format='JPEG')
        binary_data = output_buffer.getvalue()
        base64_data = base64.b64encode(binary_data)
        return base64_data

    def put_text(self, name_c="优思明", name_e="U Miss Bright", fac="一天不做爱会死制药厂"):
        img_orin = Image.open("pic.png")
        img = img_orin.copy()
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('simsun.ttc', 25)
        draw.text((160, 70), name_c, fill=(50, 50, 50), font=font)
        font = ImageFont.truetype('simsun.ttc', 15)
        draw.text((160, 105), name_e, fill=(50, 50, 50), font=font)
        font = ImageFont.truetype('simsun.ttc', 15)
        draw.text((60, 220), fac, fill=(50, 50, 50), font=font)

        change = random.randint(0, 255)
        img_hsv = img.convert("HSV")
        arr = np.asarray(img_hsv, int)
        for row in arr:
            for p in row:
                p[0] += change
                if p[0] > 255:
                    p[0] -= 255
        img_hsv = Image.fromarray(np.uint8(arr), mode="HSV")
        img = img_hsv.convert("RGB")
        return self.image_to_base64(img)