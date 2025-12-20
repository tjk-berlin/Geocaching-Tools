from PIL import Image
import os

# =========================
# Konfiguration
# =========================
BASE_DIR = "navy"
OUTPUT_FILE = "17-east.png"
HORIZONTAL_SPACING = 20  # Abstand zwischen Flaggen in Pixeln

SEQUENCE = ["E", "1", "3", "1", "2", "4", "7", "9"]

SYMBOL_FILES = {
    "0": "ICS_Pennant_Zero.svg.png",
    "1": "ICS_Pennant_One.svg.png",
    "2": "ICS_Pennant_Two.svg.png",
    "3": "ICS_Pennant_Three.svg.png",
    "4": "ICS_Pennant_Four.svg.png",
    "5": "ICS_Pennant_Five.svg.png",
    "6": "ICS_Pennant_Six.svg.png",
    "7": "ICS_Pennant_Seven.svg.png",
    "8": "ICS_Pennant_Eight.svg.png",
    "9": "ICS_Pennant_Niner.svg.png",
    "N": "ICS_November.svg.png",
    "E": "ICS_Echo.svg.png",
}

# Pfade vollständig machen
SYMBOL_FILES = {
    key: os.path.join(BASE_DIR, filename)
    for key, filename in SYMBOL_FILES.items()
}

# =========================
# Funktionen
# =========================
def make_symbol_canvas(
    symbol: Image.Image,
    target_height: int,
    align: str = "center",
    scale_factor: float = 1.0,
) -> Image.Image:
    """Skaliert ein Symbol auf target_height und richtet es vertikal aus."""
    sym_height = int(target_height * scale_factor)
    sym_width = int(symbol.width * sym_height / symbol.height)

    symbol = symbol.resize((sym_width, sym_height), Image.LANCZOS)

    canvas = Image.new("RGBA", (sym_width, target_height), (0, 0, 0, 0))

    if align == "top":
        y = 0
    elif align == "bottom":
        y = target_height - sym_height
    else:  # center
        y = (target_height - sym_height) // 2

    canvas.paste(symbol, (0, y), symbol)
    return canvas


def load_symbol(key: str) -> Image.Image:
    return Image.open(SYMBOL_FILES[key]).convert("RGBA")


# =========================
# Main
# =========================
def main():
    # Zielhöhe bestimmen (Referenzsymbol)
    reference = load_symbol("0")
    target_height = reference.height
    print(f"Target height: {target_height}px")

    # Symbole vorbereiten
    tiles = [
        make_symbol_canvas(load_symbol(key), target_height)
        for key in SEQUENCE
    ]

    # Gesamtbreite inkl. Abstände
    total_width = (
        sum(tile.width for tile in tiles)
        + HORIZONTAL_SPACING * (len(tiles) - 1)
    )

    result = Image.new("RGBA", (total_width, target_height), (0, 0, 0, 0))

    # Einfügen mit Abstand
    x = 0
    for tile in tiles:
        result.paste(tile, (x, 0), tile)
        x += tile.width + HORIZONTAL_SPACING

    result.save(OUTPUT_FILE)
    print(f"Fertig! Gespeichert als {OUTPUT_FILE}")


if __name__ == "__main__":
    main()