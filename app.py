"""
Dashboard Educacional — Mercado Competitivo, Eficiência e o Papel do Estado na Economia
Análise quantitativa e interativa para aprendizagem de Economia do Setor Público,
Teoria do Consumidor, Teoria da Firma e Equilíbrio Geral.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

# ─── Configuração da Página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="O Papel do Estado na Economia",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS Customizado ───────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    .main-header h1 {
        color: #e94560;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
    }
    .main-header p {
        color: #a7b5c9;
        font-size: 1.05rem;
        margin: 0.5rem 0 0 0;
    }

    .concept-card {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        border: 1px solid #0f3460;
        border-radius: 14px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }
    .concept-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(233,69,96,0.15);
    }
    .concept-card h3 { color: #e94560; margin: 0 0 0.5rem 0; font-size: 1.15rem; }
    .concept-card p  { color: #c4cdd8; margin: 0; font-size: 0.95rem; line-height: 1.6; }

    .metric-box {
        background: linear-gradient(145deg, #0f3460, #16213e);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid rgba(233,69,96,0.3);
    }
    .metric-box h2 { color: #e94560; margin: 0; font-size: 1.8rem; }
    .metric-box p  { color: #a7b5c9; margin: 0.3rem 0 0 0; font-size: 0.85rem; }

    .quiz-correct   { background: linear-gradient(145deg, #0a3d2a, #0d4f35); border: 1px solid #2ecc71; border-radius: 10px; padding: 1rem; margin: 0.5rem 0; }
    .quiz-incorrect  { background: linear-gradient(145deg, #3d0a0a, #4f0d0d); border: 1px solid #e74c3c; border-radius: 10px; padding: 1rem; margin: 0.5rem 0; }

    div[data-testid="stTabs"] button {
        font-weight: 600;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🏛️ Mercado Competitivo & O Papel do Estado na Economia</h1>
    <p>Dashboard interativo — Teoria do Consumidor, Firma, Equilíbrio Geral e Economia do Setor Público</p>
</div>
""", unsafe_allow_html=True)

