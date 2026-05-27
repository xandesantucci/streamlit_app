
import streamlit as st
import pandas as pd
from pandas.tseries.offsets import DateOffset
# from datetime import datetime, timedelta
# from utils import st_write_justify
# import time
# import numpy as np
import holidays

st.set_page_config(

    page_title="Financial",
    page_icon="💵",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown('<h1 class="section-header">💵 Financial</h1>', unsafe_allow_html=True)

col_fin1, col_fin2 = st.columns([1,1])
with col_fin1:
    try:
        df = pd.read_excel('streamlit_app/arquivo_fixo.xlsx')
    except:
        df = pd.read_excel('arquivo_fixo.xlsx')

    # Converter peso
    df['VALOR'] = (
        df['VALOR']
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False)
        .astype(float)
    )

    df['VALOR_DIVIDE'] = (
        df['VALOR_DIVIDE']
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False)
        .astype(float)
    )

    df = df.sort_values(['ANOMES'],ascending=False)

    df['ANOMES'] = pd.to_datetime(
    pd.to_numeric(df['ANOMES'], errors='coerce')
    .fillna(0)
    .astype(int)
    .astype(str),
    format='%Y%m',
    errors='coerce'
    ).dt.strftime('%m/%Y')

    df = df[df['ANOMES'].notna()]

    df['TIPO'] = df['TIPO'].str.lower()

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        list_group = st.selectbox('Mês',options=df['ANOMES'].unique())

        df_filtro_1= df[df['ANOMES'] == list_group]

        mes_anterior = (
        pd.to_datetime(list_group, format='%m/%Y')
        - DateOffset(months=1)
        ).strftime('%m/%Y')

        df_filtro_2 = df[df['ANOMES'] == mes_anterior]

    df_ops_1 = df_filtro_1.groupby('ANOMES').sum().reset_index()

    df_ops_1 = df_ops_1['VALOR_DIVIDE'].iloc[0]

    try:
        df_ops_2 = df_filtro_2.groupby('ANOMES').sum().reset_index()
        
        df_ops_2 = df_ops_2['VALOR_DIVIDE'].iloc[0]

    except:
        df_ops_2 = 0

    try:
        df_ops_1_2 = round((df_ops_1 - df_ops_2) * 100 / df_ops_2,1)

    except:
        df_ops_1_2 = 0.0

    with col2:

        st.metric("Present", f"{df_ops_1:,.2f}", f"{df_ops_1_2}%",delta_color="inverse")

    with col3:

        st.metric("Past", f"{df_ops_2:,.2f}")

    df_filtrado = df[
    (df['ANOMES'] >= mes_anterior) &
    (df['ANOMES'] <= list_group)
    ]

    df_filtrado = df_filtrado.sort_values(['TIPO', 'ANOMES'])

    ultimos = df_filtrado.groupby('TIPO').tail(2)

    ultimos['ordem'] = ultimos.groupby('TIPO').cumcount()  + 1

    # Pivotar
    try:
        resultado = ultimos.pivot(
            index='TIPO',
            columns='ordem',
            values='VALOR'
        ).reset_index()

        # Renomear colunas
        resultado.columns = [
            'Tipo',
            'Last',
            'Now'
        ]

        resultado['Dif'] = resultado['Now'] - resultado['Last']

        resultado['%'] = (resultado['Now'] - resultado['Last']) * 100 / resultado['Last']


    except:
        resultado = ultimos[['TIPO','VALOR_DIVIDE']]

        resultado['Last'] = 0
        resultado['Dif'] = 0
        resultado['%'] = 0

        resultado.columns = [
            'Tipo',
            'Now',
            'Last',
            'Dif',
            '%'
        ]

    resultado['Tipo'] = resultado['Tipo'].str.capitalize()


    st.dataframe(resultado.style.format({
        'Last': '{:.1f}',
        'Now': '{:.1f}',
        'Dif': '{:.1f}',
        '%': '{:.0f}'
    }).highlight_between('Dif',left=0.1, right=10000, color='red'),hide_index=True,height=(len(resultado) + 1) * 36)

with col_fin2:

    col_a1, col_a2, col_a3 = st.columns([1,1,1])

    with col_a1:

        salary_value = st.number_input("Salary/Hour",min_value=0.0,value=130.95,step=1.0)

    with col_a2:

        year_holidays = st.number_input("Year",min_value=2020,value=2026,step=1)

    year_holidays = str(year_holidays)
    # Feriados SP
    feriados_sp = holidays.country_holidays("BR", subdiv="SP")
    feriados_sp_2 = feriados_sp[f"{year_holidays}-01-01":f"{year_holidays}-12-31"]
    # Criar calendário do ano inteiro
    datas = pd.date_range(f"{year_holidays}-01-01", f"{year_holidays}-12-31")

    df = pd.DataFrame({"Data": datas})

    # Dia da semana (0=segunda, 6=domingo)
    df["DiaSemana"] = df["Data"].dt.weekday

    # Identificar fim de semana
    df["FimSemana"] = df["DiaSemana"] >= 5

    # Identificar feriado
    df["Feriado"] = df["Data"].isin(feriados_sp_2)

    # Dias úteis
    df["DiaUtil"] = ~(df["FimSemana"] | df["Feriado"])

    # Mês
    df["Month"] = df["Data"].dt.strftime('%m')

    # Contagem de dias úteis
    dias_uteis = (
        df[df["DiaUtil"]]
        .groupby("Month")
        .size()
        .reset_index(name="Useful_Days")
    )

    # Considerando 8h por dia
    HORAS_DIA = 8

    dias_uteis["Month_Hours"] = dias_uteis["Useful_Days"] * HORAS_DIA

    dias_uteis['Gross_Value'] = dias_uteis['Month_Hours'] * salary_value

    dias_uteis['Net_Value'] = dias_uteis['Gross_Value'] * 0.87

    sum_net = dias_uteis['Net_Value'].sum()

    with col_a3:
        st.metric('Net Total',f'{sum_net:,.2f}')

    # st.dataframe(dias_uteis)
    st.dataframe(dias_uteis.style.format({
            'Gross_Value': '{:,.2f}',
            'Net_Value': '{:,.2f}'
        }),height=(len(dias_uteis) + 1) * 36,hide_index=True)

df = None

try:
    # Tenta abrir o arquivo da pasta
    try:
        df = pd.read_excel('streamlit_app/arquivo_fixo.xlsx')
    except:
        df = pd.read_excel('arquivo_fixo.xlsx')

except:
    st.warning("Arquivo não encontrado. Faça upload do Excel.")

    arquivo_upload = st.file_uploader(
        "Selecione um arquivo Excel",
        type=["xlsx", "xls"]
    )

    if arquivo_upload:
        df = pd.read_excel(arquivo_upload)
        st.success("Arquivo enviado com sucesso.")

arquivo_upload = st.file_uploader(
    "Selecione um arquivo Excel",
    type=["xlsx", "xls"]
)

if arquivo_upload:
    df = pd.read_excel(arquivo_upload)
    st.success("Arquivo enviado com sucesso.")
else:
    try:
        df = pd.read_excel('streamlit_app/arquivo_fixo.xlsx')
    except:
        df = pd.read_excel('arquivo_fixo.xlsx')

# Mostra dados se existir
if df is not None:
    st.dataframe(df)
