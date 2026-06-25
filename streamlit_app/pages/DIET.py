import streamlit as st
import pandas as pd
from datetime import datetime
from utils import st_write_justify, update_github_json
import numpy as np
import plotly.express as px
import requests
import json

st.set_page_config(
    page_title="Diet",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown('<h1 class="section-header">🥗 Plano Alimentar</h1>', unsafe_allow_html=True)

# ── Constante calórica (fórmula de Atwater) ────────────────────────────────────
# proteína: 4 kcal/g | carbo: 4 kcal/g | gordura: 9 kcal/g
# A IA usa isso como referência mas pode ajustar para alimentos específicos

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_MODEL      = "claude-sonnet-4-6"

# ── Função: busca macros de um alimento via IA ─────────────────────────────────
def buscar_macros_ia(food: str, quantity: float) -> dict:
    """
    Dado um alimento e quantidade, retorna macros e calorias estimados pela IA.
    Retorna dict: {"protein", "carbs", "fat", "calories", "note"}
    """
    prompt = f"""Você é um nutricionista especialista em tabelas nutricionais brasileiras (TACO, IBGE).

Estime os macronutrientes para o alimento abaixo na quantidade informada.

Alimento: {food}
Quantidade: {quantity}g/ml

Responda SOMENTE com um JSON válido, sem texto adicional, sem markdown, sem backticks:
{{"protein": <float>, "carbs": <float>, "fat": <float>, "calories": <float>, "note": "<observacao curta em portugues>"}}"""

    try:
        response = requests.post(
            ANTHROPIC_API_URL,
            headers={"Content-Type": "application/json"},
            json={
                "model": CLAUDE_MODEL,
                "max_tokens": 300,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=15
        )
        data = response.json()
        text = data["content"][0]["text"].strip()
        result = json.loads(text)
        return result
    except Exception as e:
        return {"protein": 0.0, "carbs": 0.0, "fat": 0.0, "calories": 0.0, "note": f"Erro IA: {e}"}


# ── Carrega dados ──────────────────────────────────────────────────────────────
try:
    df = pd.read_json('streamlit_app/diet.json')
except:
    df = pd.read_json('diet.json')

df['dt_ymd']   = pd.to_datetime(df['dt_ymd'], format='mixed', utc=True)
df['calories'] = pd.to_numeric(df['calories'], errors='coerce')
df['protein']  = pd.to_numeric(df['protein'],  errors='coerce')
df['carbs']    = pd.to_numeric(df['carbs'],    errors='coerce')
df['fat']      = pd.to_numeric(df['fat'],      errors='coerce')

# ── Session state ──────────────────────────────────────────────────────────────
if "diet_saved"   not in st.session_state: st.session_state.diet_saved   = []
if "ia_result"    not in st.session_state: st.session_state.ia_result    = {}
if "macros_result" not in st.session_state: st.session_state.macros_result = {}

# ── Filtros ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1])

with col1:
    meal_options  = np.sort(df['meal'].unique())
    selected_meal = st.selectbox("🍽️ Refeição:", ["Todas"] + list(meal_options))

with col2:
    date_options  = sorted(df['dt_ymd'].dt.date.unique(), reverse=True)
    selected_date = st.selectbox("📅 Data:", date_options)

# ── Filtra pelo dia ────────────────────────────────────────────────────────────
df_day = df[df['dt_ymd'].dt.date == selected_date].copy()
if selected_meal != "Todas":
    df_day = df_day[df_day['meal'] == selected_meal].copy()

# ── Resumo do dia ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📊 Resumo do Dia")

total_cal     = df_day['calories'].sum()
total_protein = df_day['protein'].sum()
total_carbs   = df_day['carbs'].sum()
total_fat     = df_day['fat'].sum()

mc1, mc2, mc3, mc4 = st.columns(4)
mc1.metric("🔥 Calorias",    f"{total_cal:.0f} kcal")
mc2.metric("💪 Proteína",    f"{total_protein:.1f} g")
mc3.metric("🍞 Carboidrato", f"{total_carbs:.1f} g")
mc4.metric("🥑 Gordura",     f"{total_fat:.1f} g")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SEÇÃO IA — Adicionar novo alimento com macros estimados pela IA
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### 🤖 Adicionar Alimento com IA")

with st.expander("➕ Novo alimento (IA estima os macros)", expanded=False):

    ia_col1, ia_col2, ia_col3 = st.columns([3, 1.5, 1])

    with ia_col1:
        novo_alimento = st.text_input("Nome do alimento", placeholder="ex: peito de frango grelhado")
    with ia_col2:
        nova_qtd = st.number_input("Quantidade (g/ml)", value=100.0, step=5.0, key="nova_qtd_ia")
    with ia_col3:
        meal_order_opts = ['Café da manhã','Lanche da manhã','Almoço','Lanche da tarde','Jantar','Ceia']
        nova_refeicao = st.selectbox("Refeição", meal_order_opts, key="nova_refeicao_ia")

    if st.button("🤖 Estimar macros com IA", key="btn_estimar_ia"):
        if novo_alimento.strip():
            with st.spinner("IA calculando macros..."):
                result = buscar_macros_ia(novo_alimento.strip(), nova_qtd)
                st.session_state.macros_result = result
        else:
            st.warning("Digite o nome do alimento.")

    # Mostra resultado da IA e permite editar antes de salvar
    if st.session_state.macros_result:
        r = st.session_state.macros_result

        st.info(f"💡 IA: {r.get('note','')}")

        ec1, ec2, ec3, ec4 = st.columns(4)
        with ec1: edit_protein = st.number_input("Proteína (g)", value=float(r.get('protein', 0)), step=0.5, key="edit_protein")
        with ec2: edit_carbs   = st.number_input("Carbo (g)",    value=float(r.get('carbs', 0)),   step=0.5, key="edit_carbs")
        with ec3: edit_fat     = st.number_input("Gordura (g)",  value=float(r.get('fat', 0)),     step=0.5, key="edit_fat")
        with ec4:
            # Recalcula calorias em tempo real com base nos macros editados
            cals_calculadas = round(edit_protein * 4 + edit_carbs * 4 + edit_fat * 9, 1)
            st.metric("🔥 Calorias (calculadas)", f"{cals_calculadas} kcal")

        if st.button("💾 Salvar novo alimento", key="btn_salvar_novo"):
            nova_linha = pd.DataFrame([{
                "dt_ymd":   datetime.now().strftime('%Y-%m-%d'),
                "meal":     nova_refeicao,
                "food":     novo_alimento.strip().lower(),
                "quantity": nova_qtd,
                "calories": cals_calculadas,
                "protein":  edit_protein,
                "carbs":    edit_carbs,
                "fat":      edit_fat
            }])
            update_github_json(nova_linha)
            st.success(f"✅ '{novo_alimento}' salvo com {cals_calculadas} kcal!")
            st.session_state.macros_result = {}

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# REFEIÇÕES DO DIA
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### 🍽️ Refeições")

meal_order    = ['Café da manhã', 'Lanche da manhã', 'Almoço', 'Lanche da tarde', 'Jantar', 'Ceia']
meals_to_show = [selected_meal] if selected_meal != "Todas" else meal_order

for meal in meals_to_show:
    df_meal = df_day[df_day['meal'] == meal].copy()
    if df_meal.empty:
        continue

    meal_cal     = df_meal['calories'].sum()
    meal_protein = df_meal['protein'].sum()
    meal_carbs   = df_meal['carbs'].sum()
    meal_fat     = df_meal['fat'].sum()

    expander_label = (
        f"{meal}  —  🔥 {meal_cal:.0f} kcal  |  "
        f"💪 {meal_protein:.1f}g  |  🍞 {meal_carbs:.1f}g  |  🥑 {meal_fat:.1f}g"
    )

    with st.expander(expander_label, key=f'expander_{meal}'):

        for _, row in df_meal.iterrows():
            food_key = f"{meal}_{row['food']}"
            ia_key   = f"ia_{food_key}"

            st.markdown(f"**{row['food'].capitalize()}**")

            col1, col2, col_btn_ia = st.columns([1.5, 6, 1])

            with col1:
                new_qty = st.number_input(
                    "Qtd (g/ml)",
                    value=float(row['quantity']),
                    step=5.0,
                    key=f'qty_{food_key}'
                )

            # Se a IA já rodou para este alimento, usa os valores dela como base
            ia_data = st.session_state.ia_result.get(ia_key)

            if ia_data:
                # IA retornou macros — usa como valores iniciais editáveis
                base_protein = float(ia_data.get('protein', row['protein']))
                base_carbs   = float(ia_data.get('carbs',   row['carbs']))
                base_fat     = float(ia_data.get('fat',     row['fat']))
                st.caption(f"🤖 IA estimou os macros para {new_qty}g/ml — {ia_data.get('note','')}")
            else:
                # Sem IA: recalcula proporcionalmente à quantidade
                ratio        = new_qty / row['quantity'] if row['quantity'] else 1
                base_protein = round(row['protein'] * ratio, 1)
                base_carbs   = round(row['carbs']   * ratio, 1)
                base_fat     = round(row['fat']     * ratio, 1)

            with col2:
                mc1, mc2, mc3, mc4 = st.columns(4)
                with mc1:
                    new_protein = st.number_input("💪 Proteína (g)", value=base_protein, step=0.5, key=f'prot_{food_key}')
                with mc2:
                    new_carbs   = st.number_input("🍞 Carbo (g)",    value=base_carbs,   step=0.5, key=f'carb_{food_key}')
                with mc3:
                    new_fat     = st.number_input("🥑 Gordura (g)",  value=base_fat,     step=0.5, key=f'fat_{food_key}')
                with mc4:
                    # Calorias sempre derivadas dos macros editados (Atwater)
                    new_cal = round(new_protein * 4 + new_carbs * 4 + new_fat * 9, 1)
                    st.metric("🔥 Calorias", f"{new_cal} kcal")

            with col_btn_ia:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🤖 IA", key=f'ia_btn_{food_key}', help="Buscar proteína, carbo e gordura com IA"):
                    with st.spinner("IA buscando macros..."):
                        res = buscar_macros_ia(row['food'], new_qty)
                        st.session_state.ia_result[ia_key] = res
                    st.rerun()

            # Prepara linha para salvar
            df_update = df[
                (df['food'] == row['food']) & (df['meal'] == meal)
            ].sort_values('dt_ymd', ascending=False).head(1).copy().reset_index(drop=True)

            df_update['quantity'] = new_qty
            df_update['calories'] = new_cal
            df_update['protein']  = new_protein
            df_update['carbs']    = new_carbs
            df_update['fat']      = new_fat
            df_update['dt_ymd']   = datetime.now().strftime('%Y-%m-%d')

            st.button(
                "💾 Salvar",
                key=f'save_{food_key}',
                on_click=update_github_json,
                args=(df_update,)
            )

            st.divider()

# ── Gráfico + tabela ───────────────────────────────────────────────────────────
st.markdown("---")
col_graph, col_table = st.columns([2, 1.5])

with col_graph:
    st.markdown("### 📈 Evolução de Calorias")

    df_graph = df.groupby(df['dt_ymd'].dt.date)['calories'].sum().reset_index()
    df_graph.columns = ['Data', 'Calorias']
    df_graph = df_graph.sort_values('Data')

    fig = px.line(df_graph, x='Data', y='Calorias', markers=True)
    fig.update_xaxes(tickformat="%d/%m/%y")
    st.plotly_chart(fig, use_container_width=True)

with col_table:
    st.markdown("### 🧾 Macros por Refeição")

    df_macros = df_day.groupby('meal').agg(
        Calorias=('calories', 'sum'),
        Proteína=('protein', 'sum'),
        Carboidrato=('carbs', 'sum'),
        Gordura=('fat', 'sum')
    ).reset_index().rename(columns={'meal': 'Refeição'})

    st.dataframe(
        df_macros.style.format({
            'Calorias':    '{:.0f}',
            'Proteína':    '{:.1f}',
            'Carboidrato': '{:.1f}',
            'Gordura':     '{:.1f}',
        }).highlight_max(subset=['Calorias'], color='#ffe0e0')
         .highlight_min(subset=['Calorias'], color='#e0ffe0'),
        hide_index=True,
        height=(len(df_macros) + 1) * 36
    )
