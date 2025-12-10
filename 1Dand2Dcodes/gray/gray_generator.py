import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle


def draw_gray_code_disk(
    n_bits=8,
    r_inner=0.1,
    r_outer=1.0,
    invert=False,
    align_position=None,
):
    """
    Zeichnet eine Grey-Code-Scheibe.

    n_bits         : Anzahl der Bits (Spuren)
    r_inner        : innerer Lochradius
    r_outer        : äußerer Gesamtradius
    invert         : 0/1-Farben vertauschen
    align_position : Integer (0..2**n_bits-1).
                     Wenn gesetzt, wird die Scheibe so gedreht, dass
                     diese Grey-Code-Position auf der rechten Horizontalen liegt.
    draw_circles   : Wenn True, werden 4 gefüllte Kreise auf einer horizontalen Linie gezeichnet.
    """
    n_positions = 2**n_bits
    angle_step = 360.0 / n_positions

    # Rotationswinkel berechnen (in Grad)
    if align_position is not None:
        # Mitte des gewünschten Segments auf 0° (rechte Seite) legen
        rotation_deg = - (align_position + 0.5) * angle_step
    else:
        rotation_deg = 0.0

    fig, ax = plt.subplots(figsize=(8, 8))

    track_thickness = (r_outer - r_inner) / n_bits

    for pos in range(n_positions):
        gray = pos ^ (pos >> 1)

        # gedrehte Winkel
        start_angle = rotation_deg + pos * angle_step
        end_angle = rotation_deg + (pos + 1) * angle_step

        # LSB innen, MSB außen (wie in deiner letzten Version)
        for ring in range(n_bits):
            bit = n_bits - 1 - ring  # MSB außen, LSB innen
            bit_val = (gray >> bit) & 1

            if invert:
                bit_val = 1 - bit_val

            color = "black" if bit_val == 1 else "white"

            r0 = r_inner + ring * track_thickness
            r1 = r_inner + (ring + 1) * track_thickness

            wedge = Wedge(
                center=(0, 0),
                r=r1,
                theta1=start_angle,
                theta2=end_angle,
                width=track_thickness,
            )
            wedge.set_facecolor(color)
            wedge.set_edgecolor("black")
            wedge.set_linewidth(0.2)
            ax.add_patch(wedge)

            # Optional: dünne Linie durch die Kreise als "horizontale Achse"
            ax.plot(
                [0,1],
                [0,0],
                linewidth=1,
                color="red",
            )

    # Achsen anpassen
    ax.set_xlim(-r_outer - 0.1, r_outer + 0.1)
    ax.set_ylim(-r_outer - 0.1, r_outer + 0.1)
    ax.axis("off")

    plt.tight_layout()
    plt.savefig(f'tmp/gray_{align_position}.png', bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    # Beispiel:
    #  - 6-Bit-Grey-Code-Scheibe
    #  - Position 5 soll auf der rechten Horizontalen liegen
    #for i in range(0,9,1):
        #draw_gray_code_disk(n_bits=4, align_position=i)
    draw_gray_code_disk(n_bits=4, align_position=9)