# ─── Tabs ──────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "🏠 Visão Geral",
    "🛒 Teoria do Consumidor",
    "🏭 Teoria da Firma",
    "⚡ Equilíbrio & 1º Teorema",
    "📊 Eficiência de Pareto",
    "📉 Monopólio vs Concorrência",
    "🌍 Bens Públicos & Externalidades",
    "⚖️ Funções de Musgrave",
    "🧠 Quiz Interativo",
])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — VISÃO GERAL
# ════════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("## Mapa Conceitual: Razões para Intervenção do Estado")

    col1, col2, col3 = st.columns(3)
    cards = [
        ("🏛️ Instituições", "Direito de propriedade, imposição de contratos, segurança, poderes Judiciário, Legislativo e Executivo."),
        ("⚖️ Distribuição de Renda", "Segundo Teorema do Bem-Estar: redistribuição via sistema tributário, despesas e serviços públicos."),
        ("📉 Falhas de Mercado", "Concorrência imperfeita, bens públicos, externalidades, informação assimétrica, mercados incompletos."),
        ("🎯 Função Alocativa", "Prover bens públicos e meritórios, regular monopólios naturais."),
        ("💰 Função Distributiva", "Tributação progressiva, transferências, salário mínimo."),
        ("📈 Função Estabilizadora", "Política monetária e fiscal para emprego e estabilidade de preços."),
    ]
    for i, (title, desc) in enumerate(cards):
        with [col1, col2, col3][i % 3]:
            st.markdown(f"""
            <div class="concept-card">
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Estrutura das Falhas de Mercado")

    falhas_data = pd.DataFrame({
        "Falha de Mercado": [
            "Concorrência Imperfeita", "Bens Públicos", "Externalidades",
            "Informação Assimétrica", "Mercados Incompletos", "Desequilíbrios Macro"
        ],
        "Problema": [
            "Poder de mercado → preços acima do CMg",
            "Não-rivalidade + Não-excludabilidade → free rider",
            "Custos/benefícios não refletidos nos preços",
            "Risco moral e seleção adversa",
            "Riscos inviáveis impedem oferta",
            "Desemprego, inflação, ciclos"
        ],
        "Solução Típica": [
            "Regulação, política antitruste",
            "Provisão pública, impostos",
            "Pigou (imposto/subsídio), regulação",
            "Padronização, Inmetro, incentivos",
            "Seguro social, crédito dirigido",
            "Política monetária e fiscal"
        ],
        "Exemplo": [
            "Água, energia (monopólio natural)",
            "Defesa nacional, iluminação pública",
            "Poluição (neg.), Educação (pos.)",
            "Planos de saúde, mercado de trabalho",
            "Seguro-desemprego, crédito estudantil",
            "Crise de 1929, inflação anos 80"
        ],
    })
    st.dataframe(falhas_data, use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — TEORIA DO CONSUMIDOR
# ════════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown("## 🛒 Teoria do Consumidor — Maximização de Utilidade")
    st.markdown("""
    O consumidor maximiza sua utilidade **U(x₁, x₂)** sujeito à restrição orçamentária **p₁x₁ + p₂x₂ = w**.
    A solução ocorre onde a **Taxa Marginal de Substituição (TMS)** iguala a razão de preços: **TMS = p₁/p₂**.
    """)

    col_cons_p, col_cons_g = st.columns([1, 2])

    with col_cons_p:
        st.markdown("### Parâmetros")
        st.latex(r"U(x_1, x_2) = x_1^{\alpha} \cdot x_2^{1-\alpha}")
        alpha_c = st.slider("α (preferência pelo bem 1)", 0.1, 0.9, 0.5, 0.05, key="cons_alpha")
        p1_c = st.slider("p₁ (preço do bem 1)", 1, 20, 4, key="cons_p1")
        p2_c = st.slider("p₂ (preço do bem 2)", 1, 20, 5, key="cons_p2")
        w_c = st.slider("w (renda)", 20, 200, 100, key="cons_w")

        # Solução analítica (Cobb-Douglas)
        x1_star = alpha_c * w_c / p1_c
        x2_star = (1 - alpha_c) * w_c / p2_c
        u_star = (x1_star ** alpha_c) * (x2_star ** (1 - alpha_c))
        tms_star = (alpha_c * x2_star) / ((1 - alpha_c) * x1_star)

        st.markdown("### Solução Ótima")
        st.markdown(f"""
        - **x₁\*** = αw/p₁ = **{x1_star:.2f}**
        - **x₂\*** = (1-α)w/p₂ = **{x2_star:.2f}**
        - **U\*** = **{u_star:.2f}**
        - **TMS** = p₁/p₂ = **{p1_c/p2_c:.2f}**
        """)

    with col_cons_g:
        fig_cons = go.Figure()

        x1_max = w_c / p1_c * 1.3
        x2_max = w_c / p2_c * 1.3
        x1_r = np.linspace(0.1, x1_max, 300)

        # Restrição orçamentária
        x2_budget = (w_c - p1_c * x1_r) / p2_c
        mask_b = x2_budget >= 0
        fig_cons.add_trace(go.Scatter(
            x=x1_r[mask_b], y=x2_budget[mask_b], mode='lines',
            line=dict(color='#f9d923', width=2.5), name=f'Restrição: {p1_c}x₁+{p2_c}x₂={w_c}',
        ))

        # Curvas de indiferença
        for mult in [0.6, 0.8, 1.0, 1.2, 1.5]:
            u_level = u_star * mult
            x2_ic = (u_level / (x1_r ** alpha_c)) ** (1 / (1 - alpha_c))
            mask_ic = (x2_ic > 0) & (x2_ic < x2_max)
            fig_cons.add_trace(go.Scatter(
                x=x1_r[mask_ic], y=x2_ic[mask_ic], mode='lines',
                line=dict(color='#4ecdc4', width=1.5, dash='dot' if mult != 1.0 else 'solid'),
                name=f'U={u_level:.1f}', showlegend=(mult == 1.0),
                hovertemplate='x₁=%{x:.1f}<br>x₂=%{y:.1f}',
            ))

        # Ponto ótimo
        fig_cons.add_trace(go.Scatter(
            x=[x1_star], y=[x2_star], mode='markers+text',
            marker=dict(size=14, color='#e94560', symbol='star'),
            text=[f'({x1_star:.1f}, {x2_star:.1f})'], textposition='top right',
            textfont=dict(color='#e94560', size=12), name='Ótimo (x₁*, x₂*)',
        ))

        fig_cons.update_layout(
            template='plotly_dark', paper_bgcolor='#0e1117', plot_bgcolor='#1a1a2e',
            xaxis=dict(title='Bem x₁', range=[0, x1_max], gridcolor='#2a2a4e'),
            yaxis=dict(title='Bem x₂', range=[0, x2_max], gridcolor='#2a2a4e'),
            height=520, margin=dict(l=50, r=30, t=30, b=50),
            legend=dict(bgcolor='rgba(26,26,46,0.8)', bordercolor='#0f3460'),
        )
        st.plotly_chart(fig_cons, use_container_width=True)

    st.markdown("""
    > **Condição de tangência**: No ótimo, a inclinação da curva de indiferença (TMS) iguala a inclinação
    > da restrição orçamentária (p₁/p₂). Todos os consumidores enfrentam os mesmos preços, logo:
    > **TMS^a = TMS^b = ... = p₁/p₂** — condição para eficiência na troca.
    """)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — TEORIA DA FIRMA
# ════════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown("## 🏭 Teoria da Firma — Maximização de Lucro")
    st.markdown("""
    A firma maximiza lucro escolhendo insumos que minimizem custos para um dado nível de produção.
    A condição de equilíbrio é **TMST = w₁/w₂** (razão dos preços dos insumos).
    """)

    col_firm_p, col_firm_g = st.columns([1, 2])

    with col_firm_p:
        st.markdown("### Função de Produção (Cobb-Douglas)")
        st.latex(r"F(z_1, z_2) = A \cdot z_1^{\gamma} \cdot z_2^{1-\gamma}")
        A_f = st.slider("A (produtividade total)", 1.0, 10.0, 5.0, 0.5, key="firm_A")
        gamma_f = st.slider("γ (elasticidade do insumo 1)", 0.1, 0.9, 0.4, 0.05, key="firm_gamma")
        w1_f = st.slider("w₁ (preço do insumo 1)", 1, 20, 5, key="firm_w1")
        w2_f = st.slider("w₂ (preço do insumo 2)", 1, 20, 8, key="firm_w2")
        target_y = st.slider("Produção desejada (ȳ)", 5, 50, 20, key="firm_y")

        # Solução: minimizar custo → z1/z2 = (γ w2) / ((1-γ) w1)
        ratio = (gamma_f * w2_f) / ((1 - gamma_f) * w1_f)
        # F(z1, z2) = ȳ → A * z1^γ * z2^(1-γ) = ȳ → z2 = (ȳ / (A * z1^γ))^(1/(1-γ))
        # Com a condição: z1 = ratio * z2
        z2_star = (target_y / (A_f * (ratio ** gamma_f))) ** (1 / 1)
        z1_star = ratio * z2_star
        custo_min = w1_f * z1_star + w2_f * z2_star
        tmst_val = (gamma_f * z2_star) / ((1 - gamma_f) * z1_star) if z1_star > 0 else 0

        st.markdown(f"""
        ### Solução Ótima
        - **z₁\*** = **{z1_star:.2f}**
        - **z₂\*** = **{z2_star:.2f}**
        - **Custo mínimo** = **{custo_min:.2f}**
        - **TMST** = w₁/w₂ = **{w1_f/w2_f:.2f}**
        """)

    with col_firm_g:
        fig_firm = go.Figure()
        z1_max = max(z1_star * 3, 10)
        z2_max_f = max(z2_star * 3, 10)
        z1_r = np.linspace(0.1, z1_max, 300)

        # Isoquanta (F = ȳ)
        for mult in [0.6, 0.8, 1.0, 1.3]:
            y_level = target_y * mult
            z2_iso = (y_level / (A_f * z1_r ** gamma_f)) ** (1 / (1 - gamma_f))
            mask_iso = (z2_iso > 0) & (z2_iso < z2_max_f)
            fig_firm.add_trace(go.Scatter(
                x=z1_r[mask_iso], y=z2_iso[mask_iso], mode='lines',
                line=dict(color='#4ecdc4', width=1.5, dash='dot' if mult != 1.0 else 'solid'),
                name=f'Isoquanta F={y_level:.0f}', showlegend=(mult == 1.0),
            ))

        # Isocusto (w1*z1 + w2*z2 = C)
        z2_isocost = (custo_min - w1_f * z1_r) / w2_f
        mask_cost = z2_isocost >= 0
        fig_firm.add_trace(go.Scatter(
            x=z1_r[mask_cost], y=z2_isocost[mask_cost], mode='lines',
            line=dict(color='#f9d923', width=2.5), name=f'Isocusto C={custo_min:.0f}',
        ))

        # Ponto ótimo
        fig_firm.add_trace(go.Scatter(
            x=[z1_star], y=[z2_star], mode='markers+text',
            marker=dict(size=14, color='#e94560', symbol='star'),
            text=[f'({z1_star:.1f}, {z2_star:.1f})'], textposition='top right',
            textfont=dict(color='#e94560', size=12), name='Min. Custo',
        ))

        fig_firm.update_layout(
            template='plotly_dark', paper_bgcolor='#0e1117', plot_bgcolor='#1a1a2e',
            xaxis=dict(title='Insumo z₁', range=[0, z1_max], gridcolor='#2a2a4e'),
            yaxis=dict(title='Insumo z₂', range=[0, z2_max_f], gridcolor='#2a2a4e'),
            height=520, margin=dict(l=50, r=30, t=30, b=50),
            legend=dict(bgcolor='rgba(26,26,46,0.8)', bordercolor='#0f3460'),
        )
        st.plotly_chart(fig_firm, use_container_width=True)

    st.markdown("""
    > **Condição de tangência**: No custo mínimo, a isoquanta é tangente à isocusto → **TMST = w₁/w₂**.
    > Para múltiplos produtores: **TMST^α = TMST^β = ... = w₁/w₂** — condição de eficiência na produção.
    """)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 4 — EQUILÍBRIO GERAL & 1º TEOREMA DO BEM-ESTAR
# ════════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown("## ⚡ Equilíbrio Geral & Primeiro Teorema do Bem-Estar")

    st.markdown("""
    O **equilíbrio geral** ocorre quando consumidores e firmas otimizam simultaneamente sob os mesmos preços.
    O **1º Teorema Fundamental do Bem-Estar** afirma: *"Uma economia competitiva é eficiente no sentido de Pareto"*.
    """)

    # Formas de organização da economia
    col_org1, col_org2, col_org3 = st.columns(3)
    org_cards = [
        ("🏪 Economia de Mercado", "Decisões descentralizadas por famílias e firmas via sinais de preço.",
         "Interesse próprio, tomadores de preço, informação perfeita."),
        ("🏢 Planejamento Central", "Planejadores governamentais decidem o quê, quanto e como produzir.",
         "Coordenação centralizada, sem mecanismo de preços."),
        ("🔄 Economia Mista", "Mercado toma a maioria das decisões; governo intervém em falhas.",
         "Modelo predominante no mundo real."),
    ]
    for (title, desc, extra), col in zip(org_cards, [col_org1, col_org2, col_org3]):
        with col:
            st.markdown(f"""
            <div class="concept-card">
                <h3>{title}</h3>
                <p>{desc}</p>
                <p style="color: #f9d923; font-size: 0.85rem; margin-top: 0.5rem;">↳ {extra}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Curva de Possibilidades de Produção (CPP)")

    col_cpp_p, col_cpp_g = st.columns([1, 2])

    with col_cpp_p:
        st.markdown("A CPP mostra as combinações máximas de dois bens que a economia pode produzir.")
        st.latex(r"\left(\frac{x_1}{L_1}\right)^2 + \left(\frac{x_2}{L_2}\right)^2 = 1")
        L1_cpp = st.slider("Capacidade máxima de X₁", 10, 50, 30, key="cpp_L1")
        L2_cpp = st.slider("Capacidade máxima de X₂", 10, 50, 25, key="cpp_L2")
        ponto_t = st.slider("Ponto na CPP (t ∈ [0,1])", 0.0, 1.0, 0.5, 0.01, key="cpp_t")

        # Ponto na CPP
        theta = ponto_t * np.pi / 2
        x1_cpp_pt = L1_cpp * np.cos(theta)
        x2_cpp_pt = L2_cpp * np.sin(theta)
        # TMT (inclinação) = dx2/dx1 = -(L2/L1) * tan(theta) ... simplificado
        tmt = (L2_cpp * np.cos(theta)) / (L1_cpp * np.sin(theta)) if np.sin(theta) > 0.01 else float('inf')

        st.markdown(f"""
        ### Ponto escolhido
        - **X₁** = {x1_cpp_pt:.1f}
        - **X₂** = {x2_cpp_pt:.1f}
        - **TMT** = {tmt:.2f}
        """)
        st.info("No equilíbrio: TMS = TMST = TMT = p₁/p₂")

    with col_cpp_g:
        fig_cpp = go.Figure()

        # CPP
        theta_r = np.linspace(0, np.pi / 2, 300)
        x1_cpp = L1_cpp * np.cos(theta_r)
        x2_cpp = L2_cpp * np.sin(theta_r)

        fig_cpp.add_trace(go.Scatter(
            x=x1_cpp, y=x2_cpp, mode='lines',
            line=dict(color='#e94560', width=3), name='CPP (Fronteira)',
        ))

        # Área factível
        x1_fill = np.concatenate([[0], x1_cpp, [0]])
        x2_fill = np.concatenate([[0], x2_cpp, [0]])
        fig_cpp.add_trace(go.Scatter(
            x=x1_fill, y=x2_fill, fill='toself',
            fillcolor='rgba(233,69,96,0.08)', line=dict(width=0),
            name='Conjunto Factível', showlegend=True,
        ))

        # Ponto de equilíbrio na CPP
        fig_cpp.add_trace(go.Scatter(
            x=[x1_cpp_pt], y=[x2_cpp_pt], mode='markers+text',
            marker=dict(size=14, color='#f9d923', symbol='star'),
            text=[f'E ({x1_cpp_pt:.1f}, {x2_cpp_pt:.1f})'],
            textposition='top left', textfont=dict(color='#f9d923', size=12),
            name='Ponto de Equilíbrio',
        ))

        # Linha tangente (razão de preços)
        if tmt < 100:
            dx = 8
            tang_x = np.array([x1_cpp_pt - dx, x1_cpp_pt + dx])
            tang_y = x2_cpp_pt + tmt * (x1_cpp_pt - tang_x)
            tang_mask = (tang_y >= 0) & (tang_x >= 0)
            fig_cpp.add_trace(go.Scatter(
                x=tang_x[tang_mask], y=tang_y[tang_mask], mode='lines',
                line=dict(color='#4ecdc4', width=2, dash='dash'),
                name=f'p₁/p₂ = {tmt:.2f} (preços)',
            ))

        fig_cpp.update_layout(
            template='plotly_dark', paper_bgcolor='#0e1117', plot_bgcolor='#1a1a2e',
            xaxis=dict(title='Bem X₁', range=[0, L1_cpp * 1.1], gridcolor='#2a2a4e'),
            yaxis=dict(title='Bem X₂', range=[0, L2_cpp * 1.1], gridcolor='#2a2a4e'),
            height=500, margin=dict(l=50, r=30, t=30, b=50),
            legend=dict(bgcolor='rgba(26,26,46,0.8)', bordercolor='#0f3460'),
        )
        st.plotly_chart(fig_cpp, use_container_width=True)

    # Condições de equilíbrio
    st.markdown("---")
    st.markdown("### Condições de Equilíbrio Geral")
    eq_col1, eq_col2, eq_col3 = st.columns(3)
    with eq_col1:
        st.markdown("""
        <div class="concept-card">
            <h3>🔄 Entre Consumidores</h3>
            <p>TMS<sup>a</sup> = TMS<sup>b</sup> = ... = p₁/p₂<br>
            <em>Eficiência na troca: todos equalizam suas TMS aos preços relativos.</em></p>
        </div>
        """, unsafe_allow_html=True)
    with eq_col2:
        st.markdown("""
        <div class="concept-card">
            <h3>🏭 Entre Firmas</h3>
            <p>TMST<sup>α</sup> = TMST<sup>β</sup> = ... = w₁/w₂<br>
            <em>Eficiência na produção: todas equalizam suas TMST aos preços dos insumos.</em></p>
        </div>
        """, unsafe_allow_html=True)
    with eq_col3:
        st.markdown("""
        <div class="concept-card">
            <h3>⚡ Composição do Produto</h3>
            <p>TMS = TMST = TMT = p₁/p₂<br>
            <em>O que consumidores desejam = o que firmas produzem com eficiência.</em></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    > **1º Teorema do Bem-Estar**: Uma economia competitiva (com informação perfeita, tomadores de preço
    > e mercados completos) alcança automaticamente uma alocação eficiente de Pareto.
    > Podem coexistir diversos ótimos de Pareto, e o equilíbrio competitivo maximiza o bem-estar total
    > (Excedente do Consumidor + Excedente do Produtor). Porém, Pareto-eficiente ≠ justo.
    """)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 5 — EFICIÊNCIA DE PARETO / CAIXA DE EDGEWORTH
# ════════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown("## Caixa de Edgeworth — Simulação Interativa")
    st.markdown("""
    A **Caixa de Edgeworth** mostra todas as alocações possíveis de 2 bens entre 2 consumidores.
    A **curva de contrato** conecta todos os ótimos de Pareto — pontos onde as curvas de indiferença são tangentes.
    """)

    col_params, col_chart = st.columns([1, 2])

    with col_params:
        st.markdown("### Parâmetros")
        total_x = st.slider("Dotação total de Bem X", 5, 20, 10, key="edg_x")
        total_y = st.slider("Dotação total de Bem Y", 5, 20, 10, key="edg_y")
        w_x1 = st.slider("Dotação inicial C₁ — Bem X", 0.5, float(total_x) - 0.5, float(total_x) * 0.3, 0.5, key="w_x1")
        w_y1 = st.slider("Dotação inicial C₁ — Bem Y", 0.5, float(total_y) - 0.5, float(total_y) * 0.7, 0.5, key="w_y1")

        alpha = st.slider("α (preferência C₁ por X)", 0.1, 0.9, 0.5, 0.05, key="alpha")
        beta = st.slider("β (preferência C₂ por X)", 0.1, 0.9, 0.5, 0.05, key="beta")

    with col_chart:
        fig = go.Figure()

        # Curvas de indiferença de C1 (Cobb-Douglas: U = x^α * y^(1-α))
        u1_at_w = (w_x1 ** alpha) * (w_y1 ** (1 - alpha))
        x_vals = np.linspace(0.1, total_x - 0.1, 200)

        for mult in [0.7, 1.0, 1.3, 1.6]:
            u_level = u1_at_w * mult
            y_ic1 = (u_level / (x_vals ** alpha)) ** (1 / (1 - alpha))
            mask = (y_ic1 > 0) & (y_ic1 < total_y)
            fig.add_trace(go.Scatter(
                x=x_vals[mask], y=y_ic1[mask],
                mode='lines', line=dict(color='#e94560', width=1.5, dash='dot' if mult != 1.0 else 'solid'),
                name=f'IC₁ (U={u_level:.1f})', showlegend=(mult == 1.0),
                hovertemplate='x₁=%{x:.1f}<br>y₁=%{y:.1f}'
            ))

        # Curvas de indiferença de C2 (invertidas)
        w_x2 = total_x - w_x1
        w_y2 = total_y - w_y1
        u2_at_w = (w_x2 ** beta) * (w_y2 ** (1 - beta))

        for mult in [0.7, 1.0, 1.3, 1.6]:
            u_level = u2_at_w * mult
            x2_vals = np.linspace(0.1, total_x - 0.1, 200)
            y2_ic = (u_level / (x2_vals ** beta)) ** (1 / (1 - beta))
            # Convert to C1 coordinates
            x1_from_c2 = total_x - x2_vals
            y1_from_c2 = total_y - y2_ic
            mask = (y1_from_c2 > 0) & (y1_from_c2 < total_y) & (x1_from_c2 > 0) & (x1_from_c2 < total_x)
            fig.add_trace(go.Scatter(
                x=x1_from_c2[mask], y=y1_from_c2[mask],
                mode='lines', line=dict(color='#4ecdc4', width=1.5, dash='dot' if mult != 1.0 else 'solid'),
                name=f'IC₂ (U={u_level:.1f})', showlegend=(mult == 1.0),
                hovertemplate='x₁=%{x:.1f}<br>y₁=%{y:.1f}'
            ))

        # Curva de contrato (locus de tangências)
        t_vals = np.linspace(0.01, 0.99, 300)
        cc_x1 = t_vals * total_x
        # Para Cobb-Douglas, curva de contrato: y1 = (alpha * (1-beta) * total_y * x1) / (beta * (1-alpha) * total_x + (alpha*(1-beta) - beta*(1-alpha)) * x1)
        num = alpha * (1 - beta) * total_y * cc_x1
        den = beta * (1 - alpha) * total_x + (alpha * (1 - beta) - beta * (1 - alpha)) * cc_x1
        # Avoid division by zero
        valid = np.abs(den) > 1e-6
        cc_y1 = np.where(valid, num / den, np.nan)
        cc_mask = (cc_y1 > 0) & (cc_y1 < total_y) & np.isfinite(cc_y1)

        fig.add_trace(go.Scatter(
            x=cc_x1[cc_mask], y=cc_y1[cc_mask],
            mode='lines', line=dict(color='#f9d923', width=3),
            name='Curva de Contrato (Ótimos de Pareto)',
            hovertemplate='x₁=%{x:.1f}<br>y₁=%{y:.1f}'
        ))

        # Dotação inicial
        fig.add_trace(go.Scatter(
            x=[w_x1], y=[w_y1],
            mode='markers+text', marker=dict(size=14, color='#ffffff', symbol='star'),
            text=['W'], textposition='top right', textfont=dict(color='white', size=14),
            name='Dotação Inicial (W)', showlegend=True
        ))

        # Caixa
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='#0e1117', plot_bgcolor='#1a1a2e',
            xaxis=dict(title='Bem X (C₁ →)', range=[0, total_x], gridcolor='#2a2a4e'),
            yaxis=dict(title='Bem Y (C₁ →)', range=[0, total_y], gridcolor='#2a2a4e'),
            legend=dict(
                bgcolor='rgba(26,26,46,0.8)', bordercolor='#0f3460',
                font=dict(size=11)
            ),
            height=550,
            margin=dict(l=50, r=30, t=30, b=50),
        )
        # Borda da caixa
        fig.add_shape(type="rect", x0=0, y0=0, x1=total_x, y1=total_y,
                      line=dict(color="#e94560", width=2))

        st.plotly_chart(fig, use_container_width=True)

    # Explicação
    st.markdown("""
    > **Interpretação**: Pontos na **curva de contrato** (amarela) são **ótimos de Pareto** — não é possível
    > melhorar um consumidor sem piorar o outro. A estrela ⭐ mostra a dotação inicial.
    > O **Segundo Teorema do Bem-Estar** diz que qualquer ponto na curva de contrato pode ser alcançado
    > via mercado competitivo, desde que o governo redistribua as dotações iniciais adequadamente.
    """)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 6 — MONOPÓLIO vs CONCORRÊNCIA
