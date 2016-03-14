__author__ = 'ajayb'

from cStringIO import StringIO
from PIL import Image
from base64 import encodestring, decodestring
import base64

im = Image.open("image.jpg")
buffer = StringIO()
im.save(buffer, format="JPEG")
img_str = base64.b64encode(buffer.getvalue())
print im.size
size = im.size
print img_str
print len(img_str)
size = (600,400)
im.thumbnail(size)
print im.size
buffer = StringIO()
im.save(buffer, format="JPEG")
img_str = base64.b64encode(buffer.getvalue())
print img_str
print len(img_str)
fh = open("imageToSave.png", "wb")
fh.write(base64.b64decode(img_str))
fh.close()