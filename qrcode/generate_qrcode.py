import io
import segno
from PIL import Image

source_file = 'example.vcf'
target_file = 'example'
image_file = 'bender.png'

error_correction = 'h'
qrcode_size = 3
# image size of the forground image 1/foreground_img_size
foreground_img_size = 3.3

with open(source_file, 'r') as file:
    content = file.read()

qr = segno.make(content, error=error_correction)
qr_bytes = io.BytesIO()
qr.save(qr_bytes, kind='png', scale=qrcode_size)

#write qr code with background image
qr.to_artistic(background=image_file, target=target_file + '_background' + '.png', scale=qrcode_size)

#write qr code without image
qr.save(target_file + '.png', scale=qrcode_size)

# generate and write qr code with image in the middle foreground
qr_image = Image.open(qr_bytes).convert('RGB')
src_w, src_h = qr_image.size
image = Image.open(image_file)
image = image.resize((int(src_w / foreground_img_size), int(src_h / foreground_img_size)))
image_w, image_h = image.size
qr_image.paste(image, ((src_w-image_w) // 2, (src_h-image_h) // 2))
qr_image.save(target_file + '_foreground' + '.png')
#qr_image.show()
