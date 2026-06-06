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
    # df = pd.read_excel('streamlit_app/arquivo_gym.xlsx')
    df = pd.read_json('streamlit_app/gym.json')
    
except:
    # df = pd.read_excel('arquivo_gym.xlsx')
    df = pd.read_json('gym.json')

# Converter data
# df['dt_ymd'] = pd.to_datetime(df['dt_ymd'], dayfirst=True)

# Converter peso
df['weight'] = (pd.to_numeric(df['weight'], errors='coerce'))

list_group = st.selectbox("Select:", np.sort(df['group'].unique()))

df = df[df['group'] == list_group]

# Ordenar
# df = df.sort_values(['exercise', 'dt_ymd'])



col1, col2 = st.columns([2, 1.5])
    
with col1:
    
    df_graph = df.sort_values(['exercise', 'dt_ymd'])

    df_graph['dt_ymd'] = pd.to_datetime(df_graph['dt_ymd'])
    df_graph['ds_dt_ymd'] = df_graph['dt_ymd'].dt.strftime('%d/%m/%y')

    st.line_chart(df_graph,x='ds_dt_ymd',y='weight',color='exercise',x_label='Date',y_label='Weight')

# Pegar últimos 2 registros de cada exercício
ultimos = df.groupby('exercise').tail(3)

# Criar ranking dentro do exercício
ultimos['ordem'] = ultimos.groupby(['exercise','series','exercise_order']).cumcount() + 1

# Pivotar
resultado = ultimos.pivot(
    index=['exercise','series','exercise_order'],
    columns='ordem',
    values='weight'
).reset_index()

resultado = resultado.sort_values(['exercise_order']).reset_index(drop=True)

# Renomear colunas
resultado.columns = [
    'Exercise',
    'Series',
    'exercise_order',
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

# with st.container():

#     col1, col2 = st.columns([1, 3])

#     with col2:
#         st.title("🏋️ Timer de Descanso")

#     with col1:
#         segundos = st.number_input(
#             "Break",
#             min_value=0,
#             value=60,
#             step=1,
#             label_visibility="collapsed"
#         )
col1, col2 = st.columns([4, 1])

with col1:
    st.markdown("### 🏋️ Timer de Descanso")

with col2:
    segundos = st.number_input(
        "Break",
        value=60,
        label_visibility="collapsed"
    )
    # st.title("🏋️ Timer de Descanso")


    # segundos = st.number_input(
    #     "Break",
    #     min_value=0,
    #     value=60,
    #     step=1
    # )

if "historico" not in st.session_state:
    st.session_state.historico = []

try:
    # st.write(st.session_state.historico)  

    for exercise in resultado['Exercise'].unique():

        # st.write(st.session_state.historico.count(f'my_button_id_{exercise}'))
        
        df_result = resultado[resultado['Exercise'] == exercise].reset_index()

        data = df_result['Series'].iloc[0]

        # st.write(data)

        if data == st.session_state.historico.count(f'my_button_id_{exercise}'):
             
             resultado = resultado[resultado['Exercise'] != exercise]



        # if exercise_count == 

except:
     st.write('no session')

radio_exercise = st.radio('Radio:',resultado['Exercise'].unique())

placeholder = st.empty()

if st.button("▶️ Start",key=f'my_button_id_{radio_exercise}'):
            
            horario_fim = datetime.now() + timedelta(seconds=segundos) - timedelta(hours=3)

            for i in range(segundos, -1, -1):

                mins, secs = divmod(i, 60)

                placeholder.markdown(
                    f"""
                    <h1 style='text-align:center;font-size:50px;'>
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
            st.session_state.historico.append(f'my_button_id_{radio_exercise}')

quantidade = st.session_state.historico.count(f'my_button_id_{radio_exercise}')

df_result = resultado[['Exercise','Now','Proposto']]
df_result = df_result[df_result['Exercise'] == radio_exercise]
df_result['Quantidade'] = quantidade

st.dataframe(df_result,hide_index=True)

# col_c1, col_c2 = st.columns([7,3])
# for line in range(0,len(resultado)):
#     with col_c1:

        
#             df_resultado_proposto = resultado[['Exercise','Now','Proposto']]
            
#             st.dataframe(df_resultado_proposto.iloc[[line]].style.format({'Now': '{:.1f}','Proposto': '{:.0f}'}).highlight_between('Proposto',left=0, right=0,color='green').hide(axis="columns"),hide_index=True,width="content")
            
#     with col_c2:

#         if st.button("▶️ Start",key=f'my_button_id_{radio_exercise}'):
            
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
#         # st.write(f'my_button_id_{line}')
#             # # adiciona nova linha no histórico
#             st.session_state.historico.append(f'my_button_id_{radio_exercise}')
#         # st.write('')
#         # st.write('')

#         quantidade = st.session_state.historico.count(f'my_button_id_{radio_exercise}')

#         st.write(quantidade)
#         st.write(resultado['Series'][line])
#         if resultado['Series'][line] == quantidade:

#         # st.write(quantidade)
#             st.checkbox('done',value=True,key=f'my_checkbox_id_{radio_exercise}')
#         else:
#             st.checkbox('done',key=f'my_checkbox_id_{radio_exercise}')

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

