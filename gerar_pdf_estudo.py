"""
Fluxo de Estudo — Avaliação de Empresas
Design minimalista: tipografia limpa, muito espaço em branco, uma única cor de acento.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.platypus.flowables import Flowable

W, H = A4

# ── Paleta minimalista ─────────────────────────────────────────────────────────
ACCENT  = colors.HexColor("#1A1A1A")   # quase preto — texto principal
MUTED   = colors.HexColor("#6B7280")   # cinza médio — texto secundário
LIGHT   = colors.HexColor("#F3F4F6")   # cinza levíssimo — fundos
RULE    = colors.HexColor("#E5E7EB")   # linha divisória
INK     = colors.HexColor("#111827")   # título principal
BLUE    = colors.HexColor("#2563EB")   # único acento de cor (links, destaque)
WHITE   = colors.white

MOD_LABELS = ["01","02","03","04","05","06","07"]

# ── Estilos ────────────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

# Corpo
sBody = S("body", fontSize=10, leading=16, textColor=ACCENT,
          fontName="Helvetica", spaceAfter=4, alignment=TA_JUSTIFY)
sMuted = S("muted", fontSize=9, leading=14, textColor=MUTED,
           fontName="Helvetica-Oblique", spaceAfter=3)
sBullet = S("bullet", fontSize=10, leading=15, textColor=ACCENT,
            fontName="Helvetica", leftIndent=14, firstLineIndent=-10,
            spaceAfter=3)
sBullet2 = S("bullet2", fontSize=9.5, leading=14, textColor=MUTED,
             fontName="Helvetica", leftIndent=26, firstLineIndent=-10,
             spaceAfter=2)

# Cabeçalhos
sH1 = S("h1", fontSize=22, leading=28, textColor=INK,
        fontName="Helvetica-Bold", spaceBefore=0, spaceAfter=4,
        alignment=TA_LEFT)
sH2 = S("h2", fontSize=13, leading=17, textColor=INK,
        fontName="Helvetica-Bold", spaceBefore=16, spaceAfter=4)
sH3 = S("h3", fontSize=10.5, leading=14, textColor=MUTED,
        fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=3)

# Fórmula
sCode = S("code", fontSize=9.5, leading=15, textColor=INK,
          fontName="Courier", leftIndent=16, spaceAfter=2)
sCodeMuted = S("codem", fontSize=9, leading=14, textColor=MUTED,
               fontName="Courier", leftIndent=20, spaceAfter=1)

# Tabelas
sTHdr = S("thdr", fontSize=9, leading=12, textColor=MUTED,
          fontName="Helvetica-Bold", alignment=TA_LEFT)
sTCell = S("tcell", fontSize=9.5, leading=13, textColor=ACCENT,
           fontName="Helvetica", alignment=TA_LEFT)

# Capa
sCoverNum = S("covn", fontSize=72, leading=80, textColor=INK,
              fontName="Helvetica-Bold", alignment=TA_LEFT)
sCoverTitle = S("covt", fontSize=28, leading=34, textColor=INK,
                fontName="Helvetica-Bold", alignment=TA_LEFT)
sCoverSub = S("covs", fontSize=13, leading=18, textColor=MUTED,
              fontName="Helvetica", alignment=TA_LEFT)

# Footer / header
sPageNum = S("pg", fontSize=8, leading=10, textColor=MUTED,
             fontName="Helvetica", alignment=TA_RIGHT)
sRunHead = S("rh", fontSize=8, leading=10, textColor=MUTED,
             fontName="Helvetica-Bold", alignment=TA_LEFT)

# Autoavaliação
sQLabel = S("ql", fontSize=8.5, leading=11, textColor=MUTED,
            fontName="Helvetica-Bold", spaceAfter=2)
sQText  = S("qt", fontSize=10, leading=14, textColor=ACCENT,
            fontName="Helvetica", leftIndent=0, spaceAfter=2)
sQLine  = S("qln", fontSize=9, leading=11, textColor=RULE,
            fontName="Helvetica", leftIndent=0, spaceAfter=8)

# ── Flowables customizados ─────────────────────────────────────────────────────

class ThinRule(Flowable):
    """Linha divisória fina."""
    def __init__(self, color=RULE, width=None, thickness=0.5,
                 space_before=6, space_after=6):
        Flowable.__init__(self)
        self._color = color
        self._w = width
        self._t = thickness
        self._sb = space_before
        self._sa = space_after
    def wrap(self, aw, ah):
        self.width = self._w or aw
        self.height = self._t + self._sb + self._sa
        return self.width, self.height
    def draw(self):
        self.canv.setStrokeColor(self._color)
        self.canv.setLineWidth(self._t)
        self.canv.line(0, self._sa, self.width, self._sa)


class LeftBar(Flowable):
    """Barra vertical à esquerda (marca de seção)."""
    def __init__(self, content_height, color=ACCENT, width=2):
        Flowable.__init__(self)
        self._h = content_height
        self._color = color
        self._bw = width
    def wrap(self, aw, ah):
        self.width = self._bw + 4
        self.height = self._h
        return self.width, self.height
    def draw(self):
        self.canv.setFillColor(self._color)
        self.canv.rect(0, 0, self._bw, self._h, fill=1, stroke=0)


class ModTag(Flowable):
    """Número do módulo + título em estilo minimalista."""
    def __init__(self, number, title, subtitle):
        Flowable.__init__(self)
        self._n = str(number).zfill(2)
        self._title = title
        self._sub = subtitle
    def wrap(self, aw, ah):
        self.width = aw
        self.height = 70
        return self.width, self.height
    def draw(self):
        c = self.canv
        w = self.width
        # Número grande e leve
        c.setFillColor(RULE)
        c.setFont("Helvetica-Bold", 52)
        c.drawString(0, 12, self._n)
        # Título
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(72, 36, self._title)
        # Subtítulo
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 9)
        c.drawString(73, 22, self._sub)
        # Linha fina abaixo
        c.setStrokeColor(RULE)
        c.setLineWidth(0.5)
        c.line(0, 6, w, 6)


class FormulaBlock(Flowable):
    """Bloco de código/fórmula com borda esquerda."""
    def __init__(self, lines, width=None):
        Flowable.__init__(self)
        self._lines = lines
        self._w = width
        self._pad = 10
        self._lh  = 14
    def wrap(self, aw, ah):
        self.width = self._w or aw
        non_empty = sum(1 for l in self._lines if l)
        blank     = sum(1 for l in self._lines if not l)
        self.height = non_empty * self._lh + blank * 6 + 2 * self._pad
        return self.width, self.height
    def draw(self):
        c = self.canv
        w, h = self.width, self.height
        # Fundo suave
        c.setFillColor(LIGHT)
        c.roundRect(0, 0, w, h, 3, fill=1, stroke=0)
        # Barra esquerda
        c.setFillColor(ACCENT)
        c.rect(0, 0, 2.5, h, fill=1, stroke=0)
        # Texto
        y = h - self._pad - 10
        for line in self._lines:
            if not line:
                y -= 6
                continue
            if line.startswith("  ") or line.startswith("→"):
                c.setFillColor(MUTED)
                c.setFont("Courier", 9)
            elif line.startswith("══") or line.startswith("──"):
                c.setFillColor(RULE)
                c.setFont("Courier", 8)
            else:
                c.setFillColor(INK)
                c.setFont("Courier-Bold", 9.5)
            c.drawString(12, y, line)
            y -= self._lh


# ── Helpers ────────────────────────────────────────────────────────────────────

def sp(n=8):
    return Spacer(1, n)

def rule(thick=False):
    return ThinRule(RULE if not thick else MUTED,
                    thickness=1 if thick else 0.5,
                    space_before=4, space_after=4)

def h2(text):
    return Paragraph(text, sH2)

def h3(text):
    return Paragraph(text, sH3)

def body(text):
    return Paragraph(text, sBody)

def muted(text):
    return Paragraph(text, sMuted)

def bullet(text, level=0):
    mark = "—" if level == 0 else "·"
    style = sBullet if level == 0 else sBullet2
    return Paragraph(f"{mark}  {text}", style)

def tbl(rows, headers=None, col_widths=None):
    """Tabela minimalista sem bordas pesadas."""
    cw = col_widths or [5*cm, 11.5*cm]
    data = []
    if headers:
        data.append([Paragraph(h, sTHdr) for h in headers])
    for row in rows:
        data.append([Paragraph(str(c), sTCell) for c in row])

    t = Table(data, colWidths=cw)
    style_cmds = [
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("LINEBELOW",    (0,0), (-1,-1), 0.3, RULE),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[WHITE, LIGHT]),
    ]
    if headers:
        style_cmds += [
            ("LINEBELOW",    (0,0), (-1,0), 1, MUTED),
            ("BACKGROUND",   (0,0), (-1,0), WHITE),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, LIGHT]),
        ]
    t.setStyle(TableStyle(style_cmds))
    return t

def summary(title, items):
    """Bloco de resumo com fundo leve."""
    rows = [[Paragraph(f"<b>{k}</b>", sTHdr),
             Paragraph(v, sTCell)] for k, v in items]
    data = [[Paragraph(title, S("sh", fontSize=9, leading=12,
                                fontName="Helvetica-Bold", textColor=MUTED)),
             Paragraph("", sTCell)]] + rows
    t = Table(data, colWidths=[5*cm, 11.5*cm])
    t.setStyle(TableStyle([
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("BACKGROUND",   (0,0), (-1,-1), LIGHT),
        ("LINEBELOW",    (0,0), (-1,-1), 0.3, RULE),
        ("SPAN",         (0,0), (-1,0)),
        ("LINEBELOW",    (0,0), (-1,0), 0.8, MUTED),
    ]))
    return t

def example(title, items):
    """Bloco de exemplo com linha azul à esquerda."""
    rows = [[Paragraph(f"<b>{k}</b>" if k else "", sTHdr),
             Paragraph(v, sTCell)] for k, v in items]
    data = [[Paragraph(f"↳  {title}", S("et", fontSize=9, leading=12,
                                         fontName="Helvetica-Bold",
                                         textColor=BLUE)),
             Paragraph("", sTCell)]] + rows
    t = Table(data, colWidths=[5*cm, 11.5*cm])
    t.setStyle(TableStyle([
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("BACKGROUND",   (0,0), (-1,-1), WHITE),
        ("LINEBELOW",    (0,0), (-1,-1), 0.3, RULE),
        ("SPAN",         (0,0), (-1,0)),
        ("LINEAFTER",    (0,0), (0,-1), 2, BLUE),
        ("LINEBEFORE",   (0,0), (0,-1), 2, BLUE),
        ("LINEABOVE",    (0,0), (-1,0), 0.8, RULE),
        ("LINEBELOW",    (0,-1),(-1,-1), 0.8, RULE),
    ]))
    return t

def self_check(questions):
    rows = []
    for i, q in enumerate(questions, 1):
        rows.append(Paragraph(f"<b>{i}.</b>  {q}", sQText))
        rows.append(Paragraph("_" * 95, sQLine))
    outer = [[r] for r in rows]
    header = [[Paragraph("AUTOAVALIAÇÃO", S("ach", fontSize=8,
                          fontName="Helvetica-Bold", textColor=MUTED))]]
    t = Table(header + outer, colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 1),
        ("LINEABOVE",    (0,0), (-1,0), 1, ACCENT),
        ("TOPPADDING",   (0,0), (-1,0), 6),
        ("BOTTOMPADDING",(0,0), (-1,0), 6),
    ]))
    return t


# ── Header / Footer ────────────────────────────────────────────────────────────

RUNNING_MOD = [""]   # estado mutável para o header

def _on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    # Header: linha + texto
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, h - 1.4*cm, w - 2*cm, h - 1.4*cm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(2*cm, h - 1.15*cm, "Avaliação de Empresas — Fluxo de Estudo")
    canvas.drawRightString(w - 2*cm, h - 1.15*cm,
                           f"Prof. Sérgio Jurandyr Machado")
    # Footer
    canvas.line(2*cm, 1.4*cm, w - 2*cm, 1.4*cm)
    canvas.drawRightString(w - 2*cm, 0.9*cm, str(doc.page))
    canvas.restoreState()

def _cover_page(canvas, doc):
    # sem header/footer na capa
    pass


# ══════════════════════════════════════════════════════════════════════════════
# CONTEÚDO
# ══════════════════════════════════════════════════════════════════════════════
story = []

# ── CAPA ──────────────────────────────────────────────────────────────────────
story += [
    sp(3.5*cm),
    Paragraph("Fluxo de Estudo", S("cvl", fontSize=11, leading=14,
              fontName="Helvetica", textColor=MUTED)),
    sp(6),
    Paragraph("Avaliação<br/>de Empresas",
              S("cvT", fontSize=38, leading=46, fontName="Helvetica-Bold",
                textColor=INK)),
    sp(14),
    ThinRule(ACCENT, thickness=1.5, space_before=0, space_after=0),
    sp(14),
    Paragraph("Mestrado Profissional em Economia<br/>"
              "Prof. Sérgio Jurandyr Machado",
              S("cvs2", fontSize=11, leading=18, fontName="Helvetica",
                textColor=MUTED)),
    sp(40),
]

# Índice
story.append(Paragraph("MÓDULOS", S("idxH", fontSize=8, fontName="Helvetica-Bold",
                                     textColor=MUTED, spaceAfter=8)))
modulos = [
    ("01", "Fundamentos do Valuation",                 "Aula 1"),
    ("02", "Fluxo de Caixa Livre — FCFF",              "Aulas 2–4"),
    ("03", "Taxa de Desconto — WACC",                  "Aulas 2–4"),
    ("04", "Ajustes Contábeis para Valuation",         "Aulas 5–6"),
    ("05", "Opções Reais e Valor da Flexibilidade",    "Aulas 7–8"),
    ("06", "Criação de Valor & Avaliação Relativa",    "Transversal"),
    ("07", "Revisão Geral e Exercício Integrado",      "Pré-Prova"),
]
idx_rows = []
for num, title, ref in modulos:
    idx_rows.append([
        Paragraph(f"<font color='#6B7280'>{num}</font>",
                  S("in", fontSize=9, fontName="Helvetica-Bold",
                    textColor=MUTED, alignment=TA_LEFT)),
        Paragraph(title,
                  S("it", fontSize=10, fontName="Helvetica", textColor=ACCENT)),
        Paragraph(ref,
                  S("ir", fontSize=9, fontName="Helvetica",
                    textColor=MUTED, alignment=TA_RIGHT)),
    ])
t_idx = Table(idx_rows, colWidths=[1.2*cm, 12*cm, 3.3*cm])
t_idx.setStyle(TableStyle([
    ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ("LEFTPADDING",  (0,0), (-1,-1), 0),
    ("RIGHTPADDING", (0,0), (-1,-1), 0),
    ("TOPPADDING",   (0,0), (-1,-1), 5),
    ("BOTTOMPADDING",(0,0), (-1,-1), 5),
    ("LINEBELOW",    (0,0), (-1,-1), 0.3, RULE),
]))
story.append(t_idx)
story.append(PageBreak())


# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 1
# ══════════════════════════════════════════════════════════════════════════════
story += [ModTag(1, "Fundamentos do Valuation", "Aula 1"), sp(16)]

story += [h2("O que é Valuation?"),
          body("Valuation é o processo de conversão de uma projeção em uma estimativa "
               "do <b>valor</b> de uma empresa ou de um ativo. É fundamental distinguir "
               "<b>preço</b> (o que o mercado cobra hoje) de <b>valor</b> "
               "(o que o ativo vale com base nos fundamentos)."),
          sp(4),
          tbl([("DCF / FCD",          "Valor = VP dos fluxos de caixa futuros esperados."),
               ("Avaliação Relativa", "Compara a empresa a pares via múltiplos (EV/EBITDA, P/L…).")],
              headers=["Método", "Lógica"]),
          sp(14)]

story += [h2("Tese de Investimento"),
          muted('"O preço de um ativo converge para o seu valor justo."'),
          sp(4),
          tbl([("Long",        "Compra ativo subavaliado — preço < valor justo."),
               ("Short",       "Vende ativo superavaliado — preço > valor justo."),
               ("Long & Short","Opera nos dois sentidos simultaneamente.")],
              headers=["Estratégia", "Lógica"]),
          sp(14)]

story += [h2("Eficiência de Mercado"),
          bullet("HME semi-forte: toda informação pública é incorporada instantaneamente ao preço."),
          bullet("AMH: convergência pode ser lenta por fricções (custos de transação, "
                 "restrições à venda a descoberto) ou pelo noise trader."),
          bullet('<i>"Gerar alfa é mais difícil do que ganhar as Olimpíadas."</i>'),
          sp(16)]

story += [rule(),
          summary("Conceitos-chave", [
              ("Definição",        "Valuation = conversão de projeção em estimativa de valor."),
              ("Premissa DCF",     "Valor ≈ capacidade de geração de caixa futuro."),
              ("HME semi-forte",   "Informação pública → preço imediatamente."),
              ("Objetivo",         "Identificar o desvio entre preço e valor (gerar alfa)."),
          ]),
          sp(20)]

story += [self_check([
    "Qual a diferença entre preço e valor de um ativo?",
    "O que é a HME semi-forte? E a AMH?",
    "Quais as três perguntas centrais do método DCF?",
    "Por que gerar alfa é considerado tão difícil?",
])]

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 2
# ══════════════════════════════════════════════════════════════════════════════
story += [ModTag(2, "Fluxo de Caixa Livre — FCFF", "Aulas 2–4 · Pergunta 1 do DCF"),
          sp(16)]

story += [h2("As Três Perguntas do DCF"),
          tbl([("1", "Qual o montante líquido de caixa gerado pelas atividades "
                     "operacionais e como se distribui no tempo?"),
               ("2", "Qual deve ser a taxa de desconto?"),
               ("3", "Qual é o horizonte de análise (Valor Terminal)?")],
              headers=["#", "Questão"], col_widths=[0.8*cm, 15.7*cm]),
          sp(14)]

story += [h2("Cálculo do FCFF — Pergunta 1.a"),
          FormulaBlock([
              "EBIT",
              "(+) Depreciação e Amortização",
              "(=) EBITDA                    [Resolução CVM 156/2022]",
              "(+/–) Ajustes de itens não recorrentes",
              "(=) EBITDA Ajustado",
              "(–) IR/CSLL estimado sobre o EBIT",
              "(–) CAPEX",
              "(–) Variação da NCG",
              "══════════════════════════════════════════",
              "(=) FCFF em t",
          ]),
          sp(14)]

story += [h2("CAPEX vs. OPEX"),
          tbl([("CAPEX", "Investimento que gera receita adicional, aumenta vida útil "
                          "ou expande capacidade. Concentrado no tempo. Tratado separadamente no DCF."),
               ("OPEX",  "Gasto recorrente do dia a dia. Capturado no EBIT.")],
              headers=["Tipo", "Características"]),
          sp(14)]

story += [h2("Necessidade de Capital de Giro (NCG)"),
          FormulaBlock([
              "NCG = Estoques + Contas a Receber – Fornecedores",
              "",
              "Ciclo Financeiro = PME + PMR – PMP   (em dias de receita de vendas)",
              "  PME — Prazo Médio de Estoques      → menor é melhor",
              "  PMR — Prazo Médio de Recebimento   → menor é melhor",
              "  PMP — Prazo Médio de Pagamento     → maior é melhor",
          ]),
          sp(14)]

story += [h2("Taxa de Crescimento Esperada — Pergunta 1.c"),
          FormulaBlock([
              "g = ROIC × (CAPEX Líquido + ΔNCG) / NOPAT",
              "  ou",
              "g = Lucro Retido × ROE",
              "",
              "⚠  g de longo prazo ≤ PIB Potencial ± ajustes de eficiência",
          ]),
          sp(16)]

story += [rule(),
          example("Empresa XYZ — Polímeros Condutores", [
              ("Dados",      "EBIT R$20MM · D&A R$1,5MM · IR R$6,8MM · "
                             "Receita não recorrente R$5,2MM · ΔNCG R$1MM · CAPEX R$2MM"),
              ("FCFF 2025",  "20,0 + 1,5 – 5,2 – 6,8 – 1,0 – 2,0  =  R$ 6,5 MM"),
              ("FCFF 2026",  "R$ 6,5 MM × 1,02  =  R$ 6,63 MM   (crescimento real de 2%)"),
          ]),
          sp(20)]

story += [self_check([
    "Qual a diferença entre EBITDA e FCFF?",
    "Por que subtraímos CAPEX e ΔNCG no cálculo do FCFF?",
    "Por que adicionamos depreciação de volta ao EBIT?",
    "Como itens não recorrentes afetam a extrapolação?",
    "Qual o risco de projetar g acima do PIB potencial no longo prazo?",
])]

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 3
# ══════════════════════════════════════════════════════════════════════════════
story += [ModTag(3, "Taxa de Desconto — WACC", "Aulas 2–4 · Pergunta 2 do DCF"),
          sp(16)]

story += [h2("Custo de Capital Próprio (Ke) — CAPM"),
          FormulaBlock([
              "Ke  =  Rf  +  βi × (Rm – Rf)",
              "",
              "  Rf      = Taxa livre de risco",
              "  βi      = Beta da empresa i (risco relativo ao mercado)",
              "  Rm – Rf = Prêmio de risco de mercado (ERP)",
          ]),
          sp(14)]

story += [h2("Taxa Livre de Risco e ERP"),
          tbl([("Rf (Brasil)",    "NTN-B Principal vencimento ~10 anos (taxa real). "
                                  "Já embute o risco-país.  →  Ke = Rf + βi × 5,5%"),
               ("ERP EUA",        "Média geométrica S&P500 – T.Bonds (1928–2024) ≈ 5,44%. "
                                   "Sugestão do professor: 5,5% a.a."),
               ("CAPM Global",    "Ke = Rf[EUA] + β×(ERP[EUA]+Risco-País) + (INF_BR – INF_EUA). "
                                   "Avaliação em termos nominais.")],
              headers=["Componente", "Detalhes"]),
          sp(14)]

story += [h2("Beta (β)"),
          FormulaBlock([
              "β = Cov(Ri, Rm) / σ²m",
              "",
              "  β < 1  →  menos volátil que o mercado",
              "  β > 1  →  mais volátil que o mercado",
              "",
              "Bottom-Up Beta:",
              "  β_alav = β_desalav × [1 + (1 – t) × (D/E)]",
          ]),
          sp(14)]

story += [h2("Custo de Capital de Terceiros (Kd) e WACC"),
          FormulaBlock([
              "Kd = Rf + SOT                    (spread over treasury)",
              "Kd líquido = Kd × (1 – t)       (benefício fiscal dos juros)",
              "",
              "WACC = [E/(D+E)] × Ke  +  [D/(D+E)] × Kd × (1 – t)",
              "",
              "  Use pesos a valor de MERCADO — não contábil",
          ]),
          sp(16)]

story += [rule(),
          example("Ke — Orizon (ORVR3) e Azul (AZUL4) em 22/10/2025", [
              ("Dados",    "NTN-B 2035 = 7,66% a.a.  |  ERP = 5,5% a.a."),
              ("Orizon",   "β = 0,21  →  Ke = 7,66 + 0,21 × 5,5 = 8,82% a.a."),
              ("Azul",     "β = 1,73  →  Ke = 7,66 + 1,73 × 5,5 = 17,18% a.a."),
              ("Insight",  "Setor aéreo tem risco sistemático muito maior que gestão de resíduos."),
          ]),
          sp(20)]

story += [self_check([
    "Por que o Ke não é diretamente observável?",
    "Por que o Kd é em geral mais barato que o Ke?",
    "O que acontece com o WACC se a empresa aumenta a alavancagem?",
    "Por que usar a NTN-B e não a SELIC como taxa livre de risco real?",
    "O que é um 'bottom-up beta' e quando utilizá-lo?",
])]

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 4
# ══════════════════════════════════════════════════════════════════════════════
story += [ModTag(4, "Ajustes Contábeis para Valuation", "Aulas 5–6 · 'Usual Suspects'"),
          sp(16)]

story += [muted("Estes itens afetam — ou parecem afetar — o FCFF. "
                "Cada um exige análise individual."),
          sp(10)]

story += [h2("Impairment"),
          bullet("Quando Valor Contábil > Valor Recuperável, reconhece-se perda no resultado."),
          bullet("Sem efeito caixa direto → adicionar de volta (como depreciação)."),
          bullet("Mas o mercado reage negativamente: interpreta que os fluxos futuros serão menores."),
          bullet("Revise suas premissas de crescimento sempre que houver impairment relevante."),
          bullet("Casos: Petrobras 2015–2017 (R$ 44,6 bi) · Grupo Soma/Hering (2023–2024)."),
          sp(14)]

story += [h2("Provisões — Contingências Passivas"),
          tbl([("Provável + mensurável",    "Provisionar (best estimate IFRS)."),
               ("Provável + não mensurável","Divulgar em notas explicativas."),
               ("Possível",                 "Divulgar em notas explicativas."),
               ("Remota",                   "Não divulgar.")],
              headers=["Classificação", "Tratamento"]),
          sp(4),
          bullet("<b>Escrow Account:</b> valor retido em conta vinculada; liberado ao "
                 "vendedor se não surgirem contingências do adquirido."),
          bullet("<b>Earn-Out:</b> parcela do preço condicionada a metas. "
                 "Soluciona divergências de expectativas entre comprador e vendedor."),
          sp(14)]

story += [h2("ARO — Obrigação para Desmobilização de Ativos"),
          bullet("Custo futuro de retirada de serviço capitalizado como ativo + provisão idêntica no passivo."),
          bullet("O ativo é depreciado → EBITDA sobe; o pagamento futuro reduz caixa."),
          bullet("Estudo de caso: Vale — compare o balanço do 4T/2018 com o 1T/2019 (Brumadinho)."),
          sp(14)]

story += [h2("POC — Percentage of Completion"),
          bullet("Reconhece receita proporcionalmente ao avanço físico da obra."),
          bullet("IFRS 15: exige transferência progressiva de controle ao cliente."),
          bullet("IASB: POC não é aderente para incorporadoras residenciais no Brasil "
                 "— receita na entrega das chaves."),
          bullet("Para valuation: reconcilie receita contábil com caixa efetivamente recebido."),
          sp(14)]

story += [h2("Hedge Accounting"),
          bullet("Difere variações do instrumento de hedge no patrimônio; reconhece no "
                 "resultado junto com o item objeto."),
          bullet("Caso Petrobras (2013–2015): área técnica da CVM entendeu uso para "
                 "diferir perdas cambiais — Colegiado aceitou o recurso da empresa."),
          sp(16)]

story += [rule(),
          summary("Resumo — impacto no FCFF", [
              ("Impairment",  "Sem efeito caixa. Adicionar de volta. Revisar premissas."),
              ("Provisões",   "Caixa sai no pagamento — não na constituição."),
              ("ARO",         "Depreciação ↑ (EBITDA ↑). Pagamento futuro: caixa ↓."),
              ("POC",         "Receita contábil ≠ caixa recebido. Reconciliar sempre."),
              ("Hedge Acc.",  "Pode distorcer DRE. Analisar o caixa efetivo."),
          ]),
          sp(20)]

story += [self_check([
    "Por que o impairment não afeta o FCFF diretamente, mas afeta o valor percebido?",
    "Qual a diferença entre escrow account e earn-out?",
    "Como uma ARO subestimada pode inflar o valuation?",
    "Em que condições o POC é permitido pelo IFRS 15?",
    "Como identificar se o hedge accounting está diferindo perdas?",
])]

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 5
# ══════════════════════════════════════════════════════════════════════════════
story += [ModTag(5, "Opções Reais e Valor da Flexibilidade",
                 "Aulas 7–8 · VPL Expandido"),
          sp(16)]

story += [h2("Conceito"),
          body("O VPL tradicional ignora o valor das decisões gerenciais futuras. "
               "As opções reais capturam esse <b>valor de flexibilidade</b>:"),
          sp(4),
          FormulaBlock(["VPL Expandido  =  VPL Tradicional  +  Valor das Opções Reais"]),
          sp(8),
          tbl([("Expansão",  "Ampliar o projeto se condições forem favoráveis. → call"),
               ("Abandono",  "Encerrar e recuperar valor residual. → put"),
               ("Adiamento", "Postergar o início até obter mais informação."),
               ("Contração", "Reduzir escala se condições deteriorarem.")],
              headers=["Tipo", "Análogo financeiro"]),
          sp(14)]

story += [h2("Árvore Binomial e Probabilidade Neutra ao Risco"),
          FormulaBlock([
              "Em cada período: ativo sobe (×u) ou cai (×d)",
              "  d = 1/u  →  árvore recombinante",
              "",
              "Probabilidade Neutra ao Risco:",
              "  q = (1 + r – d) / (u – d)",
              "",
              "Valor do nó pai:",
              "  V = [q × V_sobe + (1–q) × V_desce] / (1 + r)",
              "",
              "  → Descontar pela taxa livre de risco, não pelo WACC",
          ]),
          sp(14)]

story += [h2("Black-Scholes para Opções Reais"),
          FormulaBlock([
              "Call (expansão): c = S₀·N(d₁) – K·e^(–rT)·N(d₂)",
              "Put  (abandono): p = K·e^(–rT)·[1–N(d₂)] – S₀·[1–N(d₁)]",
              "",
              "  d₁ = [ln(S₀/K) + (r + σ²/2)·T] / (σ√T)",
              "  d₂ = d₁ – σ√T",
              "",
              "  S₀ = VP dos fluxos do projeto (ex-CAPEX inicial)",
              "  K  = custo do investimento futuro (preço de exercício)",
              "  σ  = volatilidade do ativo objeto (use proxy setorial)",
          ]),
          sp(14)]

story += [h2("Sensibilidade do Valor da Opção"),
          tbl([("S₀ ↑",  "Call ↑   |   Put ↓"),
               ("K ↑",   "Call ↓   |   Put ↑"),
               ("σ ↑",   "Call ↑   |   Put ↑   (volatilidade sempre aumenta o valor)"),
               ("T ↑",   "Call ↑   |   Put ↑"),
               ("r ↑",   "Call ↑   |   Put ↓")],
              headers=["Parâmetro", "Efeito"]),
          sp(16)]

story += [rule(),
          example("Opção de Abandono — Planta de Ração", [
              ("Dados",      "u=1,5 · d=0,5 · rf=5% a.a. · CAPEX=$1.000 · Preço exercício=$700 em t₁"),
              ("q",          "(1,05 – 0,5) / (1,5 – 0,5)  =  0,55"),
              ("Sem opção",  "VPL_A descontado a WACC=30% → resultado negativo."),
              ("Com opção",  "No cenário adverso, a empresa exerce a put e vende por $700."),
              ("Valor opt.", "VPL_B – VPL_A = valor econômico da flexibilidade de abandono."),
          ]),
          sp(20)]

story += [self_check([
    "Por que o VPL tradicional subestima projetos com flexibilidade gerencial?",
    "Por que não podemos usar o WACC para descontar os payoffs de uma opção real?",
    "O que é a probabilidade neutra ao risco e como ela simplifica o cálculo?",
    "Aumento da volatilidade aumenta ou reduz o valor de uma opção de abandono? Por quê?",
    "Explique a analogia entre P&D farmacêutico e opções de compra sequenciais.",
])]

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 6
# ══════════════════════════════════════════════════════════════════════════════
story += [ModTag(6, "Criação de Valor & Avaliação Relativa",
                 "Transversal"),
          sp(16)]

story += [h2("Fontes de Criação de Valor"),
          tbl([("Eficiência",    "Margem ↑, giro ↑ ou alavancagem → ROE maior."),
               ("Novos projetos","TIR > WACC → VPL positivo → valor criado."),
               ("Estrutura cap.","Benefício fiscal da dívida sem comprometer saúde financeira."),
               ("M&A",          "Sinergias operacionais e tributárias → caixa incremental.")],
              headers=["Alavanca", "Mecanismo"]),
          sp(14)]

story += [h2("Decomposição do ROE — DuPont"),
          FormulaBlock([
              "ROE = Margem Líquida × Giro do Ativo × Multiplicador do PL",
              "",
              "  Margem Líquida = Lucro Líquido / Receita",
              "  Giro do Ativo  = Receita / Ativo Total",
              "  Multiplicador  = Ativo Total / PL",
          ]),
          sp(14)]

story += [h2("Avaliação Relativa — Múltiplos"),
          tbl([("EV/EBITDA",  "Neutro à estrutura de capital. Amplamente usado."),
               ("P/L",        "Reflete expectativas de crescimento do lucro."),
               ("P/VPA",      "Relevante para bancos e financeiras."),
               ("EV/Receita", "Usado em empresas pré-lucro ou de alto crescimento.")],
              headers=["Múltiplo", "Aplicação"]),
          muted('"Ativos semelhantes devem valer o mesmo." '
                'Risco: múltiplos embitem o otimismo do momento.'),
          sp(20)]

story += [self_check([
    "Em que condições um novo projeto cria valor para o acionista?",
    "Como o benefício fiscal da dívida pode criar e destruir valor ao mesmo tempo?",
    "Quais os riscos de usar exclusivamente múltiplos para avaliar uma empresa?",
    "Como as sinergias de uma fusão devem aparecer no valuation do alvo?",
])]

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 7
# ══════════════════════════════════════════════════════════════════════════════
story += [ModTag(7, "Revisão Geral e Exercício Integrado", "Semana Pré-Avaliação"),
          sp(16)]

story += [h2("Checklist — DCF Completo")]
chk_items = [
    "Calculei o FCFF atual e eliminei itens não recorrentes?",
    "O FCFF é uma base razoável para extrapolação?",
    "A taxa de crescimento de longo prazo é compatível com o PIB potencial?",
    "Calculei Ke pelo CAPM usando NTN-B 10a e ERP de 5,5%?",
    "Usei o beta adequado (histórico ou bottom-up realavancado)?",
    "Calculei o Kd líquido de IR/CSLL?",
    "Usei pesos do WACC a valor de mercado?",
    "Identifiquei e ajustei impairments, provisões e ARO relevantes?",
    "Verifiquei POC e hedge accounting nos ajustes de receita?",
    "Considerei opções reais relevantes (expansão, abandono, adiamento)?",
    "Realizei análise de sensibilidade (variando g e WACC)?",
    "Comparei com múltiplos de mercado (sanity check)?",
]
for item in chk_items:
    story.append(Paragraph(f"☐  {item}", sBullet))
story.append(sp(16))

story += [h2("Mapa de Conexões"),
          tbl([("FCFF ↑",             "Valor do DCF ↑"),
               ("WACC ↑",             "Valor do DCF ↓"),
               ("g longo prazo ↑",    "Valor Terminal ↑ → maior sensibilidade ao WACC"),
               ("β ↑",                "Ke ↑ → WACC ↑ → VPL ↓"),
               ("Alavancagem ↑",      "Kd(1–t) cai; risco financeiro sobe"),
               ("σ ↑",                "Opções Reais ↑ (call e put)"),
               ("Impairment",         "Sem efeito direto no FCFF; revisar premissas"),
               ("POC antecipado",     "Receita contábil ≠ caixa. FCFF inalterado")],
              headers=["Variável / Evento", "Efeito no Valuation"]),
          sp(16)]

story += [h2("Exercício Integrado — Empresa ABC (Logística)"),
          tbl([("EBIT",               "R$ 50 MM"),
               ("Depreciação",        "R$ 8 MM"),
               ("Receita não recorr.","R$ 3 MM"),
               ("IR sobre EBIT",      "R$ 15 MM"),
               ("CAPEX",              "R$ 12 MM"),
               ("ΔNCG",               "R$ 4 MM"),
               ("Beta",               "0,85"),
               ("NTN-B 10a",          "7,5% a.a."),
               ("ERP",                "5,5% a.a."),
               ("Kd bruto",           "11,0% a.a."),
               ("Alíquota IR/CSLL",   "34%"),
               ("E/(D+E)",            "60%"),
               ("g real longo prazo", "3,0% a.a.")],
              headers=["Dado", "Valor"], col_widths=[6*cm, 10.5*cm]),
          sp(10),
          example("Gabarito", [
              ("FCFF",     "50 + 8 – 3 – 15 – 12 – 4  =  R$ 24 MM"),
              ("Ke",       "7,5 + 0,85 × 5,5  =  12,18% a.a."),
              ("Kd líq.",  "11,0 × (1 – 0,34)  =  7,26% a.a."),
              ("WACC",     "0,60 × 12,18 + 0,40 × 7,26  =  10,21% a.a."),
              ("V.T.",     "24 × 1,03 / (0,1021 – 0,03)  ≈  R$ 343 MM"),
              ("Opções",   "Existe opção de expansão (nova rota/terminal)? Calcule se σ disponível."),
          ]),
          sp(16)]

story += [h2("Dicas para os Estudos Dirigidos e Seminário"),
          bullet("Leia as notas explicativas do ITR/DFP — contingências, impairment, segmentos."),
          bullet("Justifique sempre cada ajuste ao FCFF."),
          bullet("Seminário: 8 slides · 2 primeiros contextualizando o artigo e a questão de pesquisa."),
          bullet("Upload até quinta-feira anterior às 23h59."),
          bullet("Nota final = 60% EDs (excl. pior nota) + 40% Seminário. Mínimo: 6,0."),
          sp(8),
          ThinRule(ACCENT, thickness=1, space_before=2, space_after=6),
          muted("Fluxo de Estudo elaborado com base nos Slides das Aulas 1–8 — "
                "Avaliação de Empresas — Mestrado Profissional em Economia.")]


# ══════════════════════════════════════════════════════════════════════════════
# GERAÇÃO DO PDF
# ══════════════════════════════════════════════════════════════════════════════
OUTPUT = "/home/user/estado-economia-dashboard/Fluxo_de_Estudo_Avaliacao_de_Empresas.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=2.8*cm,
    rightMargin=2.8*cm,
    topMargin=2*cm,
    bottomMargin=2*cm,
    title="Fluxo de Estudo — Avaliação de Empresas",
    author="Prof. Sérgio Jurandyr Machado",
)

doc.build(story, onFirstPage=_cover_page, onLaterPages=_on_page)
print(f"PDF gerado: {OUTPUT}")
