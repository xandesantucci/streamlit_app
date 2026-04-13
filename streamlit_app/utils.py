import re
import streamlit as st
import pywhatkit as kit
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

def st_write_justify(text, word='none', color="green"):
    if word != 'none':
        text = re.sub(
            word,
            lambda m: f"<span style='color:{color}; font-weight:bold'>{m.group(0)}</span>",
            text,
            flags=re.IGNORECASE
        )

    return st.markdown(
        f"<div style='text-align: justify;'>{text}</div>",
        unsafe_allow_html=True
    )


def message_whatsapp(mensagem):
    kit.sendwhatmsg_instantly("+5521980029229", mensagem)

# def message_email(mensagem,assunto):
#     from selenium import webdriver
#     from selenium.webdriver.common.by import By
#     from selenium.webdriver.common.keys import Keys
#     from webdriver_manager.chrome import ChromeDriverManager
#     from selenium.webdriver.chrome.service import Service
#     import time

#     # abrir navegador
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     driver.get("https://mail.google.com/")

#     # tempo para você logar manualmente
#     time.sleep(20)

#     # clicar em "Escrever"
#     driver.find_element(By.XPATH, "//div[text()='Escrever']").click()
#     time.sleep(3)

#     # destinatário
#     driver.find_element(By.NAME, "to").send_keys("destino@email.com")

#     # assunto
#     driver.find_element(By.NAME, "subjectbox").send_keys("Email automático via Python")

#     # corpo
#     body = driver.find_element(By.XPATH, "//div[@aria-label='Corpo da mensagem']")
#     body.send_keys("Olá! Este email foi enviado automaticamente via Python.")

#     # enviar
#     body.send_keys(Keys.CONTROL + Keys.ENTER)

#     time.sleep(5)
#     driver.quit()