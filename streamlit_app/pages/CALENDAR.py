"""
Página de Calendário de Treinos
--------------------------------
Consome o df vindo do Supabase (tabela 'gym') com as colunas:
    dt_ymd (date), number (int), group (text - letra A, B, C, D...),
    type (text), exercise (text), exercise_order (int),
    series (int), rep (int), weight (float)

Requisitos:
    pip install streamlit-calendar
"""

import pandas as pd
import streamlit as st
from streamlit_calendar import calendar
from datetime import date, timedelta
import colorsys
from utils import select_all
from translations import t

# Caminho da página "academia" usado pelo st.switch_page.
# Ajuste para o caminho real do arquivo dentro da pasta pages/ do seu app,
# por exemplo: "pages/1_academia.py" ou "pages/academia.py".
PAGINA_ACADEMIA = "pages/GYM.py"


# ----------------------------------------------------------------------
# 1. Preparação dos dados
# ----------------------------------------------------------------------

def preparar_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["dt_ymd"] = pd.to_datetime(df["dt_ymd"]).dt.date
    return df


def cor_por_grupo(letra: str) -> str:
    """Gera uma cor determinística (hex) a partir da letra do grupo,
    assim cada grupo (A, B, C, D...) sempre aparece com a mesma cor."""
    if not letra:
        return "#888888"
    idx = ord(letra.upper()[0]) - ord("A")
    hue = (idx * 0.15) % 1.0
    r, g, b = colorsys.hsv_to_rgb(hue, 0.55, 0.85)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"


def ordem_rotacao(df: pd.DataFrame) -> list:
    """Ordem das letras de grupo conforme a primeira vez que apareceram
    no histórico (ex: ['A', 'B', 'C', 'D'])."""
    df_ordenado = df.sort_values(["dt_ymd", "number"])
    ordem = df_ordenado["group"].drop_duplicates().tolist()
    return ordem


def proximo_grupo(df: pd.DataFrame):
    """Olha o maior 'number' (ciclo mais recente), pega o último 'group'
    treinado dentro desse ciclo (maior dt_ymd) e retorna a próxima letra
    da rotação."""
    if df.empty:
        return None

    ordem = ordem_rotacao(df)
    if not ordem:
        return None

    max_number = df["number"].max()
    df_ciclo = df[df["number"] == max_number]
    ultima_linha = df_ciclo.sort_values("dt_ymd").iloc[-1]
    ultimo_grupo = ultima_linha["group"]

    try:
        idx = ordem.index(ultimo_grupo)
    except ValueError:
        return ordem[0]

    prox = ordem[(idx + 1) % len(ordem)]
    return prox


