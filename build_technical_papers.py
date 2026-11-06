"""Render the two archival articles from their versioned Markdown sources."""
from html import escape
from pathlib import Path
import re

from matplotlib import get_data_path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Table, TableStyle

ROOT = Path(__file__).resolve().parent
AUTHOR = "Richard Ikeda"
BLUE = colors.HexColor("#16445c")


def inline(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return escape(text.replace("**", "").replace("`", ""))


def build(source, target, language):
    styles = {
        "title": ParagraphStyle("Title", fontName="PaperBold", fontSize=21, leading=26,
                                textColor=BLUE, spaceAfter=15, keepWithNext=True),
        "heading": ParagraphStyle("Heading", fontName="PaperBold", fontSize=12, leading=17,
                                  textColor=BLUE, spaceBefore=10, spaceAfter=6, keepWithNext=True),
        "body": ParagraphStyle("Body", fontName="Paper", fontSize=9.3, leading=13, spaceAfter=7),
        "cell": ParagraphStyle("Cell", fontName="Paper", fontSize=8, leading=11),
    }
    story = []
    pending_image = None
    title = source.read_text(encoding="utf-8").splitlines()[0][2:]
    for block in source.read_text(encoding="utf-8").strip().split("\n\n"):
        block = block.strip()
        if block.startswith("!["):
            path = (source.parent / block.split("](", 1)[1].rstrip(")")).resolve()
            pending_image = Image(str(path), width=485, height=435, kind="proportional")
        elif pending_image is not None:
            story.append(KeepTogether([pending_image, Paragraph(inline(block), styles["body"])]))
            pending_image = None
        elif block in ("## Figures", "## Figuras"):
            story.extend([PageBreak(), Paragraph(inline(block[3:]), styles["heading"])])
        elif block.startswith("|"):
            rows = [line.strip("|").split("|") for line in block.splitlines()]
            cells = [[Paragraph(inline(c.strip()), styles["cell"]) for c in row]
                     for row in [rows[0], *rows[2:]]]
            table = Table(cells, colWidths=[485 / len(cells[0])] * len(cells[0]), repeatRows=1)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbeaf2")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f6f9")]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
            ]))
            table.spaceAfter = 9
            story.append(table)
        else:
            style = "title" if block.startswith("# ") else "heading" if block.startswith("## ") else "body"
            story.append(Paragraph(inline(block.lstrip("# ")), styles[style]))

    def footer(canvas, doc):
        canvas.setFont("Paper", 8)
        canvas.setFillColor(BLUE)
        canvas.drawString(48, 26, f"OMEGAGRAD 1.0.0  |  {AUTHOR}  |  {language}")
        canvas.drawRightString(A4[0] - 48, 26, str(doc.page))

    target.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(target), pagesize=A4, leftMargin=48, rightMargin=48,
                            topMargin=44, bottomMargin=46, title=title, author=AUTHOR,
                            subject=f"Technical report · OMEGAGRAD 1.0.0 · {language}")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(target.relative_to(ROOT))


def main():
    fonts = Path(get_data_path()) / "fonts/ttf"
    pdfmetrics.registerFont(TTFont("Paper", str(fonts / "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("PaperBold", str(fonts / "DejaVuSans-Bold.ttf")))
    build(ROOT / "docs/en/PAPER.md", ROOT / "output/pdf/OMEGAGRAD_Technical_Paper.pdf", "en-US")
    build(ROOT / "docs/pt-BR/ARTIGO_TECNICO.md", ROOT / "output/pdf/OMEGAGRAD_Artigo_Tecnico.pdf", "pt-BR")


if __name__ == "__main__":
    main()
