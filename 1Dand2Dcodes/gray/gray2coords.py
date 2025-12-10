from PIL import Image
import os

# Basis-Ordner mit allen PNGs
BASE_DIR = "tmp"

# Mapping der Ziffern auf die Dateien gray_0.png ... gray_9.png
digit_files = {str(i): os.path.join(BASE_DIR, f"gray_{i}.png") for i in range(10)}

# Dateien für Grad- und Punkt-Symbol (kannst du anpassen)
symbol_files = {
    "°": os.path.join(BASE_DIR, "deg.png"),   # Grad-Symbol
    ".": os.path.join(BASE_DIR, "dot.png")    # Punkt-Symbol
}

# Die gewünschte Bildfolge:
# gray_5.png, gray_2.png, Grad, gray_2.png, gray_4.png, Punkt, gray_3.png, gray_1.png, gray_1.png
sequence = ["1", "3", "°", "1", "7", ".", "7", "9", "4"]

# Skalierungsfaktor, wie groß die Symbole relativ zur Höhe der Zahlbilder sein sollen
SYMBOL_SCALE_FACTOR = 1  # 0.5 = 50% der Höhe

def make_symbol_canvas(sym_img, target_height, align="top", scale_factor=1):
    """Erstellt ein transparentes Bild mit Höhe target_height,
    in das das Symbol resized und oben/unten zentriert eingefügt wird."""
    # Symbolhöhe definieren
    sym_h = int(target_height * scale_factor)
    sym_w = int(sym_img.width * sym_h / sym_img.height)

    sym_resized = sym_img.resize((sym_w, sym_h), Image.LANCZOS)

    # Transparentes Canvas mit Zielhöhe
    canvas = Image.new("RGBA", (sym_w, target_height), (0, 0, 0, 0))

    if align == "top":
        y = 0
    elif align == "bottom":
        y = target_height - sym_h
    else:  # z.B. "center"
        y = (target_height - sym_h) // 2

    # Symbol mit Alphakanal einfügen
    canvas.paste(sym_resized, (0, y), sym_resized)
    return canvas

def main():
    # Beispiel: Höhe aus einem der gray-Bilder bestimmen
    # (wir nehmen gray_0.png, du kannst das anpassen)
    example_img = Image.open(digit_files["0"]).convert("RGBA")
    target_height = example_img.height
    print(f"Target height: {target_height}")

    tiles = []

    for item in sequence:
        if item.isdigit():
            # Ziffer -> passendes gray_*.png laden
            path = digit_files[item]
            img = Image.open(path).convert("RGBA")

            # Falls die Höhe aus irgendeinem Grund abweicht, auf target_height skalieren
            if img.height != target_height:
                new_w = int(img.width * target_height / img.height)
                img = img.resize((new_w, target_height), Image.LANCZOS)

            tiles.append(img)

        else:
            # Symbol (Grad oder Punkt)
            path = symbol_files[item]
            sym = Image.open(path).convert("RGBA")

            # Grad oben bündig, Punkt unten bündig
            if item == "°":
                canvas = make_symbol_canvas(
                    sym, target_height, align="top", scale_factor=SYMBOL_SCALE_FACTOR
                )
            elif item == ".":
                canvas = make_symbol_canvas(
                    sym, target_height, align="bottom", scale_factor=SYMBOL_SCALE_FACTOR
                )
            else:
                # Fallback: mittig
                canvas = make_symbol_canvas(
                    sym, target_height, align="center", scale_factor=SYMBOL_SCALE_FACTOR
                )

            tiles.append(canvas)

    # Gesamtbreite bestimmen
    total_width = sum(img.width for img in tiles)

    # Ausgabebild erzeugen
    result = Image.new("RGBA", (total_width, target_height), (0, 0, 0, 0))

    # Kacheln nacheinander einfügen
    x_offset = 0
    for img in tiles:
        result.paste(img, (x_offset, 0), img)
        x_offset += img.width

    # Speichern
    output_path = "10-east.png"
    result.save(output_path)
    print(f"Fertig! Gespeichert als {output_path}")

if __name__ == "__main__":
    main()