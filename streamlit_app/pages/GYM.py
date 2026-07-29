import streamlit as st
import pandas as pd
# from pandas.tseries.offsets import DateOffset
from datetime import datetime, timedelta

from utils import st_write_justify,update_github_json,select_all,insert_one
import time
import numpy as np
import plotly.express as px
from translations import t

st.set_page_config(
    page_title=t("gym_title", st.session_state.lang),
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown('<h1 class="section-header">' + "💪" + t("gym_title", st.session_state.lang) + '</h1>', unsafe_allow_html=True)

df = pd.DataFrame(select_all('gym'))

lang = st.session_state.lang

col1, col2, col3 = st.columns([1, 1, 1])

with col1:

    st.selectbox(t("gym_training",lang), options=np.sort(df['number'].unique())[::-1],key="select_traine_page")
    df = df[df['number'] == st.session_state.select_traine_page]

with col2:

    if "grupo_sugerido" in st.session_state:
        st.session_state["grupo_sugerido"]
        index_grupo_df = np.where(df['group'] == st.session_state["grupo_sugerido"])[0][0]
        st.session_state["grupo_sugerido"] = None
    else:
        index_grupo_df = 0
    

    list_group = st.selectbox(t("gym_series",lang), np.sort(df['group'].unique()), index=index_grupo_df)
    df = df[df['group'] == list_group]

with col3:

    segundos = st.number_input(t("gym_break",lang),value=60,step=5)

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


try:
    # Renomear colunas
    resultado.columns = [
        'Exercise',
        'Series',
        'exercise_order',
        '3 Weeks',
        'Last',
        'Now'
    ]
except:
    try:
        resultado.columns = [
            'Exercise',
            'Series',
            'exercise_order',
            'Last',
            'Now'
        ]
    except:
        resultado.columns = [
            'Exercise',
            'Series',
            'exercise_order',
            'Now'
        ]

resultado['Dif'] = resultado['Now'] - resultado['Last']

try:
    resultado['Proposition'] = np.where(
        resultado['Dif'] == 0,
        (resultado['Now'] - resultado['3 Weeks']),
        resultado['Dif']
    )
except:
    resultado['Proposition'] = 0

resultado['Proposition'] = np.where(
    resultado['Proposition'] == 0,
    resultado['Now'] * 1.08,
    resultado['Now']
)
# else:
#     resultado['Proposition'] = resultado['Proposition'] + resultado['Now']

resultado['Exercise'] = resultado['Exercise'].str.capitalize()

# df_exdad = resultado.copy()

# st.markdown("""
# <style>
# .card {
#     background: linear-gradient(145deg, #1E293B, #0F172A);
#     padding: 20px;
#     border-radius: 16px;
#     border: 1px solid #263449;
#     box-shadow: 0px 6px 18px rgba(0,0,0,0.35);
#     margin-bottom: 15px;
#     display: flex;
#     align-items: center;
#     justify-content: space-between;
#     gap: 16px;
# }

# .metric {
#     font-size: 22px;
#     font-weight: 800;
#     color: #22C55E;
#     margin-top: 2px;
# }

# .badge {
#     display: inline-block;
#     padding: 4px 10px;
#     border-radius: 999px;
#     background-color: #22C55E;
#     color: #0F172A;
#     font-size: 15px;
#     font-weight: 700;
#     margin-top: 4px;
# }
# </style>
# """, unsafe_allow_html=True)






if "historico" not in st.session_state:
    st.session_state.historico = []

if "saved" not in st.session_state:
    st.session_state.saved = []


for exercise in resultado['Exercise'].unique():

    with st.expander(exercise,key=f'my_expander_id_{exercise}'):
        
        placeholder = st.empty()

        col1, col2, col3, col4, col5, col6      = st.columns([1,1,2.5,2.5,1,1])
    
        with col1:

            st.markdown("""
            <style>
            .center-column {
                display: flex;
                justify-content: center;
            }
            </style>
            """, unsafe_allow_html=True)

            if st.button(t("gym_start",lang),key=f'exercise_button_id_{exercise}',width='stretch'):
                        
                        horario_fim = datetime.now() + timedelta(seconds=segundos) - timedelta(hours=3)

                        for i in range(segundos, -1, -1):

                            mins, secs = divmod(i, 60)

                            placeholder.markdown(
                                f"""
                                <h1 style='text-align:center;font-size:50px;'>
                                    {mins:02d}:{secs:02d}
                                </h1>
                                """,
                                unsafe_allow_html=True
                            )

                            time.sleep(1)
                        st.session_state.historico.append(f'exercise_button_id_{exercise}')

        quantidade = st.session_state.historico.count(f'exercise_button_id_{exercise}')

        df_result = resultado[['Exercise','Now','Proposition']]
        df_result = df_result[df_result['Exercise'] == exercise]
        df_result['Performed'] = quantidade

        with col2:

            new_weight = st.number_input(t("gym_weight",lang),value=df_result['Now'].iloc[0],step=0.5,key=f'exercise_number_id_{exercise}')

        df_update_github = df[df['exercise'] == exercise.lower()].reset_index(drop=True)

        df_update_github = df_update_github.sort_values('dt_ymd', ascending=True).reset_index(drop=True)
        df_update_github = df_update_github.tail(1).reset_index(drop=True)

        df_done_check = df_update_github['dt_ymd'].iloc[0]
        df_update_github['weight'] = new_weight
        df_update_github['dt_ymd'] = datetime.now().strftime('%Y-%m-%d')

        df_data = resultado[resultado['Exercise'] == exercise].reset_index()

        data = df_data['Series'].iloc[0]

        if data == st.session_state.historico.count(f'exercise_button_id_{exercise}'):

            st.write('Updating...')

            insert_one("gym", df_update_github.iloc[0].to_dict())

            st.write('Done')

            st.session_state.historico = []

        with col3:

            st.metric("🏋️ Atual", f"{df_result['Now'].iloc[0]:.1f} kg", border=True)

        with col4:

            st.metric("🎯 Meta", f"{df_result['Proposition'].iloc[0]:.1f} kg", delta='8%', width="stretch", height="content",border=True)

        with col5:

            st.markdown("""
            <style>
            .center-column {
                display: flex;
                justify-content: center;
                align-items:center;
            }
            </style>
            """, unsafe_allow_html=True)

            st.button(t("gym_save",lang),key=f'save_button_id_{exercise}',on_click=insert_one,args=("gym", df_update_github.iloc[0].to_dict()),width='stretch')

        with col6:

            st.markdown("""
            <style>
            .center-column {
                display: flex;
                justify-content: center;
                align-items:center;
            }
            </style>
            """, unsafe_allow_html=True)

            if df_done_check == datetime.now().date():
                st.session_state[f'checkbox_id_{exercise}'] = True
            else:
                st.session_state[f'checkbox_id_{exercise}'] = False

            st.checkbox(t("gym_done", lang), key=f'checkbox_id_{exercise}',width='stretch')


try:
    resultado_dataframe = resultado[['Exercise','3 Weeks','Last', 'Now', 'Dif']]
except:
    try:
        resultado_dataframe = resultado[['Exercise','Last', 'Now', 'Dif']]
    except:
        resultado_dataframe = resultado[['Exercise', 'Now', 'Dif']]


st.dataframe(resultado_dataframe.style.format({
'3 Weeks': '{:.1f}',
'Last': '{:.1f}',
'Now': '{:.1f}',
'Dif': '{:.1f}'
}).highlight_between('Dif',left=0.1, right=10,color='green'),hide_index=True,height=(len(resultado_dataframe) + 1) * 36,
    column_config={
        "Exercise": st.column_config.TextColumn(width="medium"),
        "3 Weeks": st.column_config.NumberColumn(width="small"),
        "Last": st.column_config.NumberColumn(width="small"),
        "Now": st.column_config.NumberColumn(width="small"),
        "Dif": st.column_config.NumberColumn(width="small"),
    })

