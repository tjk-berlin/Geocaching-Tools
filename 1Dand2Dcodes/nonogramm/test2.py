import matplotlib.pyplot as plt
import numpy as np

north = "5242.102"

def toBinaryBytes(s):
    bits = []
    for ch in s:
        b = f"{ord(ch):08b}"
        bits.extend(list(b))
    return np.array(bits, dtype=int)

# Bits erzeugen (64 Bits)
bits = toBinaryBytes(north)

# 8×8 Grid
grid = bits.reshape((8, 8))

plt.figure(figsize=(6, 6))

# --- WICHTIG ---
# extent sorgt dafür, dass Pixel exakt in einem 8x8-Koordinatensystem liegen
plt.imshow(grid, cmap="gray_r", extent=[0, 8, 0, 8])

# Gitterlinien zwischen den Feldern
plt.xticks(np.arange(0.5, 8, 1))
plt.yticks(np.arange(0.5, 8, 1))

plt.grid(color="black", linewidth=1)

# Achsen invertieren (optional, für klassisches Matrix-Layout)
plt.gca().invert_yaxis()

# Achsen ohne Labels
plt.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

plt.show()
