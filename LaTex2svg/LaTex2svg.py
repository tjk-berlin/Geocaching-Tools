import subprocess
import tempfile
from pathlib import Path
import textwrap
import csv

def latex_formula_to_svg(formula: str, output_svg: str):
    # Temporären Ordner anlegen
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        tex_file = tmpdir / "formula.tex"

        # LaTeX-Dokument mit standalone-Klasse (schneidet den Rand eng zu)
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

        tex_file.write_text(tex_content)

        # LaTeX laufen lassen (DVI statt PDF, damit dvisvgm happy ist)
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

        # SVG an Ziel kopieren
        Path(tmpdir / "formula.svg").replace(output_svg)

if __name__ == "__main__":
    with open("formulas_exampe.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="§")  # <--- Set to § to eliminate Conflicts with latex formulas

        for row in reader:
            filename = row[0].strip()
            formel = row[1].strip()

            latex_formula_to_svg(formel, filename)