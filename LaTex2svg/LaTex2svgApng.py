import subprocess
import tempfile
from pathlib import Path
import textwrap
import csv


def latex_formula_to_images(formula: str, output_base: str):
    """
    Rendert eine LaTeX-Formel sowohl als SVG als auch als PNG.

    :param formula: LaTeX-Mathe-Ausdruck ohne $-Zeichen
    :param output_base: Basis-Dateiname (ohne oder mit Extension).
                        Es werden <basename>.svg und <basename>.png erzeugt.
    """
    output_base = Path(output_base)
    output_svg = output_base.with_suffix(".svg")
    output_png = output_base.with_suffix(".png")

    # Temporären Ordner anlegen
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        tex_file = tmpdir / "formula.tex"

        # LaTeX-Dokument mit preview-Paket für engen Zuschnitt
        tex_content = textwrap.dedent(rf"""
        \documentclass{{article}}
        \usepackage[active,tightpage]{{preview}}
        \usepackage{{amsmath,amssymb}}

        \begin{{document}}
        \begin{{preview}}
        ${formula}$
        \end{{preview}}
        \end{{document}}
        """)

        tex_file.write_text(tex_content, encoding="utf-8")

        # LaTeX laufen lassen (DVI erzeugen)
        subprocess.run(
            ["latex", "-interaction=nonstopmode", tex_file.name],
            cwd=tmpdir,
            check=True,
        )

        # DVI → SVG, Rand automatisch trimmen (-a), keine eingebetteten Fonts (-n)
        subprocess.run(
            ["dvisvgm", "-n", "-a", "formula.dvi", "-o", "formula.svg"],
            cwd=tmpdir,
            check=True,
        )

        # DVI → PNG, enger Zuschnitt (-T tight)
        # Optional: Hintergrund transparent machen mit -bg Transparent (falls dein dvipng das unterstützt)
        subprocess.run(
            ["dvipng", "-T", "tight","-D", "300", "-o", "formula.png", "formula.dvi"],
            cwd=tmpdir,
            check=True,
        )

        # Dateien an Ziel verschieben
        (tmpdir / "formula.svg").replace(output_svg)
        (tmpdir / "formula.png").replace(output_png)


if __name__ == "__main__":
    with open("formulas_exampe.csv", "r", encoding="utf-8") as f:
        # Trennzeichen §, damit LaTeX-Formeln nicht kollidieren
        reader = csv.reader(f, delimiter="§")

        for row in reader:
            filename = row[0].strip()  # Basisname
            formel = row[1].strip()

            # erzeugt filename.svg UND filename.png
            latex_formula_to_images(formel, filename)
