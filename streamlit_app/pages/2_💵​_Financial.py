
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
        # df = pd.read_excel('streamlit_app/arquivo_gym.xlsx')
        df = pd.read_json('streamlit_app/financial.json')
        
    except:
        # df = pd.read_excel('arquivo_gym.xlsx')
        df = pd.read_json('financial.json')


    # Converter peso
    df['value'] = pd.to_numeric(df['value'], errors='coerce')

    df['value_divide'] = df['value'] * df['modifier']

    df = df.sort_values(['anomes'],ascending=False)

    


    df['anomes'] = pd.to_datetime(
    pd.to_numeric(df['anomes'], errors='coerce')
    .fillna(0)
    .astype(int)
    .astype(str),
    format='%Y%m',
    errors='coerce'
    ).dt.strftime('%m/%Y')

    df = df[df['anomes'].notna()]

    df['type'] = df['type'].str.lower()

    df_bills = df[~df['type'].isin(['investment', 'extras'])]

    df_extras = df[df['type'].isin(['extras'])]

    col1, col2, col3 = st.columns([0.7, 1, 1])

    with col1:
        list_group = st.selectbox('Month',options=df_bills['anomes'].unique())

        df_filtro_1 = df_bills[df_bills['anomes'] == list_group]

        df_filtro_1_extras = df_extras[df_extras['anomes'] == list_group]

        mes_anterior = (
        pd.to_datetime(list_group, format='%m/%Y')
        - DateOffset(months=1)
        ).strftime('%m/%Y')

        df_filtro_2 = df_bills[df_bills['anomes'] == mes_anterior]

    df_ops_1 = df_filtro_1.groupby('anomes').sum().reset_index()

    df_ops_1 = df_ops_1['value_divide'].iloc[0]

    

    df_ops_1_extras = df_filtro_1_extras.groupby('type').sum().reset_index()
    try:
        df_ops_1_extras = df_ops_1_extras['value_divide'].iloc[0]

        df_ops_1_extras_detail = ''

        for i in range(0,len(df_filtro_1_extras)):

            df_ops_1_extras_detail = df_ops_1_extras_detail + df_filtro_1_extras['detail'].iloc[i] + ' '
    except:
        df_ops_1_extras = None
    try:
        df_ops_2 = df_filtro_2.groupby('anomes').sum().reset_index()
        
        df_ops_2 = df_ops_2['value_divide'].iloc[0]

    except:
        df_ops_2 = 0

    try:
        df_ops_1_2 = round((df_ops_1 - df_ops_2) * 100 / df_ops_2,1)

    except:
        df_ops_1_2 = 0.0

    with col2:
        try:
            st.metric("Present", f"{df_ops_1:,.0f} + {df_ops_1_extras:,.0f} ", f"{df_ops_1_2}%",delta_color="inverse",help=df_ops_1_extras_detail,border=True)
        except:
            st.metric("Present", f"{df_ops_1:,.0f}", f"{df_ops_1_2}%",delta_color="inverse",border=True)

    with col3:

        st.metric("Past", f"{df_ops_2:,.0f}",border=True)

    df_filtrado = df_bills[
    (df_bills['anomes'] >= mes_anterior) &
    (df_bills['anomes'] <= list_group)
    ]

    df_filtrado = df_filtrado.sort_values(['type', 'anomes'])

    ultimos = df_filtrado.groupby('type').tail(2)

    ultimos['ordem'] = ultimos.groupby('type').cumcount()  + 1

    # Pivotar
    try:
        resultado = ultimos.pivot(
            index='type',
            columns='ordem',
            values='value'
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
        resultado = ultimos[['type','value_divide']]

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

    df_dates = pd.DataFrame({"Data": datas})

    st.write(feriados_sp_2)

    # Dia da semana (0=segunda, 6=domingo)
    df_dates["DiaSemana"] = df_dates["Data"].dt.weekday

    # Identificar fim de semana
    df_dates["FimSemana"] = df_dates["DiaSemana"] >= 5

    # Identificar feriado
    df_dates["Feriado"] = df_dates["Data"].isin(feriados_sp_2)

    # Dias úteis
    df_dates["DiaUtil"] = ~(df_dates["FimSemana"] | df_dates["Feriado"])

    # Mês
    df_dates["Month"] = df_dates["Data"].dt.strftime('%m')

    # Contagem de dias úteis
    dias_uteis = (
        df_dates[df_dates["DiaUtil"]]
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

# st.write(df)



df_investment = None

try:
    # Tenta abrir o arquivo da pasta
    df_investment = df[df['type'].isin(['investment'])]

except:
    st.warning("Arquivo não encontrado. Faça upload do Excel.")

    arquivo_upload = st.file_uploader(
        "Selecione um arquivo Excel",
        type=["xlsx", "xls"]
    )

    if arquivo_upload:
        df_investment = pd.read_excel(arquivo_upload)
        st.success("Arquivo enviado com sucesso.")

arquivo_upload = st.file_uploader(
    "Selecione um arquivo Excel",
    type=["xlsx", "xls"]
)

if arquivo_upload:
    df_investment = pd.read_excel(arquivo_upload)
    st.success("Arquivo enviado com sucesso.")
else:
    df_investment = df[df['type'].isin(['investment'])]


investment_goal = st.number_input("Goal/per month",min_value=5000,value=30000,step=100)        

df_investment['year'] = df_investment['anomes'].str[3:]

df_investment['month'] = df_investment['anomes'].str[:2]

resultado = pd.pivot_table(
    df_investment,
    index='year',
    columns='month',
    values='value',
    aggfunc='sum'
).reset_index()

st.dataframe(
    resultado.style.format(
        {col: "{:,.2f}" for col in resultado.select_dtypes(include='number').columns}
    ),
    hide_index=True
)

