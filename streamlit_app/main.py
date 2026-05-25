import streamlit as st
import pandas as pd
from pandas.tseries.offsets import DateOffset
# import plotly.express as px
# import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils import st_write_justify
# ,message_whatsapp,message_email
import time
import holidays

# Configuração da página
st.set_page_config(
    page_title="Professional Hub",
    page_icon="💼​",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 3rem;
#         color: #0e76a8;
#         text-align: center;
#         margin-bottom: 2rem;
#     }
#     .section-header {
#         font-size: 1.8rem;
#         color: #0e76a8;
#         border-bottom: 2px solid #0e76a8;
#         padding-bottom: 0.5rem;
#         margin-top: 2rem;
#     }
#     .card {
#         background-color: #f0f2f6;
#         padding: 1.5rem;
#         border-radius: 10px;
#         margin: 1rem 0;
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#     }
# </style>
# """, unsafe_allow_html=True)

# Barra lateral
with st.sidebar:
    # st.image("https://cdn-icons-png.flaticon.com/512/174/174857.png", width=50)

    menu_option = st.radio(
        "Sessions:",
        ["🏠 Start"
        #  , "💪​ Gym"
         , "💵​ Education"
         , "🛠️ Habilities"
         , "📊 Analytics"
         , "📞 Contact"]
    )
    
    st.markdown("---")
    st.markdown("### Streamlit Resources Used:")
    st.info("""
        - ✅ Responsive layout
        - ✅ Interactive widgets
        - ✅ Session state
        - ✅ Data caching
        - ✅ Custom markdown
        - ✅ Multimedia components
    """)

        # - ✅ Dynamic charts
        # - ✅ File upload
# Dados de exemplo
@st.cache_data
def load_profile_data():
    return {
        "name": "Alexandre Santucci",
        "location": "São Paulo, Brasil",
        "resume": "Data Analyst with over 10 years of experience, specializing in transforming complex data into strategic insights and automated solutions that enhance operational efficiency and drive data-driven decision-making. Technical expertise in Power BI, Python, SQL, and Azure Databricks, with strong ability to communicate insights clearly to stakeholders across diverse departments. Proactive and analytical professional with proven experience in solving complex challenges and collaborating effectively within multidisciplinary teams. Continuously seeking to optimize processes and maximize data value through technical and interpersonal skills.",
        "experiences": [
            {
                "role": "Senior Data Analyst"
                , "empresa": "Pluxee Brasil"
                , 'company_photo': 'pluxee_br_logo'
                , "period": "nov/25 - Present"
                , "description": "Developing"
                , 'tools' : 'Python, Power BI, SQL, VBA, Excel'
            },
            {
                "role": "Data Analyst"
                , "empresa": "Vila 11"
                , 'company_photo': 'vila11_logo'
                , "period": "abr/25 - nov/25"
                , "description": "Developed interactive Power BI dashboards integrated with Azure Databricks data pipelines, providing real-time strategic insights to marketing and sales teams. "
                    "Automated data collection, transformation, and loading processes using Power Automate and Python, reducing processing time by 35% and increasing data reliability. "
                    "Built predictive models in Python to identify market trends and customer behaviors, supporting data-driven decision-making. "
                    "Collaborated with cross-functional teams to define relevant KPIs and metrics, ensuring alignment with business objectives. "
                    "Implemented automated reporting solutions, enabling the sales team to quickly access insights and make more assertive decisions. "
                , 'tools' : 'Python, Power BI, SQL, VBA, Excel, DataBricks'
            },
            {
                "role": "Data Analyst"
                , "empresa": "Oi"
                , 'company_photo': 'oioficial_logo'
                , "period": "abr/25 - nov/25"
                , "description": 'Developed an interactive Python dashboard using Streamlit, connected to SQL and SharePoint databases, to optimize resource allocation and productivity analysis. The solution replaced manual processes and third-party software, resulting in annual cost savings of R$200,000 and improved decision-making through dynamic visualizations and predictive insights. '
                    'Created SQL stored procedures and complex views to streamline integration with managerial dashboards, accelerating data collection and organization. '
                    'Designed dynamic and interactive Power BI dashboards using sources such as SQL, Excel, and SharePoint, enabling deep and real-time analysis of key performance indicators (KPIs). '
                    'Automated data collection and analysis processes using VBA, Python, and R, reducing processing time by up to 40% and increasing operational efficiency. '
                    'Led corporate OKR analysis and proposed improvements based on insights, optimizing team performance and alignment with organizational goals. '
                , 'tools' : 'Python, Power BI, SQL, VBA, Excel'
            }
            # ,{"cargo": "Data Scientist Pleno", "empresa": "Vila 11", "periodo": "apr/25 - nov/25", "descricao": "Desenvolvimento de modelos preditivos..."},
            # {"cargo": "Analista de Dados", "empresa": "Oi S/A", "periodo": "2015 - 2017", "descricao": "Análise de dados de marketing..."}
        ]
        
    }

# Página inicial
if menu_option == "🏠 Start":
    
    profile_data = load_profile_data()

    list_tools = list(dict.fromkeys(
        tool
        for exp in profile_data['experiences']
        for tool in exp['tools'].split(', ')
    ))
    
    col1, col2 = st.columns([1, 2.5])
    
    with col1:

        col_aux1, col_aux2 = st.columns([1,2])

        with col_aux1:
            try:
                st.image('streamlit_app/images/1740496083441.jfif',width=100)
            except:
                st.image('images/1740496083441.jfif',width=100)

        with col_aux2:

            st.markdown(f"### {profile_data['name']}")
            st.markdown(f"**{profile_data['experiences'][0]['role']}**")
            st.markdown(f"📍 {profile_data['location']}")
            
        st.markdown("### 📝 Professional Resume")
        # st.write(f'{profile_data["resume"]}')
        st_write_justify(profile_data["resume"])

    with col2:
        
        # st.header('👨‍💼 Perfil Profissional')
        st.header('📈 Tools and Projects')
        skill_to_view = st.selectbox("Select Tool:", list_tools)
        # Métricas rápidas
        # st.markdown("### 📊 Métricas")
        # col_met1, col_met2, col_met3 = st.columns(3)

        for exp in profile_data['experiences']:
            if skill_to_view in exp['tools']:
                container_box = st.container(border=True)
                with container_box:
                    col_met1, col_met2, col_met3 = st.columns([1,4,1])

                    with col_met1:
                        try:
                            st.image(f'streamlit_app/images/{exp['company_photo']}.jfif'  ,width="content")
                        except:
                            st.image(f'images/{exp['company_photo']}.jfif'  ,width="content")

                        

                    with col_met2:
                        st_write_justify(exp['description'],skill_to_view)

                    with col_met3:
                        st.metric("Clientes Satisfeitos", "95%", "2%")
        
        # Upload de arquivo (demonstração)
        # st.markdown("### 📎 Upload de Currículo")
        # uploaded_file = st.file_uploader("Faça upload do seu currículo", type=['pdf', 'docx'])
        # if uploaded_file is not None:
        #     st.success(f"Arquivo {uploaded_file.name} carregado com sucesso!")

# # # Página de experiência
# elif menu_option == "💪​ Gym":
#     st.markdown('<h1 class="section-header">Gym</h1>', unsafe_allow_html=True)
    
#     try:
#         df = pd.read_excel('streamlit_app/arquivo_gym.xlsx')
#     except:
#         df = pd.read_excel('arquivo_gym.xlsx')

#     # Converter data
#     # df['dt_ymd'] = pd.to_datetime(df['dt_ymd'], dayfirst=True)

#     # Converter peso
#     df['weight'] = (
#         df['weight']
#         .str.replace(',', '.', regex=False)
#         .astype(float)
#     )

#     list_group = st.radio("Select:", df['group'].unique(),horizontal=True)

#     df = df[df['group'] == list_group]

#     # Ordenar
#     # df = df.sort_values(['exercise', 'dt_ymd'])

#     col1, col2 = st.columns([2, 1.5])
        
#     with col1:
        
#         df_graph = df.sort_values(['exercise', 'dt_ymd'])
#         st.line_chart(df_graph,x='dt_ymd',y='weight',color='exercise')

#     # Pegar últimos 2 registros de cada exercício
#     ultimos = df.groupby('exercise').tail(2)

#     # Criar ranking dentro do exercício
#     ultimos['ordem'] = ultimos.groupby('exercise').cumcount() + 1

#     # Pivotar
#     resultado = ultimos.pivot(
#         index='exercise',
#         columns='ordem',
#         values='weight'
#     ).reset_index()

#     # Renomear colunas
#     resultado.columns = [
#         'Exercise',
#         'Last',
#         'Now'
#     ]
    
#     resultado['Dif'] = resultado['Now'] - resultado['Last']
    
#     resultado['Exercise'] = resultado['Exercise'].str.capitalize()

#     resultado[['Last', 'Now', 'Dif']] = resultado[['Last', 'Now', 'Dif']].round(1)


#     with col2:

#         st.dataframe(resultado.style.format({
#         'Last': '{:.1f}',
#         'Now': '{:.1f}',
#         'Dif': '{:.1f}'
#     }).highlight_between('Dif',left=0.1, right=10,color='green'),hide_index=True,height=(len(resultado) + 1) * 36)


#     st.title("🏋️ Timer de Descanso")

#     # session state para guardar histórico
#     if "historico" not in st.session_state:
#         st.session_state.historico = []

#     segundos = st.slider(
#         "Segundos",
#         45,
#         120,
#         60
#     )

#     placeholder = st.empty()

#     if st.button("▶️ Start"):

#         horario_fim = datetime.now() + timedelta(seconds=segundos)

#         for i in range(segundos, -1, -1):

#             mins, secs = divmod(i, 60)

#             placeholder.markdown(
#                 f"""
#                 <h1 style='text-align:center;font-size:80px;'>
#                     {mins:02d}:{secs:02d}
#                 </h1>

#                 <h3 style='text-align:center;'>
#                     Termina às {horario_fim.strftime("%H:%M:%S")}
#                 </h3>
#                 """,
#                 unsafe_allow_html=True
#             )

#             time.sleep(1)

#         # adiciona nova linha no histórico
#         st.session_state.historico.append(
#             f"✅ Descanso finalizado às {datetime.now().strftime('%H:%M:%S')}"
#         )

#     # printa todas as execuções
#     for item in st.session_state.historico:
#         st.success(item)

# #     profile_data = load_profile_data()
    
#     for exp in profile_data["experiencias"]:
#         with st.container():
#             col1, col2 = st.columns([3, 1])
#             with col1:
#                 st.markdown(f"### {exp['cargo']}")
#                 st.markdown(f"**{exp['empresa']}**")
#                 st.markdown(exp['descricao'])
#             with col2:
#                 st.markdown(f"*{exp['periodo']}*")
#             st.markdown("---")

# # Página de educação
elif menu_option == "💵​ Education":
    st.markdown('<h1 class="section-header">Fixo</h1>', unsafe_allow_html=True)
    
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

    # list_group = st.selectbox("Select:", df['ANOMES'].unique())

    # df_filtro_1= df[df['ANOMES'] == list_group]

    # mes_anterior = (
    # pd.to_datetime(list_group, format='%m/%Y')
    # - DateOffset(months=1)
    # ).strftime('%m/%Y')

    # df_filtro_2 = df[df['ANOMES'] == mes_anterior]
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        list_group = st.selectbox('Mês',options=df['ANOMES'].unique())

        df_filtro_1= df[df['ANOMES'] == list_group]

        mes_anterior = (
        pd.to_datetime(list_group, format='%m/%Y')
        - DateOffset(months=1)
        ).strftime('%m/%Y')

        df_filtro_2 = df[df['ANOMES'] == mes_anterior]

    with col2:

        df_ops_1 = df_filtro_1.groupby('ANOMES').sum().reset_index()

        st.write('Valor Atual: ',df_ops_1['VALOR_DIVIDE'][0])
    
    with col3:
        try:
            df_ops_2 = df_filtro_2.groupby('ANOMES').sum().reset_index()

            st.write('Valor Anterior: ',df_ops_2['VALOR_DIVIDE'][0])
        except:
            st.write('Sem valor anterior')

    with col4:
        try:
            df_ops_1_2 = (df_ops_1['VALOR_DIVIDE'][0] - df_ops_2['VALOR_DIVIDE'][0]) * 100 / df_ops_2['VALOR_DIVIDE'][0]

            st.write('Aumento: ',df_ops_1_2.round(1),'%')
        except:
            st.write()
    # st.write(list_group.str[4:])

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

    # resultado[['Last', 'Now', 'Dif']] = resultado[['Last', 'Now', 'Dif']].round(1)
    
    st.dataframe(resultado.style.format({
        'Last': '{:.1f}',
        'Now': '{:.1f}',
        'Dif': '{:.1f}',
        '%': '{:.0f}'
    }).highlight_between('Dif',left=0.1, right=10000, color='red'),hide_index=True,height=(len(resultado) + 1) * 36)

# # Página de habilidades
elif menu_option == "🛠️ Habilities":
    st.markdown('<h1 class="section-header">In Developtment</h1>', unsafe_allow_html=True)
    

    # Feriados SP
    feriados = holidays.country_holidays("BR", subdiv="SP")

    # Criar calendário do ano inteiro
    datas = pd.date_range("2026-01-01", "2026-12-31")

    df = pd.DataFrame({"Data": datas})

    # Dia da semana (0=segunda, 6=domingo)
    df["DiaSemana"] = df["Data"].dt.weekday

    # Identificar fim de semana
    df["FimSemana"] = df["DiaSemana"] >= 5

    # Identificar feriado
    df["Feriado"] = df["Data"].isin(feriados)

    # Dias úteis
    df["DiaUtil"] = ~(df["FimSemana"] | df["Feriado"])

    # Mês
    df["Mes"] = df["Data"].values.astype("datetime64[M]")

    # Contagem de dias úteis
    dias_uteis = (
        df[df["DiaUtil"]]
        .groupby("Mes")
        .size()
        .reset_index(name="DiasUteis")
    )

    # Considerando 8h por dia
    HORAS_DIA = 8

    dias_uteis["HorasMes"] = dias_uteis["DiasUteis"] * HORAS_DIA

    st.write(dias_uteis)

    feriados_br = holidays.country_holidays("BR")

# Feriados estaduais SP (inclui nacionais também)
    feriados_sp = holidays.country_holidays("BR", subdiv="SP")

    feriados_sp_2 = feriados_sp["2024-01-01":"2024-12-31"]
    feriados_br_2 = feriados_br["2024-01-01":"2024-12-31"]
    print(feriados_sp_2)

    for feriado in feriados_sp_2:
        print(feriado)
    for feriado in feriados_br_2:
        print(feriado)
    # df = pd.DataFrame({"Data": datas})

    # df["Feriado"] = df["Data"].isin(feriados_sp_2)

    # # df = pd.DataFrame(dados, columns=["Data", "Feriado"])

    # st.dataframe(df, hide_index=True)
#     profile_data = load_profile_data()
    
#     # Gráfico de barras para habilidades
#     skills_df = pd.DataFrame({
#         'Habilidade': list(profile_data["habilidades"].keys()),
#         'Nível': list(profile_data["habilidades"].values())
#     })
    
#     fig = px.bar(skills_df, x='Nível', y='Habilidade', orientation='h',
#                  color='Nível', color_continuous_scale='Blues')
#     fig.update_layout(title="Nível de Habilidades Técnicas", height=400)
#     st.plotly_chart(fig, use_container_width=True)
    
#     # Filtro interativo
#     st.markdown("### 🔍 Filtro de Habilidades")
#     min_level = st.slider("Nível mínimo:", 0, 100, 70)
    
#     filtered_skills = {k: v for k, v in profile_data["habilidades"].items() if v >= min_level}
    
#     col1, col2 = st.columns(2)
#     with col1:
#         st.markdown("**Habilidades Filtradas:**")
#         for skill, level in filtered_skills.items():
#             st.progress(level/100, text=f"{skill}: {level}%")
    
#     with col2:
#         st.metric("Total de Habilidades", len(filtered_skills))

# Página de analytics
elif menu_option == "📊 Analytics":
    st.markdown('<h1 class="section-header">In Developtment</h1>', unsafe_allow_html=True)
    
#     # Dados simulados para demonstração
#     @st.cache_data
#     def generate_analytics_data():
#         return pd.DataFrame({
#             'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
#             'Visualizações do Perfil': [120, 150, 180, 220, 190, 250],
#             'Conexões': [45, 52, 48, 60, 55, 65],
#             'Engajamento': [75, 80, 78, 85, 82, 90]
#         })
    
#     analytics_df = generate_analytics_data()
    
#     # Gráficos interativos
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.markdown("### 📈 Visualizações do Perfil")
#         fig = px.line(analytics_df, x='Mês', y='Visualizações do Perfil', 
#                      title="Evolução das Visualizações")
#         st.plotly_chart(fig, use_container_width=True)
    
#     with col2:
#         st.markdown("### 🔗 Crescimento da Rede")
#         fig = px.area(analytics_df, x='Mês', y='Conexões', 
#                      title="Conexões Realizadas")
#         st.plotly_chart(fig, use_container_width=True)
    
#     # Métricas dinâmicas
#     st.markdown("### 📋 Métricas de Engajamento")
#     metric_cols = st.columns(4)
    
#     with metric_cols[0]:
#         st.metric("Visualizações Totais", sum(analytics_df['Visualizações do Perfil']))
    
#     with metric_cols[1]:
#         st.metric("Novas Conexões", sum(analytics_df['Conexões']))
    
#     with metric_cols[2]:
#         st.metric("Taxa de Engajamento", f"{analytics_df['Engajamento'].mean():.1f}%")
    
#     with metric_cols[3]:
#         st.metric("Crescimento Mensal", "15%", "3%")

# Página de contato
elif menu_option == "📞 Contact":
    st.markdown('<h1 class="section-header">📞 Reach Me</h1>', unsafe_allow_html=True)
    
    # Formulário de contato
    with st.form("contact_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name*")
            company = st.text_input("Company")
        
        with col2:
            email = st.text_input("E-mail*")
            phone = st.text_input("Phone")
        
        subject = st.selectbox("Subject", [
            "Work proposal", "Partnership", 
            "Professional Consult", "Others"
        ])
        
        message = st.text_area("Message*", height=150)

        submitted_whatsapp = st.form_submit_button("Send WhatsApp",icon=":material/business_messages:",help='Required to be logged into WhatsApp Web')


        # col1, col2 = st.columns(2)
        # with col1:
        #     submitted_whatsapp = st.form_submit_button("Enviar WhatsApp",icon=":material/business_messages:",help='Necessário estar logado no WhatsApp Web')
        
        # with col2:
        #     submitted_mail = st.form_submit_button("Enviar e-mail",icon=":material/mail:",help='Necessário estar logado no Gmail')
        

        if submitted_whatsapp:

            if name and email and message:
                st.success("✅ All fields provided.")
                
                full_text = f'Hi Alexandre, my name is {name}.\nI work for {company}.\nI would really like to talk about {subject}.\n{message}'

                # message_whatsapp(full_text)                # message_email(mensagem)

                # Demonstração do session state
                if 'messages_sent' not in st.session_state:
                    st.session_state.messages_sent = 0
                st.session_state.messages_sent += 1
                
                st.info(f"📨 Total messages sent in this session: {st.session_state.messages_sent}")
            else:
                st.error("❌ Please fill in all required fields (*)")
        
        # if submitted_mail:

        #     if nome and email and mensagem:
        #         st.success("✅ Mensagem enviada com sucesso! Entrarei em contato em breve.")
                
        #         # message_whatsapp(mensagem)
        #         message_email(mensagem,assunto)

        #         # Demonstração do session state
        #         if 'messages_sent' not in st.session_state:
        #             st.session_state.messages_sent = 0
        #         st.session_state.messages_sent += 1
                
        #         st.info(f"📨 Total de mensagens enviadas nesta sessão: {st.session_state.messages_sent}")
        #     else:
        #         st.error("❌ Por favor, preencha todos os campos obrigatórios (*)")

# Rodapé
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "🚀 This page demonstrates the main features of Streamlit | "
    "Developed by Alexandre Santucci"
    "</div>", 
    unsafe_allow_html=True
)