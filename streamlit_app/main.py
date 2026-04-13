import streamlit as st
import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
from datetime import datetime
from utils import st_write_justify,message_whatsapp,message_email


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
         , "👨‍💻 Experience"
         , "🎓 Education"
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
                , 'company_photo': 'https://media.licdn.com/dms/image/v2/D4E0BAQFGw9nfFeGHQw/company-logo_200_200/B4EZu09jBnKQAI-/0/1768267592168/pluxee_br_logo?e=1777507200&v=beta&t=4SRLoHB6xTSQVQGyEwjZx18Njy1i8CsysDdy4thWl9s'
                , "period": "nov/25 - Present"
                , "description": "Developing"
                , 'tools' : 'Python, Power BI, SQL, VBA, Excel'
            },
            {
                "role": "Data Analyst"
                , "empresa": "Vila 11"
                , 'company_photo': 'https://media.licdn.com/dms/image/v2/D4D0BAQFCJ39PonRwVA/company-logo_200_200/company-logo_200_200/0/1727445742003/vila11_logo?e=1777507200&v=beta&t=coJLMwQXZ3CKzh4Kxaz0JH0QuX8qiSzmf6EU1rpIzP8'
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
                , 'company_photo': 'https://media.licdn.com/dms/image/v2/D4D0BAQHSpZ63oeMgeA/company-logo_200_200/company-logo_200_200/0/1714513065939/oioficial_logo?e=1777507200&v=beta&t=0dDqJXjhhxLgErwkPoQoTfxaJz_zs_doBZPAAUa_OsU'
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
            st.image("https://media.licdn.com/dms/image/v2/D4D03AQEbV3zhJKzI6Q/profile-displayphoto-shrink_400_400/B4DZU9ppbnHAAg-/0/1740496083441?e=1777507200&v=beta&t=9uxudj9nSV47mvdk4AVD8awfzlk31pX39fljAq3-lHc", 
                    width=100
                    )
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
                        st.image(exp['company_photo'],width="content")

                    with col_met2:
                        st_write_justify(exp['description'],skill_to_view)

                    with col_met3:
                        st.metric("Clientes Satisfeitos", "95%", "2%")
        
        # Upload de arquivo (demonstração)
        # st.markdown("### 📎 Upload de Currículo")
        # uploaded_file = st.file_uploader("Faça upload do seu currículo", type=['pdf', 'docx'])
        # if uploaded_file is not None:
        #     st.success(f"Arquivo {uploaded_file.name} carregado com sucesso!")

# # Página de experiência
elif menu_option == "👨‍💻 Experience":
    st.markdown('<h1 class="section-header">In Developtment</h1>', unsafe_allow_html=True)
    
#     profile_data = load_profile_data()
    
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
elif menu_option == "🎓 Education":
    st.markdown('<h1 class="section-header">In Developtment</h1>', unsafe_allow_html=True)
    
#     profile_data = load_profile_data()
    
#     for edu in profile_data["educacao"]:
#         with st.container():
#             st.markdown(f"### {edu['curso']}")
#             st.markdown(f"**{edu['instituicao']}**")
#             st.markdown(f"*{edu['periodo']}*")
#             st.markdown("---")

# # Página de habilidades
elif menu_option == "🛠️ Habilities":
    st.markdown('<h1 class="section-header">In Developtment</h1>', unsafe_allow_html=True)
    
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

                message_whatsapp(full_text)                # message_email(mensagem)

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