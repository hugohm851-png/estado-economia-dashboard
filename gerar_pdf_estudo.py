"""
Gera PDF do Fluxo de Estudo — Avaliação de Empresas
Formatação profissional com reportlab
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

W, H = A4

# ── Paleta de cores ────────────────────────────────────────────────────────────
NAVY      = colors.HexColor("#0D2B4E")
BLUE      = colors.HexColor("#1A5276")
TEAL      = colors.HexColor("#148F77")
PURPLE    = colors.HexColor("#6C3483")
ORANGE    = colors.HexColor("#CA6F1E")
RED       = colors.HexColor("#922B21")
GOLD      = colors.HexColor("#B7950B")
LIGHTBLUE = colors.HexColor("#D6EAF8")
LIGHTGREEN= colors.HexColor("#D5F5E3")
LIGHTPURP = colors.HexColor("#E8DAEF")
LIGHTYELL = colors.HexColor("#FEF9E7")
LIGHTGREY = colors.HexColor("#F2F3F4")
MIDGREY   = colors.HexColor("#AAB7B8")
WHITE     = colors.white
BLACK     = colors.HexColor("#1C2833")

MOD_COLORS = [NAVY, BLUE, TEAL, PURPLE, ORANGE, RED, GOLD]

# ── Estilos ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

sTitle = S("sTitle",
    fontSize=26, leading=32, alignment=TA_CENTER,
    textColor=NAVY, fontName="Helvetica-Bold", spaceAfter=6)

sSubtitle = S("sSubtitle",
    fontSize=14, leading=18, alignment=TA_CENTER,
    textColor=BLUE, fontName="Helvetica", spaceAfter=4)

sCaption = S("sCaption",
    fontSize=10, leading=13, alignment=TA_CENTER,
    textColor=MIDGREY, fontName="Helvetica-Oblique", spaceAfter=2)

sModHeader = S("sModHeader",
    fontSize=15, leading=19, alignment=TA_LEFT,
    textColor=WHITE, fontName="Helvetica-Bold",
    leftIndent=10, spaceAfter=0, spaceBefore=0)

sH2 = S("sH2",
    fontSize=12, leading=15, alignment=TA_LEFT,
    textColor=BLUE, fontName="Helvetica-Bold",
    spaceBefore=10, spaceAfter=4)

sH3 = S("sH3",
    fontSize=10.5, leading=13, alignment=TA_LEFT,
    textColor=NAVY, fontName="Helvetica-Bold",
    spaceBefore=6, spaceAfter=2)

sBody = S("sBody",
    fontSize=10, leading=14, alignment=TA_JUSTIFY,
    textColor=BLACK, fontName="Helvetica",
    spaceBefore=2, spaceAfter=2)

sBullet = S("sBullet",
    fontSize=10, leading=14, alignment=TA_LEFT,
    textColor=BLACK, fontName="Helvetica",
    leftIndent=14, firstLineIndent=-10,
    spaceBefore=1, spaceAfter=1)

sBullet2 = S("sBullet2",
    fontSize=9.5, leading=13, alignment=TA_LEFT,
    textColor=BLACK, fontName="Helvetica",
    leftIndent=26, firstLineIndent=-10,
    spaceBefore=1, spaceAfter=1)

sFormula = S("sFormula",
    fontSize=9.5, leading=14, alignment=TA_LEFT,
    textColor=BLUE, fontName="Courier-Bold",
    leftIndent=16, spaceBefore=2, spaceAfter=2)

sFormulaNote = S("sFormulaNote",
    fontSize=9, leading=13, alignment=TA_LEFT,
    textColor=NAVY, fontName="Courier",
    leftIndent=20, spaceBefore=0, spaceAfter=1)

sNote = S("sNote",
    fontSize=9, leading=12, alignment=TA_LEFT,
    textColor=colors.HexColor("#555555"), fontName="Helvetica-Oblique",
    leftIndent=8, spaceBefore=2, spaceAfter=4)

sTableHdr = S("sTableHdr",
    fontSize=9.5, leading=12, alignment=TA_CENTER,
    textColor=WHITE, fontName="Helvetica-Bold")

sTableCell = S("sTableCell",
    fontSize=9, leading=12, alignment=TA_LEFT,
    textColor=BLACK, fontName="Helvetica")

sFooter = S("sFooter",
    fontSize=8, leading=10, alignment=TA_CENTER,
    textColor=MIDGREY, fontName="Helvetica-Oblique")

sIndex = S("sIndex",
    fontSize=10, leading=14, alignment=TA_LEFT,
    textColor=BLACK, fontName="Helvetica",
    leftIndent=10, spaceBefore=1, spaceAfter=1)

sQuest = S("sQuest",
    fontSize=9.5, leading=13, alignment=TA_LEFT,
    textColor=BLACK, fontName="Helvetica",
    leftIndent=14, firstLineIndent=-10,
    spaceBefore=3, spaceAfter=1)

sAnswerLine = S("sAnswerLine",
    fontSize=9, leading=11, alignment=TA_LEFT,
    textColor=MIDGREY, fontName="Helvetica",
    leftIndent=20, spaceBefore=1, spaceAfter=3)


# ── Componentes visuais ────────────────────────────────────────────────────────

class ColorBar(Flowable):
    """Barra colorida horizontal."""
    def __init__(self, color, height=4, width=None):
        Flowable.__init__(self)
        self._color = color
        self._h = height
        self._w = width
    def wrap(self, aw, ah):
        self.width = self._w or aw
        self.height = self._h
        return self.width, self.height
    def draw(self):
        self.canv.setFillColor(self._color)
        self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=0)


class ModuleHeader(Flowable):
    """Cabeçalho de módulo com fundo colorido e número em destaque."""
    def __init__(self, number, title, subtitle, color):
        Flowable.__init__(self)
        self._n = number
        self._title = title
        self._sub = subtitle
        self._color = color
    def wrap(self, aw, ah):
        self.width = aw
        self.height = 52
        return self.width, self.height
    def draw(self):
        c = self.canv
        w, h = self.width, self.height
        # Fundo
        c.setFillColor(self._color)
        c.roundRect(0, 0, w, h, 6, fill=1, stroke=0)
        # Círculo do número
        c.setFillColor(WHITE)
        c.circle(28, h/2, 18, fill=1, stroke=0)
        c.setFillColor(self._color)
        c.setFont("Helvetica-Bold", 15)
        c.drawCentredString(28, h/2 - 5.5, str(self._n))
        # Título
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(56, h/2 + 4, self._title)
        # Subtítulo
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(colors.HexColor("#CCDDEE"))
        c.drawString(57, h/2 - 10, self._sub)


class FormulaBox(Flowable):
    """Caixa com fundo azul claro para fórmulas."""
    def __init__(self, lines, width=None):
        Flowable.__init__(self)
        self._lines = lines
        self._w = width
        self._pad = 10
    def wrap(self, aw, ah):
        self.width = self._w or aw
        self.height = len(self._lines) * 14 + 2 * self._pad
        return self.width, self.height
    def draw(self):
        c = self.canv
        w, h = self.width, self.height
        c.setFillColor(LIGHTBLUE)
        c.roundRect(0, 0, w, h, 5, fill=1, stroke=0)
        c.setStrokeColor(BLUE)
        c.setLineWidth(1.2)
        c.roundRect(0, 0, w, h, 5, fill=0, stroke=1)
        # Barra lateral
        c.setFillColor(BLUE)
        c.rect(0, 0, 4, h, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont("Courier-Bold", 9.5)
        y = h - self._pad - 10
        for line in self._lines:
            if line.startswith("═") or line.startswith("─"):
                c.setFillColor(BLUE)
                c.setFont("Courier", 9)
                c.drawString(14, y, line)
                c.setFillColor(NAVY)
                c.setFont("Courier-Bold", 9.5)
            elif line.startswith("  ") or line.startswith("→"):
                c.setFillColor(colors.HexColor("#1A5276"))
                c.setFont("Courier", 9)
                c.drawString(14, y, line)
                c.setFillColor(NAVY)
                c.setFont("Courier-Bold", 9.5)
            elif line == "":
                pass
            else:
                c.drawString(14, y, line)
            y -= 14


class SideCallout(Flowable):
    """Caixa lateral de destaque (tip/aviso)."""
    def __init__(self, text, color, label="", width=None):
        Flowable.__init__(self)
        self._text = text
        self._color = color
        self._label = label
        self._w = width
    def wrap(self, aw, ah):
        self.width = self._w or aw
        # Estimar altura
        chars_per_line = int((self.width - 36) / 5.5)
        lines = max(1, len(self._text) // chars_per_line + 1)
        self.height = lines * 13 + 24
        return self.width, self.height
    def draw(self):
        c = self.canv
        w, h = self.width, self.height
        c.setFillColor(colors.HexColor("#FDFEFE"))
        c.roundRect(0, 0, w, h, 5, fill=1, stroke=0)
        c.setFillColor(self._color)
        c.rect(0, 0, 5, h, fill=1, stroke=0)
        if self._label:
            c.setFont("Helvetica-Bold", 8.5)
            c.setFillColor(self._color)
            c.drawString(12, h - 14, self._label)
        c.setFont("Helvetica", 9)
        c.setFillColor(BLACK)
        # Texto simples (sem quebra automática sofisticada)
        c.drawString(12, 8, self._text[:120])


# ── Funções auxiliares ─────────────────────────────────────────────────────────

def bullet(text, level=0, bold_prefix=""):
    mark = "•" if level == 0 else "–"
    style = sBullet if level == 0 else sBullet2
    full = f"<b>{bold_prefix}</b>{text}" if bold_prefix else text
    return Paragraph(f"{mark}  {full}", style)


def two_col_table(rows, header1="", header2="", col_widths=None, color=BLUE):
    """Tabela de 2 colunas com cabeçalho opcional."""
    cw = col_widths or [5.5*cm, 11*cm]
    data = []
    if header1:
        data.append([
            Paragraph(f"<b>{header1}</b>", sTableHdr),
            Paragraph(f"<b>{header2}</b>", sTableHdr),
        ])
    for c1, c2 in rows:
        data.append([
            Paragraph(f"<b>{c1}</b>", sTableCell),
            Paragraph(c2, sTableCell),
        ])
    t = Table(data, colWidths=cw)
    style = [
        ("GRID",        (0,0), (-1,-1), 0.4, colors.HexColor("#BDC3C7")),
        ("ROWBACKGROUNDS", (0, 1 if header1 else 0), (-1,-1),
         [LIGHTGREY, WHITE]),
        ("VALIGN",      (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING",   (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
    ]
    if header1:
        style += [
            ("BACKGROUND",  (0,0), (-1,0), color),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [LIGHTGREY, WHITE]),
        ]
    t.setStyle(TableStyle(style))
    return t


def summary_box(title, items, color=BLUE):
    """Tabela de resumo com cabeçalho colorido."""
    data = [[Paragraph(f"<b>{title}</b>", sTableHdr)]]
    for item in items:
        if isinstance(item, tuple):
            txt = f"<b>{item[0]}</b>  {item[1]}"
        else:
            txt = item
        data.append([Paragraph(txt, sTableCell)])
    t = Table(data, colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), color),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[LIGHTGREY, WHITE]),
        ("GRID",         (0,0), (-1,-1), 0.4, colors.HexColor("#BDC3C7")),
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
    ]))
    return t


def self_check(questions, color=PURPLE):
    """Bloco de autoavaliação."""
    items = [[Paragraph(
        f'<font color="#6C3483"><b>Autoavaliação</b></font>', sTableHdr)]]
    for i, q in enumerate(questions, 1):
        items.append([Paragraph(f"<b>{i}.</b> {q}", sTableCell)])
        items.append([Paragraph("_" * 90, sAnswerLine)])
        items.append([Paragraph(" ", sTableCell)])
    t = Table(items, colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), PURPLE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[LIGHTPURP, WHITE]),
        ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#D7BDE2")),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    return t


def example_box(title, items, color=TEAL):
    """Caixa de exemplo resolvido."""
    data = [[Paragraph(f"<b>Exemplo Resolvido: {title}</b>", sTableHdr)]]
    for item in items:
        if isinstance(item, tuple):
            txt = f"<b>{item[0]}</b>  {item[1]}"
        else:
            txt = item
        data.append([Paragraph(txt, sTableCell)])
    t = Table(data, colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), color),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[LIGHTGREEN, WHITE]),
        ("GRID",         (0,0), (-1,-1), 0.4, colors.HexColor("#A9DFBF")),
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
    ]))
    return t


def sp(n=6):
    return Spacer(1, n)


def h2(text, color=BLUE):
    return Paragraph(f'<font color="#{color.hexval()[1:] if hasattr(color,"hexval") else "1A5276"}">'
                     f'<b>{text}</b></font>', sH2)


def h2b(text, c="#1A5276"):
    return Paragraph(f'<font color="{c}"><b>{text}</b></font>', sH2)


def divider(color=MIDGREY):
    return HRFlowable(width="100%", thickness=0.5, color=color, spaceAfter=6, spaceBefore=6)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE TEMPLATES
# ══════════════════════════════════════════════════════════════════════════════

def _header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    # Linha superior
    canvas.setFillColor(NAVY)
    canvas.rect(0, h - 28, w, 28, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(1.5*cm, h - 17, "FLUXO DE ESTUDO — AVALIAÇÃO DE EMPRESAS")
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(w - 1.5*cm, h - 17, "Mestrado Profissional em Economia")
    # Linha inferior
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, w, 20, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(1.5*cm, 6, "Prof. Sérgio Jurandyr Machado")
    canvas.drawRightString(w - 1.5*cm, 6, f"Página {doc.page}")
    canvas.restoreState()


def _cover_template(canvas, doc):
    canvas.saveState()
    w, h = A4
    # Fundo gradiente simulado com retângulos
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, w, h, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#0A1929"))
    canvas.rect(0, 0, w, h * 0.45, fill=1, stroke=0)
    # Linha dourada decorativa
    canvas.setFillColor(GOLD)
    canvas.rect(0, h * 0.45, w, 3, fill=1, stroke=0)
    canvas.restoreState()


# ══════════════════════════════════════════════════════════════════════════════
# CONTEÚDO
# ══════════════════════════════════════════════════════════════════════════════

story = []

# ── CAPA ──────────────────────────────────────────────────────────────────────
# Usamos primeira página sem header/footer — criamos manualmente via background
story.append(Spacer(1, 3.5*cm))

p = Paragraph("<font color='#B7950B'>◆ ◆ ◆</font>", S("d", fontSize=20,
              alignment=TA_CENTER, spaceAfter=10))
story.append(p)

story.append(Paragraph(
    '<font color="white"><b>FLUXO DE ESTUDO</b></font>',
    S("ct", fontSize=32, leading=38, alignment=TA_CENTER,
      fontName="Helvetica-Bold", spaceAfter=8)))

story.append(Paragraph(
    '<font color="#5DADE2"><b>Avaliação de Empresas</b></font>',
    S("cs", fontSize=22, leading=26, alignment=TA_CENTER,
      fontName="Helvetica-Bold", spaceAfter=6)))

story.append(Paragraph(
    '<font color="#AAB7B8">Mestrado Profissional em Economia</font>',
    S("cm", fontSize=13, alignment=TA_CENTER, spaceAfter=4)))

story.append(Paragraph(
    '<font color="#AAB7B8">Prof. Sérgio Jurandyr Machado</font>',
    S("ci", fontSize=11, alignment=TA_CENTER,
      fontName="Helvetica-Oblique", spaceAfter=30)))

story.append(Spacer(1, 2*cm))

# Linha decorativa
story.append(HRFlowable(width="60%", thickness=1.5, color=GOLD,
                         hAlign="CENTER", spaceAfter=20))

# Mini índice na capa
modulos_capa = [
    ("01", "Fundamentos do Valuation",            "Aula 1",    NAVY),
    ("02", "Fluxo de Caixa Livre — FCFF",         "Aulas 2–4", BLUE),
    ("03", "Taxa de Desconto — WACC",             "Aulas 2–4", TEAL),
    ("04", "Ajustes Contábeis para Valuation",    "Aulas 5–6", PURPLE),
    ("05", "Opções Reais e Valor da Flexibilidade","Aulas 7–8", ORANGE),
    ("06", "Criação de Valor & Múltiplos",         "Transversal",RED),
    ("07", "Revisão Geral e Exercício Integrado",  "Pré-Prova", GOLD),
]

idx_data = []
for num, title, ref, col in modulos_capa:
    idx_data.append([
        Paragraph(f'<font color="white"><b>{num}</b></font>',
                  S("n", fontSize=11, alignment=TA_CENTER, fontName="Helvetica-Bold")),
        Paragraph(f'<font color="white"><b>{title}</b></font>',
                  S("t", fontSize=10, fontName="Helvetica-Bold")),
        Paragraph(f'<font color="#AAB7B8">{ref}</font>',
                  S("r", fontSize=9, fontName="Helvetica-Oblique", alignment=TA_CENTER)),
    ])
    idx_colors = [
        ("BACKGROUND", (0, len(idx_data)-1), (-1, len(idx_data)-1),
         colors.HexColor(col.hexval() + "55" if len(col.hexval()) == 7 else col.hexval())),
    ]

t_idx = Table(idx_data, colWidths=[1.2*cm, 11*cm, 3.5*cm])
ts = TableStyle([
    ("BACKGROUND",   (0,0), (-1,-1), colors.HexColor("#142B3F")),
    ("LINEBELOW",    (0,0), (-1,-2), 0.5, colors.HexColor("#1A5276")),
    ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ("LEFTPADDING",  (0,0), (-1,-1), 8),
    ("RIGHTPADDING", (0,0), (-1,-1), 8),
    ("TOPPADDING",   (0,0), (-1,-1), 7),
    ("BOTTOMPADDING",(0,0), (-1,-1), 7),
    ("ROWBACKGROUNDS",(0,0),(-1,-1),[
        colors.HexColor("#0D2B4E"), colors.HexColor("#1A3A5C"),
        colors.HexColor("#1B5E7B"), colors.HexColor("#1B3A5C"),
        colors.HexColor("#3B1F5E"), colors.HexColor("#5E2F1A"),
        colors.HexColor("#5E4A08"),
    ]),
])
t_idx.setStyle(ts)
story.append(t_idx)

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 1
# ══════════════════════════════════════════════════════════════════════════════
story.append(ModuleHeader(1, "FUNDAMENTOS DO VALUATION", "Aula 1 | Introdução", NAVY))
story.append(sp(12))

story.append(h2b("1.1  O que é Valuation?"))
story.append(Paragraph(
    "Valuation é o processo de conversão de uma projeção em uma estimativa do "
    "<b>valor</b> de uma empresa ou de um ativo. É fundamental distinguir "
    "<b>preço</b> (o que o mercado cobra) de <b>valor</b> (o que o ativo vale "
    "de fato).", sBody))
story.append(sp(6))

story.append(two_col_table([
    ("DCF / FCD",            "Fluxo de Caixa Descontado: valor = capacidade de gerar caixa futuro."),
    ("Avaliação Relativa",   "Múltiplos: compara a empresa a pares (EV/EBITDA, P/L, etc.)."),
], "Método", "Descrição"))
story.append(sp(8))

story.append(h2b("1.2  Tese de Investimento"))
story.append(Paragraph(
    '<i>"O preço de um ativo converge para o seu valor justo."</i>', sNote))
story.append(sp(4))
story.append(two_col_table([
    ("Long",        "Compra ativo subavaliado: preço < valor justo."),
    ("Short",       "Vende ativo superavaliado: preço > valor justo."),
    ("Long & Short","Opera nos dois sentidos simultaneamente."),
], "Estratégia", "Lógica"))
story.append(sp(8))

story.append(h2b("1.3  Eficiência de Mercado"))
story.append(bullet("HME semi-forte: toda informação pública é incorporada "
                    "instantaneamente ao preço."))
story.append(bullet("AMH (Adaptive Markets): a convergência pode ser lenta por "
                    "fricções (custos de transação, restrição a venda a descoberto) "
                    "ou comportamento irracional (noise trader)."))
story.append(bullet('<i>"Gerar alfa é mais difícil do que ganhar as Olimpíadas."</i> — Damodaran'))
story.append(sp(8))

story.append(summary_box("Conceitos-Chave — Módulo 1", [
    ("Definição:", "Valuation = conversão de projeção em estimativa de valor."),
    ("Premissa DCF:", "Valor ≈ capacidade de geração de caixa futuro."),
    ("HME semi-forte:", "Informação pública → preço imediatamente."),
    ("Objetivo do analista:", "Identificar desvio entre preço e valor (gerar alfa)."),
    ("Citação:", '"I would buy any company at the right price." — Damodaran'),
], NAVY))
story.append(sp(10))

story.append(self_check([
    "Qual a diferença entre preço e valor de um ativo?",
    "O que é a HME em sua forma semi-forte? E a AMH?",
    "Quais as três perguntas centrais do método DCF?",
    "Por que gerar alfa é considerado tão difícil?",
]))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 2
# ══════════════════════════════════════════════════════════════════════════════
story.append(ModuleHeader(2, "FLUXO DE CAIXA LIVRE PARA A FIRMA — FCFF",
                          "Aulas 2–4 | Pergunta 1 do DCF", BLUE))
story.append(sp(12))

story.append(h2b("2.1  As Três Perguntas do DCF"))
story.append(two_col_table([
    ("Pergunta 1", "Qual o montante líquido de caixa gerado pelas atividades "
                   "operacionais e como se distribui no tempo? (FCFF)"),
    ("Pergunta 2", "Qual deve ser a taxa de desconto? (WACC)"),
    ("Pergunta 3", "Qual é o horizonte de análise? (Valor Terminal)"),
], "Nº", "Questão", [2*cm, 14*cm]))
story.append(sp(10))

story.append(h2b("2.2  Cálculo do FCFF Atual — Pergunta 1.a"))
story.append(FormulaBox([
    "EBIT",
    "(+) Depreciação e Amortização",
    "(=) EBITDA                      [Resolução CVM 156/2022]",
    "(+/-) Ajustes de itens não recorrentes",
    "(=) EBITDA Ajustado",
    "(-) IR/CSLL estimado sobre o EBIT",
    "(-) CAPEX  (investimentos em capital fixo)",
    "(-) ΔNCG   (variação do capital de giro não monetário)",
    "══════════════════════════════════════════════",
    "(=) FCFF em t",
]))
story.append(sp(10))

story.append(h2b("2.3  CAPEX vs. OPEX"))
story.append(two_col_table([
    ("CAPEX", "Investimento que: (i) gera receita adicional; (ii) aumenta vida "
              "útil; ou (iii) expande capacidade. Concentrado no tempo. "
              "Contemplado separadamente no DCF."),
    ("OPEX",  "Gasto do dia a dia. Mais frequente e recorrente. "
              "Já capturado no cálculo do EBIT."),
], "Tipo", "Características", [3*cm, 13*cm]))
story.append(sp(10))

story.append(h2b("2.4  Necessidade de Capital de Giro (NCG)"))
story.append(FormulaBox([
    "NCG = Estoques + Contas a Receber – Fornecedores",
    "",
    "Ciclo Financeiro = PME + PMR – PMP   (em dias de receita de vendas)",
    "  PME (Prazo Médio de Estoques)      → quanto menor, melhor",
    "  PMR (Prazo Médio de Recebimento)   → quanto menor, melhor",
    "  PMP (Prazo Médio de Pagamento)     → quanto maior, melhor",
]))
story.append(sp(10))

story.append(h2b("2.5  Base Razoável para Extrapolação — Pergunta 1.b"))
story.append(bullet("Verifique e elimine itens não recorrentes do FCFF base."))
story.append(bullet("Avalie se o CAPEX do período é representativo ou pontual."))
story.append(bullet("Confirme se a margem EBIT reflete condições normais de mercado."))
story.append(sp(8))

story.append(h2b("2.6  Taxa de Crescimento Esperada — Pergunta 1.c"))
story.append(FormulaBox([
    "g = ROIC × (CAPEX Líquido + ΔNCG) / NOPAT",
    "       ou",
    "g = Lucro Retido × ROE",
    "",
    "⚠  g de longo prazo ≤ PIB Potencial ± ajustes de eficiência",
]))
story.append(sp(10))

story.append(example_box("FCFF da Empresa XYZ — Polímeros Condutores", [
    ("Dados:",     "EBIT = R$ 20 MM  |  Depreciação = R$ 1,5 MM  |  IR = R$ 6,8 MM"),
    ("",           "Receita não recorrente = R$ 5,2 MM  |  ΔNCG = R$ 1 MM  |  CAPEX = R$ 2 MM"),
    ("FCFF 2025:", "20,0 + 1,5 – 5,2 – 6,8 – 1,0 – 2,0  =  R$ 6,5 MM"),
    ("FCFF 2026:", "R$ 6,5 MM × 1,02  =  R$ 6,63 MM   (crescimento real de 2%)"),
]))
story.append(sp(10))

story.append(self_check([
    "Qual a diferença entre EBITDA e FCFF?",
    "Por que subtraímos CAPEX e ΔNCG no cálculo do FCFF?",
    "Por que adicionamos depreciação de volta ao EBIT?",
    "Como itens não recorrentes afetam a extrapolação?",
    "Qual o risco de projetar g acima do PIB potencial de longo prazo?",
]))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 3
# ══════════════════════════════════════════════════════════════════════════════
story.append(ModuleHeader(3, "TAXA DE DESCONTO — WACC",
                          "Aulas 2–4 | Pergunta 2 do DCF", TEAL))
story.append(sp(12))

story.append(h2b("3.1  Custo de Capital Próprio (Ke) — CAPM", "#148F77"))
story.append(FormulaBox([
    "Ke  =  Rf  +  βi × (Rm – Rf)",
    "",
    "  Rf       = Taxa livre de risco",
    "  βi       = Beta da empresa i  (risco relativo ao mercado)",
    "  Rm – Rf  = Prêmio de risco de mercado (ERP)",
]))
story.append(sp(8))

story.append(h2b("3.2  Taxa Livre de Risco (Rf)", "#148F77"))
story.append(bullet("Requisitos: sem risco de default, sem risco de reinvestimento, "
                    "duration compatível com o horizonte."))
story.append(bullet("<b>Sugestão do professor:</b> NTN-B Principal (vencimento ~10 anos). "
                    "Taxa real; já embute o risco-país."))
story.append(bullet("Em valuation real:  Ke = Rf [NTN-B 10a] + βi × 5,5% a.a."))
story.append(sp(8))

story.append(h2b("3.3  Prêmio de Risco de Mercado (ERP)", "#148F77"))
story.append(two_col_table([
    ("ERP USA (S&P500)",
     "Média geométrica Stocks − T.Bonds (1928–2024) ≈ 5,44% a.a. "
     "Sugestão do professor: usar 5,5% a.a."),
    ("ERP Brasil",
     "Instável: varia muito com o horizonte. "
     "Alternativa: ERP EUA + Risco-País (CDS) → CAPM Global."),
    ("CAPM Global",
     "Ke = Rf[EUA] + β × (ERP[EUA] + Rp[BR]) + (INF_BR – INF_EUA). "
     "Avaliação em termos nominais."),
], "Abordagem", "Detalhes"))
story.append(sp(8))

story.append(h2b("3.4  Beta (β)", "#148F77"))
story.append(FormulaBox([
    "β = Cov(Ri, Rm) / σ²m",
    "",
    "  β < 1  →  ativo menos volátil que o mercado",
    "  β > 1  →  ativo mais volátil que o mercado",
    "",
    "Bottom-Up Beta:",
    "  β_alav = β_desalav × [1 + (1 – t) × (D/E)]",
]))
story.append(sp(8))

story.append(h2b("3.5  Custo de Capital de Terceiros (Kd) e WACC", "#148F77"))
story.append(FormulaBox([
    "Kd = Rf + SOT   (spread over treasury)",
    "Kd líquido = Kd × (1 – alíquota IR/CSLL)",
    "",
    "WACC = [E/(D+E)] × Ke  +  [D/(D+E)] × Kd × (1 – t)",
    "",
    "  Use pesos a valor de MERCADO (não contábil)",
    "  Ke > Kd  (capital próprio é mais caro — sem benefício fiscal direto)",
]))
story.append(sp(10))

story.append(example_box("Ke para Orizon (ORVR3) e Azul (AZUL4)", [
    ("Data:",    "22/10/2025  |  NTN-B 2035 = 7,66% a.a.  |  ERP = 5,5% a.a."),
    ("Orizon:",  "β = 0,21  →  Ke = 7,66 + 0,21 × 5,5 = 8,82% a.a."),
    ("Azul:",    "β = 1,73  →  Ke = 7,66 + 1,73 × 5,5 = 17,18% a.a."),
    ("Insight:", "Setor aéreo tem risco sistemático muito maior que gestão de resíduos."),
], TEAL))
story.append(sp(10))

story.append(self_check([
    "Por que o Ke não é diretamente observável?",
    "Por que o Kd é em geral mais barato que o Ke?",
    "O que acontece com o WACC se a empresa aumenta a alavancagem?",
    "Por que usar a NTN-B e não a SELIC como taxa livre de risco real?",
    "O que é um 'bottom-up beta' e quando utilizá-lo?",
]))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 4
# ══════════════════════════════════════════════════════════════════════════════
story.append(ModuleHeader(4, "AJUSTES CONTÁBEIS RELEVANTES PARA O VALUATION",
                          "Aulas 5–6 | 'The Usual Suspects'", PURPLE))
story.append(sp(12))

story.append(Paragraph(
    'Estes itens são os <b>"Usual Suspects"</b> — afetam (ou parecem afetar) o '
    'FCFF, mas sua influência real exige análise cuidadosa.', sNote))
story.append(sp(6))

story.append(h2b("4.1  Impairment — Perda por Desvalorização", "#6C3483"))
story.append(bullet("<b>Conceito:</b> quando Valor Contábil > Valor Recuperável, "
                    "reconhece-se perda no resultado."))
story.append(bullet("Valor Recuperável = max(Valor Justo Líquido, Valor em Uso)."))
story.append(bullet("<b>Efeito no FCFF:</b> não afeta o caixa diretamente. "
                    "Deve ser adicionado de volta (como depreciação)."))
story.append(bullet("<b>Atenção:</b> o mercado reage negativamente — interpreta que "
                    "os fluxos futuros serão menores. Revise suas premissas!"))
story.append(bullet("Casos: Petrobras 2015–2017 (R$ 44,6 bi) · Grupo Soma/Hering "
                    "(Lei nº 14.789/23 + EC 132/2023)."))
story.append(sp(8))

story.append(h2b("4.2  Provisões — Contingências Passivas", "#6C3483"))
story.append(two_col_table([
    ("Provável + mensurável",    "Provisionar no balanço (best estimate IFRS)"),
    ("Provável + não mensurável","Divulgar em notas explicativas"),
    ("Possível",                 "Divulgar em notas explicativas"),
    ("Remota",                   "Não divulgar"),
], "Classificação", "Tratamento Contábil", [5*cm, 11*cm]))
story.append(sp(4))
story.append(bullet("<b>Escrow Account:</b> valor retido do preço de aquisição em "
                    "conta vinculada; liberado ao vendedor se não houver contingências."))
story.append(bullet("<b>Earn-Out:</b> parcela do preço condicionada ao atingimento de "
                    "metas. Soluciona divergências de expectativas entre comprador e vendedor."))
story.append(sp(8))

story.append(h2b("4.3  Ágio (Goodwill)", "#6C3483"))
story.append(bullet("Surge em combinações de negócios: diferença entre o valor pago "
                    "e o valor justo dos ativos líquidos adquiridos."))
story.append(bullet("Representa sinergias estimadas em t₀ (redução de custo, ganho "
                    "de mercado). Analise se são razoáveis."))
story.append(sp(8))

story.append(h2b("4.4  ARO — Obrigação para Desmobilização de Ativos", "#6C3483"))
story.append(bullet("Custo de retirada de serviço do bem capitalizado como ativo + "
                    "provisão idêntica no passivo."))
story.append(bullet("Custo capitalizado é depreciado → aumenta EBITDA; "
                    "pagamento futuro reduz caixa."))
story.append(bullet("Caso Vale: compare o balanço do 4T/2018 com o 1T/2019 "
                    "(Brumadinho)."))
story.append(sp(8))

story.append(h2b("4.5  POC — Percentage of Completion Method", "#6C3483"))
story.append(bullet("Reconhece receita proporcionalmente ao avanço físico da obra."))
story.append(bullet("IFRS 15 exige transferência progressiva de controle ao cliente."))
story.append(bullet("IASB: POC <b>não</b> é aderente para incorporadoras residenciais "
                    "no Brasil — receita deve ser reconhecida na entrega das chaves."))
story.append(bullet("Para valuation: reconcilie sempre receita contábil com caixa "
                    "efetivamente recebido."))
story.append(sp(8))

story.append(h2b("4.6  Hedge Accounting", "#6C3483"))
story.append(bullet("Difere variações do instrumento de hedge no patrimônio, "
                    "reconhecendo ao resultado apenas quando o item objeto é impactado."))
story.append(bullet("Caso Petrobras (2013–2015): área técnica da CVM entendeu uso "
                    "para diferir perdas cambiais (\"desvirtuou a essência econômica\"); "
                    "Colegiado aceitou recurso da empresa."))
story.append(sp(10))

story.append(summary_box("Resumo — Impacto dos 'Usual Suspects' no FCFF", [
    ("Impairment:",   "Sem efeito caixa. Adicionar de volta. Revisar premissas de fluxo futuro."),
    ("Provisões:",    "Sem efeito caixa na constituição. Caixa sai no pagamento efetivo."),
    ("ARO:",          "Custo capitalizado: depreciação ↑. Pagamento futuro: caixa ↓."),
    ("POC:",          "Receita antecipada ≠ caixa recebido. Reconcilie sempre."),
    ("Hedge Acc.:",   "Pode distorcer DRE. Analise o caixa efetivo da operação objeto."),
], PURPLE))
story.append(sp(10))

story.append(self_check([
    "Por que o impairment não afeta o FCFF diretamente, mas afeta o valor percebido?",
    "Qual a diferença entre escrow account e earn-out?",
    "Como uma ARO subestimada pode inflar o valuation de uma empresa?",
    "Em que condições o POC é permitido pelo IFRS 15?",
    "Como identificar se o hedge accounting está sendo usado para diferir perdas?",
]))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 5
# ══════════════════════════════════════════════════════════════════════════════
story.append(ModuleHeader(5, "OPÇÕES REAIS E VALOR DA FLEXIBILIDADE",
                          "Aulas 7–8 | Pergunta 3 do DCF", ORANGE))
story.append(sp(12))

story.append(h2b("5.1  Conceito e Motivação", "#CA6F1E"))
story.append(Paragraph(
    "O VPL tradicional ignora o valor das decisões gerenciais futuras "
    "(expandir, adiar, contrair, abandonar). As opções reais capturam esse "
    "<b>valor de flexibilidade</b>:", sBody))
story.append(sp(4))
story.append(Paragraph(
    "VPL Expandido  =  VPL Tradicional  +  Valor das Opções Reais", sFormula))
story.append(sp(6))

story.append(two_col_table([
    ("Expansão",  "Ampliar o projeto se condições forem favoráveis. → Opção de COMPRA (call)."),
    ("Abandono",  "Encerrar e recuperar valor residual. → Opção de VENDA (put)."),
    ("Adiamento", "Postergar o início até obter mais informação."),
    ("Contração", "Reduzir escala se condições deteriorarem."),
], "Tipo de Opção Real", "Descrição"))
story.append(sp(10))

story.append(h2b("5.2  Árvore Binomial", "#CA6F1E"))
story.append(FormulaBox([
    "Em cada período: valor sobe (×u) ou cai (×d)",
    "  u = fator de subida   (calculado via volatilidade σ)",
    "  d = fator de descida  (d = 1/u → árvore recombinante)",
    "",
    "Probabilidade Neutra ao Risco (q):",
    "  q = (1 + r – d) / (u – d)",
    "  r = taxa livre de risco por período",
    "",
    "Valor do nó pai:",
    "  V = [q × V_sobe + (1–q) × V_desce] / (1 + r)",
]))
story.append(sp(10))

story.append(h2b("5.3  Por que Usar a Probabilidade Neutra ao Risco?", "#CA6F1E"))
story.append(bullet("O risco de uma opção muda a cada nó → usar WACC como taxa "
                    "de desconto é inadequado."))
story.append(bullet("A mudança de medida de probabilidade cria um mundo hipotético "
                    "onde a taxa de desconto única é a taxa livre de risco."))
story.append(bullet("Resultado: é possível descontar os payoffs de qualquer opção "
                    "pela taxa livre de risco, independentemente do risco intrínseco."))
story.append(sp(10))

story.append(h2b("5.4  Black-Scholes para Opções Reais", "#CA6F1E"))
story.append(FormulaBox([
    "Opção de Expansão (call):  c = S₀·N(d₁) – K·e^(–rT)·N(d₂)",
    "Opção de Abandono  (put):  p = K·e^(–rT)·[1–N(d₂)] – S₀·[1–N(d₁)]",
    "",
    "  d₁ = [ln(S₀/K) + (r + σ²/2)·T] / (σ√T)",
    "  d₂ = d₁ – σ√T",
    "",
    "  S₀ = VP dos fluxos do projeto (ex-CAPEX inicial)",
    "  K  = custo do investimento futuro (preço de exercício)",
    "  σ  = volatilidade (use proxy setorial se necessário)",
    "  r  = taxa livre de risco (capitalização contínua)",
    "  T  = tempo até o vencimento (em anos)",
]))
story.append(sp(10))

story.append(h2b("5.5  Sensibilidade do Valor da Opção", "#CA6F1E"))
story.append(two_col_table([
    ("S₀ ↑ (ativo objeto sobe)",   "Call ↑   |   Put ↓"),
    ("K ↑ (preço de exercício sobe)","Call ↓   |   Put ↑"),
    ("σ ↑ (volatilidade aumenta)", "Call ↑   |   Put ↑"),
    ("T ↑ (mais tempo p/ exercer)","Call ↑   |   Put ↑"),
    ("r ↑ (juros sobem)",          "Call ↑   |   Put ↓"),
], "Parâmetro", "Efeito sobre a Opção"))
story.append(sp(10))

story.append(h2b("5.6  Exemplos Setoriais", "#CA6F1E"))
story.append(bullet("<b>Cinema:</b> 1º filme = opção de expansão. Sequência só "
                    "produzida se o original for bem recebido. Preferência por "
                    "franquias (menor incerteza de demanda)."))
story.append(bullet("<b>Farma:</b> cada fase de P&D é análoga a uma call — custo "
                    "atual = prêmio; custo das fases seguintes = preço de exercício."))
story.append(bullet("<b>Construção:</b> opção de abandono com venda a concorrente "
                    "= put com preço de exercício = valor de venda."))
story.append(sp(10))

story.append(example_box("Opção de Abandono — Planta de Ração em Ribeirão Preto", [
    ("Dados:", "u = 1,5  |  d = 0,5  |  rf = 5% a.a.  |  CAPEX = $ 1.000"),
    ("",       "Preço de exercício (venda p/ concorrente) = $ 700  |  data: t₁"),
    ("Prob. neutra ao risco:",
     "q = (1,05 – 0,5) / (1,5 – 0,5)  =  0,55  (55%)"),
    ("VPL sem opção (A):",
     "Descontado a WACC = 30%; resultado negativo."),
    ("VPL com opção (B):",
     "No cenário adverso, a empresa exerce a put e vende por $ 700."),
    ("Valor da Opção:",
     "VPL_B – VPL_A = valor econômico da flexibilidade de abandono."),
], ORANGE))
story.append(sp(10))

story.append(self_check([
    "Por que o VPL tradicional subestima projetos com flexibilidade gerencial?",
    "Por que não podemos usar o WACC para descontar os payoffs de uma opção real?",
    "O que é a probabilidade neutra ao risco e como ela simplifica o cálculo?",
    "Aumento da volatilidade aumenta ou reduz o valor de uma opção de abandono? Por quê?",
    "Explique a analogia entre P&D farmacêutico e uma sequência de opções de compra.",
]))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 6
# ══════════════════════════════════════════════════════════════════════════════
story.append(ModuleHeader(6, "CRIAÇÃO DE VALOR & AVALIAÇÃO RELATIVA",
                          "Transversal | Complementar ao DCF", RED))
story.append(sp(12))

story.append(h2b("6.1  Fontes de Criação de Valor", "#922B21"))
story.append(two_col_table([
    ("Eficiência operacional",   "Margem ↑, giro ↑ ou alavancagem → ROE maior."),
    ("Novos projetos (VPL > 0)", "TIR do projeto > WACC: valor criado para o acionista."),
    ("Estrutura de capital",     "Benefício fiscal da dívida sem comprometer saúde financeira."),
    ("M&A / Sinergias",          "Ganhos de custo e mercado → geração de caixa incremental."),
], "Alavanca", "Mecanismo"))
story.append(sp(8))

story.append(h2b("6.2  Decomposição do ROE (DuPont)", "#922B21"))
story.append(FormulaBox([
    "ROE = Margem Líquida × Giro do Ativo × Multiplicador do PL",
    "",
    "  Margem Líquida  = Lucro Líquido / Receita",
    "  Giro do Ativo   = Receita / Ativo Total",
    "  Multiplicador   = Ativo Total / PL   (alavancagem financeira)",
]))
story.append(sp(8))

story.append(h2b("6.3  Caso Mobly & Tok&Stok (agosto/2024)", "#922B21"))
story.append(bullet("<b>Sinergias operacionais:</b> tecnologia/logística da Mobly + "
                    "desenvolvimento de produto da Tok&Stok → Bain&Co estimou "
                    "+R$ 80–135 MM de caixa/ano em 5 anos."))
story.append(bullet("<b>Estrutura de capital:</b> Mobly (caixa R$ 185 MM) assume "
                    "dívida de R$ 450 MM da Tok&Stok, avaliada a 10% do pico histórico."))
story.append(bullet("<b>Earn-Out:</b> troca de ações com lock-up de 24 meses."))
story.append(sp(8))

story.append(h2b("6.4  Avaliação Relativa — Múltiplos", "#922B21"))
story.append(two_col_table([
    ("EV/EBITDA",  "Enterprise Value / EBITDA. Neutro à estrutura de capital."),
    ("P/L (P/E)",  "Preço / Lucro. Reflete expectativas de crescimento."),
    ("P/VPA",      "Preço / Valor Patrimonial. Relevante para bancos e financeiras."),
    ("EV/Receita", "Usado em empresas pré-lucro ou de alto crescimento."),
], "Múltiplo", "Aplicação"))
story.append(Paragraph(
    '<i>Premissa central: "ativos semelhantes devem valer o mesmo." '
    'Risco: múltiplos embitem o otimismo ou pessimismo do momento.</i>', sNote))
story.append(sp(10))

story.append(self_check([
    "Em que condições um novo projeto cria valor para o acionista?",
    "Como o benefício fiscal da dívida pode criar e, ao mesmo tempo, destruir valor?",
    "Quais os riscos de usar exclusivamente múltiplos para avaliar uma empresa?",
    "Como as sinergias de uma fusão devem aparecer no valuation do alvo?",
]))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 7
# ══════════════════════════════════════════════════════════════════════════════
story.append(ModuleHeader(7, "REVISÃO GERAL E EXERCÍCIO INTEGRADO",
                          "Semana Pré-Avaliação", GOLD))
story.append(sp(12))

story.append(h2b("7.1  Checklist de Valuation — DCF Completo", "#B7950B"))

checklist_items = [
    "[ ]  Calculei o FCFF atual e eliminei itens não recorrentes?",
    "[ ]  O FCFF é uma base razoável para extrapolação?",
    "[ ]  A taxa de crescimento de longo prazo é compatível com o PIB potencial?",
    "[ ]  Calculei Ke pelo CAPM usando NTN-B 10a e ERP de 5,5%?",
    "[ ]  Usei o beta adequado (histórico ou bottom-up realavancado)?",
    "[ ]  Calculei o Kd líquido de IR/CSLL?",
    "[ ]  Usei pesos do WACC a valor de MERCADO?",
    "[ ]  Identifiquei e ajustei impairments, provisões e ARO relevantes?",
    "[ ]  Verifiquei POC e hedge accounting nos ajustes de receita?",
    "[ ]  Considerei opções reais relevantes (expansão, abandono, adiamento)?",
    "[ ]  Realizei análise de sensibilidade (variando g e WACC)?",
    "[ ]  Comparei o resultado com múltiplos de mercado (sanity check)?",
]
chk_data = [[Paragraph(item, sTableCell)] for item in checklist_items]
t_chk = Table([[Paragraph("<b>✔ CHECKLIST</b>", sTableHdr)]] + chk_data,
              colWidths=[16.5*cm])
t_chk.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0), GOLD),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[LIGHTYELL, WHITE]),
    ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#F0D060")),
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ("RIGHTPADDING",  (0,0), (-1,-1), 10),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
]))
story.append(t_chk)
story.append(sp(10))

story.append(h2b("7.2  Mapa de Conexões", "#B7950B"))
story.append(two_col_table([
    ("FCFF ↑",               "Valor do DCF ↑   (ceteris paribus)"),
    ("WACC ↑",               "Valor do DCF ↓   (ceteris paribus)"),
    ("g de longo prazo ↑",   "Valor Terminal ↑ → maior sensibilidade ao WACC"),
    ("Beta (β) ↑",           "Ke ↑ → WACC ↑ → VPL ↓"),
    ("Alavancagem ↑",        "Kd(1–t) mais barato; mas risco financeiro ↑"),
    ("Volatilidade (σ) ↑",   "Opções Reais ↑ (tanto call quanto put)"),
    ("Impairment",           "Sem efeito direto no FCFF; revisar premissas de crescimento"),
    ("POC antecipado",       "Receita contábil ≠ caixa. FCFF não é diretamente afetado"),
], "Variável / Evento", "Efeito no Valuation"))
story.append(sp(10))

story.append(h2b("7.3  Exercício Integrado — Empresa ABC (Logística)", "#B7950B"))
story.append(Paragraph("Calcule FCFF, Ke, WACC, Valor Terminal e discuta opções reais.", sBody))
story.append(sp(4))
story.append(two_col_table([
    ("EBIT",               "R$ 50 MM"),
    ("Depreciação",        "R$ 8 MM"),
    ("Receita não recorr.","R$ 3 MM"),
    ("IR sobre EBIT",      "R$ 15 MM"),
    ("CAPEX",              "R$ 12 MM"),
    ("ΔNCG",               "R$ 4 MM"),
    ("Beta (histórico)",   "0,85"),
    ("NTN-B 10a",          "7,5% a.a."),
    ("ERP",                "5,5% a.a."),
    ("Kd bruto",           "11,0% a.a."),
    ("Alíquota IR/CSLL",   "34%"),
    ("E/(D+E)",            "60%"),
    ("g real longo prazo", "3,0% a.a."),
], "Dado", "Valor", [6*cm, 10*cm]))
story.append(sp(8))

story.append(example_box("Gabarito — Empresa ABC", [
    ("FCFF:",   "50 + 8 – 3 – 15 – 12 – 4  =  R$ 24 MM"),
    ("Ke:",     "7,5 + 0,85 × 5,5  =  12,175% a.a."),
    ("Kd líq.:","11,0 × (1 – 0,34)  =  7,26% a.a."),
    ("WACC:",   "0,60 × 12,175 + 0,40 × 7,26  =  10,21% a.a."),
    ("V.T.:",   "FCFF × (1+g) / (WACC – g)  =  24 × 1,03 / (0,1021 – 0,03)  ≈  R$ 343 MM"),
    ("Opções:", "Existe opção real de expansão (nova rota/terminal logístico)?"),
    ("",        "Se σ do VPL ≈ σ do preço de celulose/frete, calcule o valor da call."),
], GOLD))
story.append(sp(10))

story.append(h2b("7.4  Dicas para os Estudos Dirigidos e Seminário", "#B7950B"))
story.append(bullet("Leia sempre as notas explicativas do ITR/DFP (contingências, "
                    "impairment, segmentos, hedge)."))
story.append(bullet("Em estudos de caso, justifique todos os ajustes ao FCFF."))
story.append(bullet("<b>Seminário:</b> 8 slides. Os 2 primeiros contextualizam o artigo "
                    "e explicitam a questão de pesquisa. Upload até quinta-feira "
                    "anterior às 23h59."))
story.append(bullet("Nota final = 60% (Estudos Dirigidos, excl. pior nota) + "
                    "40% (Seminário). Mínimo 6,0 para aprovação."))
story.append(sp(6))
story.append(divider(GOLD))
story.append(Paragraph(
    "Fluxo de Estudo elaborado com base nos Slides das Aulas 1–8 — "
    "Avaliação de Empresas — Mestrado Profissional em Economia — "
    "Prof. Sérgio Jurandyr Machado",
    sFooter))

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
OUTPUT = "/home/user/estado-economia-dashboard/Fluxo_de_Estudo_Avaliacao_de_Empresas.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=2.5*cm,
    rightMargin=2.5*cm,
    topMargin=1.8*cm,
    bottomMargin=1.8*cm,
    title="Fluxo de Estudo — Avaliação de Empresas",
    author="Prof. Sérgio Jurandyr Machado",
)

# Primeira página usa template de capa; demais usam header/footer
def first_page(canvas, doc):
    _cover_template(canvas, doc)

def later_pages(canvas, doc):
    _header_footer(canvas, doc)

doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
print(f"PDF gerado: {OUTPUT}")
