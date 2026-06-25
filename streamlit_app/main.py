import streamlit as st
from translations import t

if "lang" not in st.session_state:
        st.session_state.lang = "pt"

pg = st.navigation([
    st.Page("pages/GYM.py", title="💪" + t("gym_title", st.session_state.lang)),
    st.Page("pages/DIET.py", title=t("diet_title", st.session_state.lang)),
])

with st.sidebar:

    col_pt, col_en = st.columns(2)
 
    with col_pt:
        pt_type = "primary" if st.session_state.lang == "pt" else "secondary"
        if st.button('BR', key="lang_btn_pt", width='stretch', type=pt_type):
            st.session_state.lang = "pt"
            st.rerun()

    with col_en:
        en_type = "primary" if st.session_state.lang == "en" else "secondary"
        if st.button("EN", key="lang_btn_en", width='stretch', type=en_type):
            st.session_state.lang = "en"
            st.rerun()

    st.link_button('DEV: Alexandre Santucci','https://www.linkedin.com/in/alexandre-santucci-breves-oliveira/',width='stretch')

pg.run()
