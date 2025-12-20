from PIL import Image
import numpy as np
import random
import matplotlib.pyplot as plt
from PIL import Image
import os

# Grauwert -> Anzahl Pixel
mapping = {
    20: 52,   # N Grad
    40: 27,   # N Minuten
    80: 132,  # N Tausendstel Minuten
    120: 13,   # E Grad (z.B. 013)
    160: 8,   # E Minuten
    200: 978,  # E Tausendstel Minuten
}

# Alle Pixelwerte in eine Liste
pixels = []
for gray, count in mapping.items():
    pixels.extend([gray] * count)

# Shuffle, damit es „zufällig“ aussieht
random.shuffle(pixels)

# Aus Liste ein Bild machen (z.B. 64 x 24 Pixel, muss groß genug sein)
width = 64
height = (len(pixels) + width - 1) // width
pixels += [0] * (width * height - len(pixels))  # auffüllen

arr = np.array(pixels, dtype=np.uint8).reshape((height, width))

#plt.imshow(arr)
#plt.show()

im = Image.fromarray(arr)
im.save("./images/histograms/20-6shadesofgray.jpg")
#im.show()