
import streamlit as st
from streamlit_image_select import image_select
from translations import t

if "lang" not in st.session_state:
        st.session_state.lang = "pt"
import traceback

try:
    if not st.user.is_logged_in:
        st.login('google')
        st.stop()
except Exception as e:
    st.error("Error: " + str(e))
    # st.code(traceback.format_exc())

pg = st.navigation([
    st.Page("pages/CALENDAR.py", title="📅" + t("calendar", st.session_state.lang)),
    st.Page("pages/GYM.py", title="💪" + t("gym_title", st.session_state.lang)),
    st.Page("pages/DIET.py", title=t("diet_title", st.session_state.lang)),
])

# Captura qual botão foi clicado

with st.sidebar:

    if "valor_antigo" not in st.session_state:
        st.session_state.valor_antigo = "https://flagcdn.com/w160/br.png"

    lang = image_select(
        label="Language / Idioma",
        images=[
            "https://flagcdn.com/w160/br.png",
            "https://flagcdn.com/w160/gb.png",
        ],
        captions=["", ""],
        use_container_width=True,
    )

    if lang.endswith("br.png"):
        st.session_state.lang = "pt"
        # st.rerun()

    elif lang.endswith("gb.png"):
        st.session_state.lang = "en"
        # st.rerun()
        

    if lang != st.session_state.valor_antigo:

        st.session_state.valor_antigo = lang
        st.rerun()


    # if st.button("Sair",width='stretch'):
    #     st.logout() 

    st.link_button('DEV: Alexandre Santucci','https://www.linkedin.com/in/alexandre-santucci-breves-oliveira/',width='stretch')


pg.run()