# ════════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown("## Monopólio vs. Concorrência Perfeita")

    col_p, col_g = st.columns([1, 2])

    with col_p:
        st.markdown("### Função de Demanda Inversa")
        st.latex(r"P(Q) = a - bQ")
        a_val = st.slider("a (intercepto)", 10, 100, 50, key="mono_a")
        b_val = st.slider("b (inclinação)", 1, 10, 2, key="mono_b")

        st.markdown("### Custo Marginal")
        st.latex(r"CMg = c")
        c_val = st.slider("c (custo marginal constante)", 1, 50, 10, key="mono_c")

    # Cálculos
    q_max = a_val / b_val
    q_range = np.linspace(0, q_max, 300)
    p_demand = a_val - b_val * q_range
    rmg = a_val - 2 * b_val * q_range
    cmg_line = np.full_like(q_range, c_val)

    # Equilíbrio competitivo: P = CMg  →  Q_c = (a - c) / b
    q_comp = max(0, (a_val - c_val) / b_val)
    p_comp = c_val

    # Equilíbrio monopolista: RMg = CMg  →  Q_m = (a - c) / (2b)
    q_mono = max(0, (a_val - c_val) / (2 * b_val))
    p_mono = a_val - b_val * q_mono

    with col_g:
        fig2 = go.Figure()

        # ── Áreas de excedente (desenhadas primeiro, ficam atrás) ──
        if q_mono < q_comp and q_mono > 0:
            # 1) Excedente do Consumidor no monopólio (triângulo acima de Pm)
            q_ec = np.linspace(0, q_mono, 50)
            p_ec = a_val - b_val * q_ec
            fig2.add_trace(go.Scatter(
                x=np.concatenate([q_ec, [q_mono, 0]]),
                y=np.concatenate([p_ec, [p_mono, p_mono]]),
                fill='toself', fillcolor='rgba(78,205,196,0.20)',
                line=dict(color='rgba(78,205,196,0.4)', width=1),
                name='Exc. Consumidor (EC)', showlegend=True,
            ))

            # 2) Lucro do monopolista (retângulo entre Pm e CMg, de 0 a Qm)
            fig2.add_trace(go.Scatter(
                x=[0, q_mono, q_mono, 0, 0],
                y=[p_mono, p_mono, c_val, c_val, p_mono],
                fill='toself', fillcolor='rgba(168,85,247,0.22)',
                line=dict(color='rgba(168,85,247,0.5)', width=1),
                name='Lucro Monopolista (π)', showlegend=True,
            ))

            # 3) PESO MORTO — triângulo bem visível
            fig2.add_trace(go.Scatter(
                x=[q_mono, q_comp, q_mono, q_mono],
                y=[p_mono, c_val, c_val, p_mono],
                fill='toself', fillcolor='rgba(255,60,60,0.45)',
                line=dict(color='#ff3c3c', width=3),
                name='⚠️ PESO MORTO (DWL)',
            ))

        # ── Curvas ──
        fig2.add_trace(go.Scatter(
            x=q_range, y=p_demand, mode='lines',
            line=dict(color='#4ecdc4', width=3), name='Demanda P(Q)',
        ))
        fig2.add_trace(go.Scatter(
            x=q_range, y=rmg, mode='lines',
            line=dict(color='#e94560', width=3, dash='dash'), name='Receita Marginal (RMg)',
        ))
        fig2.add_trace(go.Scatter(
            x=q_range, y=cmg_line, mode='lines',
            line=dict(color='#f9d923', width=2.5), name=f'CMg = {c_val}',
        ))

        # ── Linhas de referência tracejadas (Qm→Pm, Qc→Pc) ──
        if q_mono > 0:
            fig2.add_shape(type="line", x0=q_mono, y0=0, x1=q_mono, y1=p_mono,
                           line=dict(color='#e94560', width=1.5, dash='dot'))
            fig2.add_shape(type="line", x0=0, y0=p_mono, x1=q_mono, y1=p_mono,
                           line=dict(color='#e94560', width=1.5, dash='dot'))
        if q_comp > 0:
            fig2.add_shape(type="line", x0=q_comp, y0=0, x1=q_comp, y1=c_val,
                           line=dict(color='#4ecdc4', width=1.5, dash='dot'))

        # ── Pontos de equilíbrio (maiores e mais visíveis) ──
        fig2.add_trace(go.Scatter(
            x=[q_comp], y=[p_comp], mode='markers',
            marker=dict(size=14, color='#4ecdc4', symbol='circle', line=dict(width=2, color='white')),
            name=f'Competitivo (Q={q_comp:.1f}, P={p_comp:.1f})',
        ))
        fig2.add_trace(go.Scatter(
            x=[q_mono], y=[p_mono], mode='markers',
            marker=dict(size=14, color='#e94560', symbol='diamond', line=dict(width=2, color='white')),
            name=f'Monopólio (Q={q_mono:.1f}, P={p_mono:.1f})',
        ))

        # ── Anotações no gráfico ──
        if q_mono < q_comp and q_mono > 0:
            dwl_x = (q_mono + q_comp) / 2
            dwl_y = (p_mono + c_val) / 2
            fig2.add_annotation(
                x=dwl_x, y=dwl_y, text="<b>PESO<br>MORTO</b>",
                font=dict(size=13, color='#ff3c3c'), showarrow=False,
                bgcolor='rgba(0,0,0,0.6)', bordercolor='#ff3c3c', borderwidth=1, borderpad=4,
            )
            fig2.add_annotation(
                x=q_mono / 2, y=(p_mono + c_val) / 2, text="<b>π</b>",
                font=dict(size=14, color='#a855f7'), showarrow=False,
            )
            fig2.add_annotation(
                x=q_mono / 3, y=(a_val + p_mono) / 2, text="<b>EC</b>",
                font=dict(size=14, color='#4ecdc4'), showarrow=False,
            )

        # Anotações dos eixos (Qm, Qc, Pm)
        if q_mono > 0:
            fig2.add_annotation(x=q_mono, y=-0.03*(a_val), text=f"Q<sub>m</sub>={q_mono:.1f}",
                                font=dict(size=11, color='#e94560'), showarrow=False, yanchor='top')
            fig2.add_annotation(x=-0.03*q_max, y=p_mono, text=f"P<sub>m</sub>={p_mono:.1f}",
                                font=dict(size=11, color='#e94560'), showarrow=False, xanchor='right')
        fig2.add_annotation(x=q_comp, y=-0.03*(a_val), text=f"Q<sub>c</sub>={q_comp:.1f}",
                            font=dict(size=11, color='#4ecdc4'), showarrow=False, yanchor='top')

        fig2.update_layout(
            template='plotly_dark',
            paper_bgcolor='#0e1117', plot_bgcolor='#1a1a2e',
            xaxis=dict(title='Quantidade (Q)', gridcolor='#2a2a4e', rangemode='tozero',
                       title_font=dict(size=14), tickfont=dict(size=12)),
            yaxis=dict(title='Preço (P)', gridcolor='#2a2a4e', rangemode='tozero',
                       title_font=dict(size=14), tickfont=dict(size=12)),
            height=560, margin=dict(l=60, r=30, t=30, b=60),
            legend=dict(bgcolor='rgba(26,26,46,0.9)', bordercolor='#0f3460',
                        font=dict(size=12), x=0.55, y=0.98),
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Métricas
    dwl = 0.5 * (p_mono - c_val) * (q_comp - q_mono) if q_mono < q_comp else 0
    lucro_mono = (p_mono - c_val) * q_mono
    exc_cons_comp = 0.5 * (a_val - c_val) * q_comp
    exc_cons_mono = 0.5 * (a_val - p_mono) * q_mono

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""<div class="metric-box"><h2>💀 {dwl:.1f}</h2><p>Peso Morto (DWL)</p></div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class="metric-box"><h2>💰 {lucro_mono:.1f}</h2><p>Lucro do Monopolista</p></div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class="metric-box"><h2>📉 {exc_cons_mono:.1f}</h2><p>Exc. Consumidor (Monop.)</p></div>""", unsafe_allow_html=True)
    with m4:
        st.markdown(f"""<div class="metric-box"><h2>📈 {exc_cons_comp:.1f}</h2><p>Exc. Consumidor (Comp.)</p></div>""", unsafe_allow_html=True)

    st.markdown(f"""
    > **Análise**: O monopólio reduz a quantidade de **{q_comp:.1f}** para **{q_mono:.1f}** e aumenta o preço
    > de **{p_comp:.1f}** para **{p_mono:.1f}**, gerando uma perda de bem-estar (peso morto) de **{dwl:.1f}**.
    > A empresa competitiva opera onde **P = CMg**, enquanto o monopolista onde **RMg = CMg** (com P > CMg).
    """)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 7 — BENS PÚBLICOS & EXTERNALIDADES
# ════════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown("## Classificação dos Bens Econômicos")

    # Classificação interativa
    bens_df = pd.DataFrame({
        "Tipo": ["🔒 Privado", "🌐 Público", "🐟 Recurso Comum", "📺 Artificialmente Escasso"],
        "Excludente?": ["✅ Sim", "❌ Não", "❌ Não", "✅ Sim"],
        "Rival?": ["✅ Sim", "❌ Não", "✅ Sim", "❌ Não"],
        "Exemplos": [
            "Alimentos, roupas, automóveis",
            "Defesa nacional, farol, iluminação pública",
            "Peixes, água, estradas congestionadas",
            "TV a cabo, software, cinema"
        ],
        "Problema Principal": [
            "Nenhum (mercado funciona)",
            "Free rider — ninguém paga voluntariamente",
            "Tragédia dos comuns — uso excessivo",
            "Restrição artificial de acesso"
        ],
    })
    st.dataframe(bens_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    tab_ext_neg, tab_ext_pos, tab_tragedia = st.tabs([
        "📉 Externalidade Negativa",
        "📈 Externalidade Positiva",
        "🐟 Tragédia dos Comuns"
    ])

    # ── Externalidade Negativa ─────────────────────────────────────────────────
    with tab_ext_neg:
        st.markdown("### Externalidade Negativa + Imposto de Pigou")
        col_en1, col_en2 = st.columns([1, 2])

        with col_en1:
            ext_cost = st.slider("Custo externo por unidade", 1, 30, 10, key="ext_neg")
            st.markdown(f"""
            **Custo Social** = Custo Privado + Custo Externo ({ext_cost})

            O **Imposto de Pigou** = {ext_cost} por unidade internaliza a externalidade,
            fazendo o produtor pagar o custo social total.
            """)

        with col_en2:
            q_r = np.linspace(0, 25, 200)
            p_demand_en = 50 - 2 * q_r
            cmg_priv = 5 + q_r
            cmg_soc = cmg_priv + ext_cost

            q_priv = (50 - 5) / 3  # P = CMg_priv
            q_soc = (50 - 5 - ext_cost) / 3  # P = CMg_social

            fig3 = go.Figure()

            # DWL da externalidade (desenhada primeiro, fica atrás)
            if q_soc < q_priv and q_soc > 0:
                # Área de perda de bem-estar (entre Q* e Q_mercado)
                q_dwl = np.linspace(q_soc, q_priv, 50)
                cmg_soc_dwl = 5 + q_dwl + ext_cost
                p_dem_dwl = 50 - 2 * q_dwl
                fig3.add_trace(go.Scatter(
                    x=np.concatenate([q_dwl, q_dwl[::-1]]),
                    y=np.concatenate([p_dem_dwl, cmg_soc_dwl[::-1]]),
                    fill='toself', fillcolor='rgba(255,60,60,0.40)',
                    line=dict(color='#ff3c3c', width=2.5),
                    name='⚠️ Perda de Bem-Estar (DWL)',
                ))

                # Anotação de DWL
                dwl_cx = (q_soc + q_priv) / 2
                dwl_cy = (50 - 2 * dwl_cx + 5 + dwl_cx + ext_cost) / 2
                fig3.add_annotation(
                    x=dwl_cx, y=dwl_cy, text="<b>DWL</b>",
                    font=dict(size=14, color='#ff3c3c'), showarrow=False,
                    bgcolor='rgba(0,0,0,0.6)', bordercolor='#ff3c3c', borderwidth=1, borderpad=4,
                )

            # Curvas
            fig3.add_trace(go.Scatter(x=q_r, y=p_demand_en, mode='lines',
                                      line=dict(color='#4ecdc4', width=3), name='Demanda'))
            fig3.add_trace(go.Scatter(x=q_r, y=cmg_priv, mode='lines',
                                      line=dict(color='#a7b5c9', width=2.5), name='CMg Privado'))
            fig3.add_trace(go.Scatter(x=q_r, y=cmg_soc, mode='lines',
                                      line=dict(color='#e94560', width=3, dash='dash'), name='CMg Social'))

            # Linhas de referência
            if q_soc > 0:
                fig3.add_shape(type="line", x0=q_soc, y0=0, x1=q_soc, y1=50 - 2 * q_soc,
                               line=dict(color='#e94560', width=1.5, dash='dot'))
                fig3.add_shape(type="line", x0=q_priv, y0=0, x1=q_priv, y1=50 - 2 * q_priv,
                               line=dict(color='#a7b5c9', width=1.5, dash='dot'))

            # Pontos com borda branca
            fig3.add_trace(go.Scatter(x=[q_priv], y=[50 - 2 * q_priv], mode='markers',
                                      marker=dict(size=14, color='#a7b5c9',
                                                  line=dict(width=2, color='white')),
                                      name=f'Mercado (Q={q_priv:.1f})'))
            fig3.add_trace(go.Scatter(x=[q_soc], y=[50 - 2 * q_soc], mode='markers',
                                      marker=dict(size=14, color='#e94560',
                                                  line=dict(width=2, color='white')),
                                      name=f'Ótimo Social (Q*={q_soc:.1f})'))

            # Anotação do imposto de Pigou
            if q_soc > 0:
                fig3.add_annotation(
                    x=q_soc, y=50 - 2 * q_soc + 2,
                    text=f"<b>Imposto = {ext_cost}</b>",
                    font=dict(size=11, color='#f9d923'), showarrow=True,
                    arrowcolor='#f9d923', arrowwidth=2, arrowhead=2,
                    ax=60, ay=-30,
                    bgcolor='rgba(0,0,0,0.5)', borderpad=3,
                )

            fig3.update_layout(
                template='plotly_dark', paper_bgcolor='#0e1117', plot_bgcolor='#1a1a2e',
                xaxis=dict(title='Quantidade (Q)', gridcolor='#2a2a4e',
                           title_font=dict(size=14), tickfont=dict(size=12)),
                yaxis=dict(title='Preço (P)', gridcolor='#2a2a4e',
                           title_font=dict(size=14), tickfont=dict(size=12)),
                height=480, margin=dict(l=60, r=30, t=30, b=50),
                legend=dict(bgcolor='rgba(26,26,46,0.9)', bordercolor='#0f3460', font=dict(size=12)),
            )
            st.plotly_chart(fig3, use_container_width=True)

    # ── Externalidade Positiva ─────────────────────────────────────────────────
    with tab_ext_pos:
        st.markdown("### Externalidade Positiva + Subsídio de Pigou")
        col_ep1, col_ep2 = st.columns([1, 2])

        with col_ep1:
            ext_ben = st.slider("Benefício externo por unidade", 1, 30, 12, key="ext_pos")
            st.markdown(f"""
            **Benefício Social** = Benefício Privado + Benefício Externo ({ext_ben})

            O **Subsídio de Pigou** = {ext_ben} por unidade incentiva a produção
            até o nível socialmente ótimo.
            """)

        with col_ep2:
            q_r2 = np.linspace(0, 30, 200)
            bmg_priv = 60 - 2 * q_r2
            bmg_soc = bmg_priv + ext_ben
            cmg_ep = 5 + q_r2

            q_priv_ep = (60 - 5) / 3
            q_soc_ep = (60 + ext_ben - 5) / 3

            fig4 = go.Figure()
            fig4.add_trace(go.Scatter(x=q_r2, y=bmg_priv, mode='lines',
                                      line=dict(color='#4ecdc4', width=2.5), name='BMg Privado (Demanda)'))
            fig4.add_trace(go.Scatter(x=q_r2, y=bmg_soc, mode='lines',
                                      line=dict(color='#2ecc71', width=2.5, dash='dash'), name='BMg Social'))
            fig4.add_trace(go.Scatter(x=q_r2, y=cmg_ep, mode='lines',
                                      line=dict(color='#f9d923', width=2), name='CMg'))

            if q_soc_ep > q_priv_ep:
                fig4.add_trace(go.Scatter(
                    x=[q_priv_ep, q_soc_ep, q_priv_ep],
                    y=[60 - 2 * q_priv_ep, 5 + q_soc_ep, 60 - 2 * q_priv_ep + ext_ben],
                    fill='toself', fillcolor='rgba(46,204,113,0.2)',
                    line=dict(color='rgba(46,204,113,0.5)'),
                    name='Ganho Social Potencial',
                ))

            fig4.add_trace(go.Scatter(x=[q_priv_ep], y=[60 - 2 * q_priv_ep], mode='markers',
                                      marker=dict(size=10, color='#4ecdc4'), name=f'Mercado (Q={q_priv_ep:.1f})'))
            fig4.add_trace(go.Scatter(x=[q_soc_ep], y=[60 + ext_ben - 2 * q_soc_ep], mode='markers',
                                      marker=dict(size=10, color='#2ecc71'), name=f'Ótimo Social (Q*={q_soc_ep:.1f})'))

            fig4.update_layout(
                template='plotly_dark', paper_bgcolor='#0e1117', plot_bgcolor='#1a1a2e',
                xaxis=dict(title='Q', gridcolor='#2a2a4e'), yaxis=dict(title='P', gridcolor='#2a2a4e'),
                height=420, margin=dict(l=50, r=30, t=30, b=50),
                legend=dict(bgcolor='rgba(26,26,46,0.8)', bordercolor='#0f3460'),
            )
            st.plotly_chart(fig4, use_container_width=True)

    # ── Tragédia dos Comuns ────────────────────────────────────────────────────
    with tab_tragedia:
        st.markdown("### Simulação: Tragédia dos Comuns")
        col_tc1, col_tc2 = st.columns([1, 2])

        with col_tc1:
            n_agentes = st.slider("Número de agentes", 2, 20, 5, key="tc_n")
            capacidade = st.slider("Capacidade do recurso", 50, 200, 100, key="tc_cap")
            st.markdown(f"""
            Cada agente decide quanto explorar do recurso comum.
            - Se a exploração total excede **{capacidade}**, o recurso se esgota.
            - Sem regulação, cada agente maximiza seu ganho individual,
              ignorando o custo imposto aos demais.
            """)

        with col_tc2:
            # Simulação simples: benefício individual decresce com uso total
            uso_individual = np.linspace(1, capacidade / n_agentes * 2, 100)
            uso_total = uso_individual * n_agentes

            beneficio_ind = uso_individual * (1 - uso_total / (2 * capacidade))
            beneficio_ind = np.maximum(beneficio_ind, 0)

            beneficio_social = beneficio_ind * n_agentes

            # Ótimo individual (sem coordenação)
            idx_max_ind = np.argmax(beneficio_ind)
            # Ótimo social
            idx_max_soc = np.argmax(beneficio_social * (1 - uso_total / capacidade))

            fig5 = go.Figure()
            fig5.add_trace(go.Scatter(
                x=uso_individual, y=beneficio_ind, mode='lines',
                line=dict(color='#e94560', width=2.5), name='Benefício Individual'
            ))
            fig5.add_trace(go.Scatter(
                x=uso_individual, y=beneficio_social * (1 - uso_total / capacidade), mode='lines',
                line=dict(color='#2ecc71', width=2.5, dash='dash'), name='Benefício Social Sustentável'
            ))

            # Linha de capacidade
            cap_per_agent = capacidade / n_agentes
            fig5.add_vline(x=cap_per_agent, line=dict(color='#f9d923', width=1.5, dash='dot'),
                           annotation_text=f"Capacidade/agente = {cap_per_agent:.0f}")

            fig5.update_layout(
                template='plotly_dark', paper_bgcolor='#0e1117', plot_bgcolor='#1a1a2e',
                xaxis=dict(title='Uso Individual', gridcolor='#2a2a4e'),
                yaxis=dict(title='Benefício', gridcolor='#2a2a4e'),
                height=420, margin=dict(l=50, r=30, t=30, b=50),
                legend=dict(bgcolor='rgba(26,26,46,0.8)', bordercolor='#0f3460'),
            )
            st.plotly_chart(fig5, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 8 — FUNÇÕES DE MUSGRAVE
# ════════════════════════════════════════════════════════════════════════════════
with tabs[7]:
    st.markdown("## Funções do Governo — Classificação de Musgrave")

    col_m1, col_m2 = st.columns(2)

    with col_m1:
        st.markdown("""
        <div class="concept-card">
            <h3>🎯 Função Alocativa</h3>
            <p>Intervenção para garantir a oferta de bens e serviços que o mercado não provê
            adequadamente: bens públicos, bens meritórios (educação, saúde) e regulação de
            monopólios naturais e externalidades.</p>
        </div>
        <div class="concept-card">
            <h3>💰 Função Distributiva</h3>
            <p>Ajuste da distribuição de renda via tributação progressiva, transferências
            diretas (Bolsa Família), salário mínimo, serviços públicos universais e
            políticas de acesso.</p>
        </div>
        <div class="concept-card">
            <h3>📈 Função Estabilizadora</h3>
            <p>Uso de política monetária (juros, câmbio) e fiscal (gastos, impostos)
            para manter estabilidade de preços, pleno emprego e crescimento sustentável.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        # Gráfico: Composição dos gastos públicos (dados ilustrativos Brasil)
        categorias = [
            'Previdência Social', 'Saúde', 'Educação', 'Defesa',
            'Assistência Social', 'Infraestrutura', 'Juros da Dívida', 'Outros'
        ]

        # Sliders para o mix
        st.markdown("### Simule a Composição dos Gastos Públicos (%)")
        gastos = {}
        defaults = [35, 12, 10, 5, 8, 6, 18, 6]
        funcoes = ['Estabilizadora', 'Alocativa', 'Alocativa/Distributiva', 'Alocativa',
                   'Distributiva', 'Alocativa', 'Estabilizadora', 'Mista']
        cores_funcao = {
            'Alocativa': '#4ecdc4',
            'Distributiva': '#e94560',
            'Estabilizadora': '#f9d923',
            'Alocativa/Distributiva': '#a855f7',
            'Mista': '#a7b5c9',
        }

        for cat, default in zip(categorias, defaults):
            gastos[cat] = default

        labels = [f"{cat}" for cat in categorias]
        values = list(gastos.values())
        colors = [cores_funcao.get(f, '#a7b5c9') for f in funcoes]

        fig6 = go.Figure(data=[go.Pie(
            labels=labels, values=values,
            hole=0.45,
            marker=dict(colors=colors, line=dict(color='#1a1a2e', width=2)),
            textinfo='label+percent',
            textfont=dict(size=12),
        )])
        fig6.update_layout(
            template='plotly_dark', paper_bgcolor='#0e1117',
            height=420,
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(bgcolor='rgba(26,26,46,0.8)', bordercolor='#0f3460', font=dict(size=11)),
            annotations=[dict(text='Gastos<br>Públicos', x=0.5, y=0.5, font_size=14,
                              font_color='#a7b5c9', showarrow=False)],
        )
        st.plotly_chart(fig6, use_container_width=True)

    # Mapeamento funções → instrumentos
    st.markdown("---")
    st.markdown("### Instrumentos por Função")
    instr_df = pd.DataFrame({
        "Função": ["Alocativa", "Alocativa", "Alocativa", "Distributiva", "Distributiva", "Distributiva",
                    "Estabilizadora", "Estabilizadora", "Estabilizadora"],
        "Instrumento": [
            "Provisão de bens públicos (defesa, iluminação)",
            "Regulação de monopólios naturais (ANEEL, ANATEL)",
            "Imposto de Pigou / Subsídio para externalidades",
            "Imposto de renda progressivo",
            "Transferências diretas (Bolsa Família)",
            "Serviços públicos universais (SUS, educação)",
            "Taxa Selic (política monetária)",
            "Gastos públicos anticíclicos",
            "Metas de inflação"
        ],
        "Exemplo Concreto": [
            "Forças Armadas, faróis marítimos",
            "Tarifas de energia reguladas",
            "ICMS sobre cigarro, subsídio à pesquisa",
            "Alíquotas de 7,5% a 27,5% no IRPF",
            "R$ 600/mês por família elegível",
            "Atendimento gratuito no SUS",
            "Selic a 13,75% para conter inflação",
            "PAC (Programa de Aceleração do Crescimento)",
            "Banco Central persegue meta de 3% a.a."
        ],
    })
    st.dataframe(instr_df, use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 9 — QUIZ INTERATIVO
# ════════════════════════════════════════════════════════════════════════════════
with tabs[8]:
    st.markdown("## 🧠 Quiz — Teste seu Conhecimento")
    st.markdown("Responda às questões abaixo para verificar o aprendizado sobre o papel do Estado na economia.")

    # Banco de questões
    questions = [
        {
            "q": "1. O que significa uma alocação ser 'ótima de Pareto'?",
            "options": [
                "Todos os agentes têm a mesma renda",
                "Não é possível melhorar a situação de um agente sem piorar a de outro",
                "O governo maximiza a arrecadação tributária",
                "A produção está no máximo tecnologicamente possível"
            ],
            "answer": 1,
            "explanation": "Uma alocação é ótima de Pareto quando todas as trocas mutuamente benéficas foram exploradas — melhorar um agente necessariamente piora outro."
        },
        {
            "q": "2. Qual o principal problema dos bens públicos?",
            "options": [
                "São muito caros de produzir",
                "O governo proíbe o setor privado de produzi-los",
                "O problema do 'carona' (free rider) — ninguém quer pagar voluntariamente",
                "Não existem exemplos reais de bens públicos"
            ],
            "answer": 2,
            "explanation": "Como bens públicos são não-excludentes e não-rivais, agentes racionais preferem usufruir sem pagar (free rider), impedindo a provisão pelo mercado."
        },
        {
            "q": "3. Na empresa monopolista, qual a relação entre preço (P) e custo marginal (CMg)?",
            "options": [
                "P = CMg (como na concorrência perfeita)",
                "P < CMg (o monopolista cobra menos)",
                "P > CMg (o monopolista cobra mais que o custo marginal)",
                "Não há relação entre P e CMg"
            ],
            "answer": 2,
            "explanation": "O monopolista opera onde RMg = CMg, mas como a RMg é menor que P (pela demanda negativamente inclinada), resulta P > CMg, gerando peso morto."
        },
        {
            "q": "4. O que é o Imposto de Pigou?",
            "options": [
                "Um imposto sobre lucros extraordinários",
                "Um imposto que visa internalizar o custo de uma externalidade negativa",
                "Um imposto sobre heranças e doações",
                "Um imposto que financia bens meritórios"
            ],
            "answer": 1,
            "explanation": "O Imposto de Pigou é um tributo igual ao custo externo marginal, fazendo o poluidor pagar pelo dano social causado e levando o mercado ao ótimo social."
        },
        {
            "q": "5. O Segundo Teorema Fundamental do Bem-Estar afirma que:",
            "options": [
                "Toda economia de mercado é naturalmente justa",
                "O governo nunca deve intervir na economia",
                "Toda alocação eficiente de Pareto pode ser alcançada via mercado com redistribuição adequada",
                "Mercados monopolistas são sempre eficientes"
            ],
            "answer": 2,
            "explanation": "O Segundo Teorema diz que não é preciso abandonar o mercado para atingir distribuição desejada — basta redistribuir dotações iniciais e deixar o mercado competitivo funcionar."
        },
        {
            "q": "6. A 'Tragédia dos Comuns' se refere a:",
            "options": [
                "A falência de empresas públicas",
                "A superutilização de recursos comuns (não-excludentes e rivais)",
                "A escassez de bens artificialmente escassos",
                "O monopólio natural em serviços essenciais"
            ],
            "answer": 1,
            "explanation": "Recursos comuns (ex: peixes, pastagens) são rivais mas não-excludentes, levando cada agente a explorar em excesso sem considerar o impacto nos demais."
        },
        {
            "q": "7. Qual das seguintes NÃO é uma função do governo segundo Musgrave?",
            "options": [
                "Função Alocativa",
                "Função Distributiva",
                "Função Competitiva",
                "Função Estabilizadora"
            ],
            "answer": 2,
            "explanation": "As três funções de Musgrave são: Alocativa (prover bens públicos e regular falhas), Distributiva (redistribuir renda), e Estabilizadora (estabilizar moeda e emprego)."
        },
        {
            "q": "8. Seleção adversa ocorre quando:",
            "options": [
                "O governo seleciona políticas econômicas inadequadas",
                "Apenas agentes de baixa qualidade participam do mercado devido à assimetria de informação",
                "Firmas selecionam tecnologias obsoletas",
                "Consumidores escolhem bens substitutos mais baratos"
            ],
            "answer": 1,
            "explanation": "Na seleção adversa, uma parte tem mais informação que a outra. Ex: no mercado de seguros, pessoas de alto risco têm mais incentivo a participar, elevando os custos para todos."
        },
        {
            "q": "9. Qual é um exemplo de externalidade positiva?",
            "options": [
                "Poluição industrial",
                "Congestionamento no trânsito",
                "Educação pública",
                "Formação de cartel"
            ],
            "answer": 2,
            "explanation": "A educação gera benefícios que vão além do indivíduo (redução de criminalidade, maior produtividade social), sendo uma externalidade positiva clássica."
        },
        {
            "q": "10. Monopólios naturais se justificam quando:",
            "options": [
                "O governo proíbe a concorrência",
                "Há custos médios decrescentes / rendimentos crescentes de escala",
                "A demanda pelo produto é muito baixa",
                "Existe excesso de oferta no mercado"
            ],
            "answer": 1,
            "explanation": "Em setores como água e energia, os custos fixos são tão altos que uma única firma operando é mais eficiente que várias competindo — é o monopólio natural."
        },
        {
            "q": "11. O que a Taxa Marginal de Substituição (TMS) representa?",
            "options": [
                "A quantidade total consumida pelo agente",
                "A taxa à qual o consumidor troca um bem pelo outro mantendo a utilidade constante",
                "O custo marginal de produção",
                "A alíquota de imposto sobre o consumo"
            ],
            "answer": 1,
            "explanation": "A TMS mede a inclinação da curva de indiferença — quanto do bem 2 o consumidor está disposto a sacrificar por uma unidade adicional do bem 1, mantendo a utilidade constante."
        },
        {
            "q": "12. No equilíbrio competitivo, a condição de eficiência na troca exige que:",
            "options": [
                "Todos os consumidores tenham a mesma renda",
                "TMS de todos os consumidores seja igual à razão de preços p₁/p₂",
                "O governo fixe os preços dos bens",
                "A produção seja maximizada independentemente das preferências"
            ],
            "answer": 1,
            "explanation": "A eficiência na troca requer TMS^a = TMS^b = ... = p₁/p₂. Como todos enfrentam os mesmos preços, a concorrência perfeita garante essa condição automaticamente."
        },
        {
            "q": "13. O Primeiro Teorema Fundamental do Bem-Estar afirma que:",
            "options": [
                "O governo deve sempre intervir na economia",
                "Uma economia competitiva é eficiente no sentido de Pareto",
                "O monopólio é a forma mais eficiente de organização",
                "A distribuição de renda em mercados livres é sempre justa"
            ],
            "answer": 1,
            "explanation": "O 1º Teorema diz que, sob certas condições (informação perfeita, tomadores de preço), o equilíbrio competitivo é automaticamente eficiente de Pareto."
        },
        {
            "q": "14. A firma minimiza custos quando:",
            "options": [
                "Usa o menor número possível de insumos",
                "TMST (isoquanta) iguala a razão dos preços dos insumos w₁/w₂",
                "Produz a maior quantidade possível",
                "Todas as firmas usam a mesma tecnologia"
            ],
            "answer": 1,
            "explanation": "A condição de custo mínimo é TMST = w₁/w₂, que equivale à tangência entre isoquanta e isocusto. Isso garante que a firma use a combinação mais barata de insumos."
        },
        {
            "q": "15. Na Curva de Possibilidades de Produção (CPP), a eficiência na composição do produto exige:",
            "options": [
                "Produzir apenas um tipo de bem",
                "TMS = TMST = TMT = p₁/p₂",
                "Operar dentro (abaixo) da CPP",
                "Que o governo decida a composição ideal"
            ],
            "answer": 1,
            "explanation": "Na composição ótima do produto, a TMS (preferências) iguala a TMST (produção) iguala a TMT (inclinação da CPP), todos iguais à razão de preços. Isso garante que se produz o que os consumidores desejam."
        },
    ]

    # Inicializar state
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False

    for i, q in enumerate(questions):
        st.markdown(f"### {q['q']}")
        key = f"q_{i}"
        selected = st.radio(
            "Escolha uma alternativa:",
            q["options"],
            key=key,
            index=None,
            label_visibility="collapsed",
        )
        if selected is not None:
            st.session_state.quiz_answers[i] = q["options"].index(selected)

    st.markdown("---")
    if st.button("📝 Verificar Respostas", type="primary", use_container_width=True):
        st.session_state.quiz_submitted = True

    if st.session_state.quiz_submitted:
        score = 0
        total = len(questions)

        for i, q in enumerate(questions):
            user_ans = st.session_state.quiz_answers.get(i, -1)
            correct = user_ans == q["answer"]
            if correct:
                score += 1
                st.markdown(f"""
                <div class="quiz-correct">
                    ✅ <strong>{q['q']}</strong><br>
                    <em>{q['explanation']}</em>
                </div>
                """, unsafe_allow_html=True)
            else:
                chosen = q["options"][user_ans] if user_ans >= 0 else "Não respondida"
                st.markdown(f"""
                <div class="quiz-incorrect">
                    ❌ <strong>{q['q']}</strong><br>
                    Sua resposta: {chosen}<br>
                    Resposta correta: <strong>{q['options'][q['answer']]}</strong><br>
                    <em>{q['explanation']}</em>
                </div>
                """, unsafe_allow_html=True)

        pct = (score / total) * 100
        emoji = "🏆" if pct >= 80 else "👍" if pct >= 60 else "📚"
        color = "#2ecc71" if pct >= 80 else "#f9d923" if pct >= 60 else "#e94560"

        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #1a1a2e, #16213e); border: 2px solid {color};
                    border-radius: 16px; padding: 2rem; text-align: center; margin-top: 1.5rem;">
            <h1 style="color: {color}; margin: 0;">{emoji} {score}/{total}</h1>
            <h3 style="color: #a7b5c9; margin: 0.5rem 0 0 0;">Sua pontuação: {pct:.0f}%</h3>
            <p style="color: #c4cdd8; margin-top: 0.5rem;">
                {'Excelente! Você domina o conteúdo.' if pct >= 80 else
                 'Bom trabalho! Revise os pontos errados.' if pct >= 60 else
                 'Continue estudando! Revise o material e tente novamente.'}
            </p>
        </div>
        """, unsafe_allow_html=True)

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📖 Sobre")
    st.markdown("""
    Dashboard educacional para estudo do
    **Mercado Competitivo** e do
    **Papel do Estado na Economia**.

    **Conteúdo coberto:**
    - Teoria do Consumidor
    - Teoria da Firma
    - Equilíbrio Geral & 1º Teorema
    - Eficiência de Pareto
    - Falhas de mercado
    - Bens públicos e externalidades
    - Funções de Musgrave
    - Monopólio e concorrência

    ---
    *Desenvolvido com Streamlit + Plotly*
    """)

    st.markdown("## 📚 Tópicos Rápidos")
    with st.expander("Teoria do Consumidor"):
        st.markdown("Maximização de U(x) s.a. restrição orçamentária. "
                     "Condição: TMS = p₁/p₂ (tangência).")
    with st.expander("Teoria da Firma"):
        st.markdown("Maximização de lucro / minimização de custo. "
                     "Condição: TMST = w₁/w₂ (tangência isoquanta-isocusto).")
    with st.expander("1º Teorema do Bem-Estar"):
        st.markdown("Uma economia competitiva é eficiente de Pareto. "
                     "TMS = TMST = TMT = razão de preços.")
    with st.expander("Eficiência de Pareto"):
        st.markdown("Situação onde não se pode melhorar um agente sem piorar outro. "
                     "Não garante equidade — pode haver extrema desigualdade.")
    with st.expander("Segundo Teorema do Bem-Estar"):
        st.markdown("Qualquer ótimo de Pareto pode ser alcançado via mercado, "
                     "desde que haja redistribuição adequada de recursos.")
    with st.expander("Peso Morto"):
        st.markdown("Perda de eficiência causada pelo monopólio: a sociedade perde "
                     "bem-estar porque quantidades menores são produzidas a preços maiores.")
    with st.expander("Teorema de Coase"):
        st.markdown("Se os custos de transação são zero, a negociação privada resolve "
                     "externalidades independentemente da atribuição inicial de direitos.")