def resumo_por_dia(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna, por dia, apenas o group/number treinado (sem contagens)."""
    return df[["dt_ymd", "group", "number"]].drop_duplicates().reset_index(drop=True)


def detalhe_treino_sugerido(df: pd.DataFrame, grupo: str) -> pd.DataFrame:
    """Retorna as séries/exercícios do último treino registrado para o
    'group' informado (o mais recente 'number' daquele grupo), para servir
    de base ao treino sugerido de hoje."""
    if not grupo:
        return pd.DataFrame()

    df_grupo = df[df["group"] == grupo]
    if df_grupo.empty:
        return pd.DataFrame()

    ultimo_number = df_grupo["number"].max()
    treino = df_grupo[df_grupo["number"] == ultimo_number].sort_values("exercise_order")
    return treino


# ----------------------------------------------------------------------
# 2. Construção dos eventos do calendário
# ----------------------------------------------------------------------

def montar_eventos(df: pd.DataFrame, sugestao_grupo):
    resumo = resumo_por_dia(df)
    hoje = date.today()
    treinou_hoje = hoje in df["dt_ymd"].values

    eventos = []
    for _, row in resumo.iterrows():
        cor = cor_por_grupo(row["group"])
        eventos.append(
            {
                "title": f"Treino {row['group']}",
                "start": row["dt_ymd"].isoformat(),
                "end": row["dt_ymd"].isoformat(),
                "color": cor,
                "extendedProps": {"group": row["group"], "number": row["number"]},
            }
        )

    # Evento de sugestão para hoje, só se ainda não tiver treino lançado
    if not treinou_hoje and sugestao_grupo:
        eventos.append(
            {
                "title": f"⭐ Sugestão: Treino {sugestao_grupo}",
                "start": hoje.isoformat(),
                "end": hoje.isoformat(),
                "color": "#444444",
                "textColor": "#ffffff",
                "extendedProps": {"sugestao": True, "group": sugestao_grupo},
            }
        )

    return eventos


# ----------------------------------------------------------------------
# 3. Página Streamlit
# ----------------------------------------------------------------------

def render_pagina_calendario(df: pd.DataFrame):
    st.title(t("calendar", st.session_state.lang))

    if df.empty:
        st.info("Nenhum treino encontrado ainda.")
        return

    df = preparar_df(df)
    sugestao = proximo_grupo(df)

    hoje = date.today()
    treinou_hoje = hoje in df["dt_ymd"].values

    col1, col2 = st.columns([3, 1])
    with col2:
        st.metric("Hoje", hoje.strftime("%d/%m/%Y"))
        if treinou_hoje:
            grupo_hoje = df.loc[df["dt_ymd"] == hoje, "group"].iloc[0]
            st.success(f"Treino de hoje: **{grupo_hoje}**")
        elif sugestao:
            st.warning(f"Próximo treino sugerido: **{sugestao}**")

    eventos = montar_eventos(df, sugestao)

    opcoes_calendario = {
        "initialView": "dayGridMonth",
        "initialDate": hoje.isoformat(),
        "locale": "pt-br",
        "firstDay": 1,
        "height": 700,
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,listMonth",
        },
    }

    with col1:
        estado_calendario = calendar(
            events=eventos,
            options=opcoes_calendario,
            key="calendario_treinos",
        )

    # ------------------------------------------------------------------
    # Detalhe do dia clicado
    # ------------------------------------------------------------------
    data_selecionada = None
    if estado_calendario and estado_calendario.get("callback") == "dateClick":
        data_selecionada = pd.to_datetime(
            estado_calendario["dateClick"]["date"]
        ).date()
    elif estado_calendario and estado_calendario.get("callback") == "eventClick":
        evento_clicado = estado_calendario["eventClick"]["event"]
        data_selecionada = pd.to_datetime(evento_clicado["start"]).date()

        props = evento_clicado.get("extendedProps", {})
        if props.get("sugestao"):
            grupo_sugerido = props.get("group")
            treino_sugerido = detalhe_treino_sugerido(df, grupo_sugerido)

            # Guarda o grupo e as séries sugeridas para a página academia usar
            st.session_state["grupo_sugerido"] = grupo_sugerido
            st.session_state["treino_sugerido"] = treino_sugerido.to_dict("records")
            st.switch_page(PAGINA_ACADEMIA)
            return

    if data_selecionada:
        st.subheader(f"Detalhes de {data_selecionada.strftime('%d/%m/%Y')}")
        dia_df = df[df["dt_ymd"] == data_selecionada]

        if dia_df.empty and data_selecionada == hoje and sugestao:
            st.write(f"Nenhum treino lançado ainda. Sugestão: **Treino {sugestao}**")
        elif dia_df.empty:
            st.write("Sem treino registrado nesse dia.")
        else:
            cols = ["type", "exercise", "series", "rep", "weight"]
            cols = [c for c in cols if c in dia_df.columns]
            st.dataframe(
                dia_df.sort_values("exercise_order")[cols].rename(
                    columns={
                        "type": "Grupo Muscular",
                        "exercise": "Exercício",
                        "series": "Séries",
                        "rep": "Reps",
                        "weight": "Carga (kg)",
                    }
                ),
                hide_index=True,
                use_container_width=True,
            )


# ----------------------------------------------------------------------
# Exemplo de uso dentro do app
# ----------------------------------------------------------------------
if __name__ == "__main__":
    st.set_page_config(page_icon="📅", page_title=t("calendar", st.session_state.lang), layout="wide")
    df = pd.DataFrame(select_all("gym"))
    render_pagina_calendario(df)