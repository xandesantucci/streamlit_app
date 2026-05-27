import streamlit as st
import pandas as pd
# from pandas.tseries.offsets import DateOffset
from datetime import datetime, timedelta
from utils import st_write_justify
import time
import numpy as np

st.set_page_config(

    page_title="Gym",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown('<h1 class="section-header">💪 Gym</h1>', unsafe_allow_html=True)

try:
    df = pd.read_excel('streamlit_app/arquivo_gym.xlsx')
except:
    df = pd.read_excel('arquivo_gym.xlsx')

# Converter data
# df['dt_ymd'] = pd.to_datetime(df['dt_ymd'], dayfirst=True)

# Converter peso
df['weight'] = (
    df['weight']
    .str.replace(',', '.', regex=False)
    .astype(float)
)

list_group = st.selectbox("Select:", np.sort(df['group'].unique()))

df = df[df['group'] == list_group]

# Ordenar
# df = df.sort_values(['exercise', 'dt_ymd'])



col1, col2 = st.columns([2, 1.5])
    
with col1:
    
    df_graph = df.sort_values(['exercise', 'dt_ymd'])
    st.line_chart(df_graph,x='dt_ymd',y='weight',color='exercise')

# Pegar últimos 2 registros de cada exercício
ultimos = df.groupby('exercise').tail(3)

# Criar ranking dentro do exercício
ultimos['ordem'] = ultimos.groupby(['exercise','series']).cumcount() + 1

# Pivotar
resultado = ultimos.pivot(
    index=['exercise','series'],
    columns='ordem',
    values='weight'
).reset_index()

# Renomear colunas
resultado.columns = [
    'Exercise',
    'Series',
    '3 Weeks',
    'Last',
    'Now'
]

resultado['Dif'] = resultado['Now'] - resultado['Last']

resultado['Proposto'] = np.where(
    resultado['Dif'] == 0,
    resultado['Now'] - resultado['3 Weeks'],
    resultado['Dif']
)

# resultado['Cap'] = np.where(resultado['Proposto'] == 0,'Aumenta','')

resultado['Exercise'] = resultado['Exercise'].str.capitalize()

# resultado[['3 Weeks','Last', 'Now', 'Dif']] = resultado[['3 Weeks','Last', 'Now', 'Dif']].round(1)

resultado_dataframe = resultado[['Exercise','3 Weeks','Last', 'Now', 'Dif']]

with col2:

    st.dataframe(resultado_dataframe.style.format({
    '3 Weeks': '{:.1f}',
    'Last': '{:.1f}',
    'Now': '{:.1f}',
    'Dif': '{:.1f}'
}).highlight_between('Dif',left=0.1, right=10,color='green'),hide_index=True,height=(len(resultado_dataframe) + 1) * 36)


st.title("🏋️ Timer de Descanso")

# session state para guardar histórico
if "historico" not in st.session_state:
    st.session_state.historico = []



# ultimos_aux = df.groupby('exercise').tail(1)
# st.write(ultimos_aux)

segundos = st.number_input(
"Break",
min_value=0,
value=60,
step=1
)
placeholder = st.empty()

# st.write(st.session_state.historico)


    
st.markdown("""
<style>

@media (max-width: 768px) {

    [data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
    }

    [data-testid="column"] {
        width: 100% !important;
        min-width: 100% !important;
    }

}

</style>
""", unsafe_allow_html=True)

col_c1, col_c2 = st.columns([7,3])
for line in range(0,len(resultado)):
    with col_c1:

        
            df_resultado_proposto = resultado[['Exercise','Now','Proposto']]
            
            st.dataframe(df_resultado_proposto.iloc[[line]].style.format({'Now': '{:.1f}','Proposto': '{:.0f}'}).highlight_between('Proposto',left=0, right=0,color='green').hide(axis="columns"),hide_index=True,width="content")
            
    with col_c2:

        if st.button("▶️ Start",key=f'my_button_id_{line}'):
            
            horario_fim = datetime.now() + timedelta(seconds=segundos)

            for i in range(segundos, -1, -1):

                mins, secs = divmod(i, 60)

                placeholder.markdown(
                    f"""
                    <h1 style='text-align:center;font-size:80px;'>
                        {mins:02d}:{secs:02d}
                    </h1>

                    <h3 style='text-align:center;'>
                        Termina às {horario_fim.strftime("%H:%M:%S")}
                    </h3>
                    """,
                    unsafe_allow_html=True
                )

                time.sleep(1)
        # st.write(f'my_button_id_{line}')
            # # adiciona nova linha no histórico
            st.session_state.historico.append(f'my_button_id_{line}')
        # st.write('')
        # st.write('')

        quantidade = st.session_state.historico.count(f'my_button_id_{line}')
        if resultado['Series'][line] == quantidade:

        # st.write(quantidade)
            st.checkbox('done',value=True,key=f'my_checkbox_id_{line}')
        else:
            st.checkbox('done',key=f'my_checkbox_id_{line}')

    # st.write(resultado['Exercise'][line])
    # st.write(resultado['Proposto'][line])

    # st.write(line)

# with col3:
#     for line in range(0,len(resultado)):   
#         if st.button("▶️ Start",key=f'my_button_id_{line}'):

#             horario_fim = datetime.now() + timedelta(seconds=segundos)

#             for i in range(segundos, -1, -1):

#                 mins, secs = divmod(i, 60)

#                 placeholder.markdown(
#                     f"""
#                     <h1 style='text-align:center;font-size:80px;'>
#                         {mins:02d}:{secs:02d}
#                     </h1>

#                     <h3 style='text-align:center;'>
#                         Termina às {horario_fim.strftime("%H:%M:%S")}
#                     </h3>
#                     """,
#                     unsafe_allow_html=True
#                 )

#                 time.sleep(1)

#             # adiciona nova linha no histórico
#             st.session_state.historico = st.session_state.historico + 1

# # printa todas as execuções
# for item in st.session_state.historico:
#     st.success(item)

