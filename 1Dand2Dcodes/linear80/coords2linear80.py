import random as rd
from PIL import Image, ImageDraw

# Inputs north
nd1 = 1
nd2 = 3
nm1 = 0
nm2 = 1
nm3 = 6
ndm1 = 5
ndm2 = 4
ndm3 = 7

# Inputs east
east_input = [1, 3, 0, 1, 6, 5, 4, 7]
east_zip = [1,4,1,0,9]

kodierung_01247 = ["00011", "11000", "10100", "01100", "10010", "01010", "00110", "01110", "01001", "00101"]
kodierung_8421 = ["0000", "0001", "0010", "0011", "0100", "0101", "0110", "1010", "1000", "1001"]

# define random binary field for better format
def rdbinary():
    return f"{rd.randint(0, 1)}"

north_binary = (rdbinary()
                +rdbinary()
                +kodierung_8421[nd1]            # first degree digit
                +rdbinary()
                +kodierung_8421[nd2]            # second degree digit
                +rdbinary()
                +kodierung_8421[nm1]
                +rdbinary()
                +kodierung_8421[nm2]
                +rdbinary()
                +kodierung_8421[nm3]
                +rdbinary()
                +kodierung_8421[ndm1]
                +rdbinary()
                +kodierung_8421[ndm2]
                +rdbinary()
                +kodierung_8421[ndm3]
                +rdbinary()
                +kodierung_01247[1]
                +rdbinary()
                +kodierung_01247[4]
                +rdbinary()
                +kodierung_01247[1]
                +rdbinary()
                +kodierung_01247[0]
                +rdbinary()
                +kodierung_01247[9]
                +rdbinary()
                +kodierung_01247[2]             # Prüfzimmer (2 = PLZ OK)
                +"000")

east_binary = rdbinary()
for i in east_input:
    east_binary= east_binary+rdbinary()
    east_binary= east_binary+kodierung_8421[i]

for i in east_zip:
    east_binary = east_binary + rdbinary()
    east_binary = east_binary + kodierung_01247[i]

east_binary = east_binary + rdbinary() + kodierung_01247[2] +"000"

print(north_binary)
print(east_binary)

def make_rect_image(bits, rect_width=20, rect_height=80,
                    color0=(255, 255, 255),  # weiß
                    color1=(255, 140, 0),    # orange
                    border_color=(0, 0, 0),  # schwarz
                    border_width=1,
                    out_path="output.png"):
    """
    bits: Liste aus 0 und 1, z.B. [0,1,0,1,...]
    rect_width, rect_height: Größe der einzelnen Rechtecke in Pixeln
    """
    n = len(bits)
    if n == 0:
        raise ValueError("Die Liste 'bits' darf nicht leer sein.")

    # Bildgröße berechnen
    img_width = n * rect_width
    img_height = rect_height

    # Bild erstellen (weißer Hintergrund)
    img = Image.new("RGB", (img_width, img_height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    for i, bit in enumerate(bits):
        # x-Koordinaten für dieses Rechteck
        x0 = i * rect_width
        y0 = 0
        x1 = x0 + rect_width
        y1 = rect_height

        fill_color = color1 if bit == "0" else color0

        # Erst Füllung zeichnen (innenliegend, damit der Rand sichtbar bleibt)
        draw.rectangle(
            [x0 + border_width, y0 + border_width,
             x1 - border_width, y1 - border_width],
            fill=fill_color
        )

        # Dann Rahmen zeichnen
        for bw in range(border_width):
            draw.rectangle(
                [x0 + bw, y0 + bw,
                 x1 - bw - 1, y1 - bw - 1],
                outline=border_color
            )
    img.save(out_path)
    print(f"Bild gespeichert als {out_path}")


 make_rect_image(north_binary, rect_width=20, rect_height=100, out_path="./07-east.png")