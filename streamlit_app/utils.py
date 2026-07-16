import re
import streamlit as st
import requests
import json
import base64
import pandas as pd
# from github import Github
# import pywhatkit as kit
# # import smtplib
# # from email.mime.text import MIMEText
# # from email.mime.multipart import MIMEMultipart
import psycopg2
from psycopg2.extras import execute_values
from contextlib import contextmanager
import tomllib
from pathlib import Path

# ─────────────────────────────────────────────
# LEITURA DO CONFIG.TOML
# ─────────────────────────────────────────────
import os

def get_db_config() -> dict:
    """Lê config do st.secrets (produção) ou do toml local (desenvolvimento)."""
    try:
        # Produção: st.secrets disponível
        return {
            "host":            st.secrets["SUPABASE_HOST"],
            "port":            st.secrets.get("SUPABASE_PORT", "6543"),
            "dbname":          st.secrets.get("SUPABASE_DBNAME", "postgres"),
            "user":            st.secrets.get("SUPABASE_USER", "postgres.qyzfchjuhljfkgmjlwcs"),
            "password":        st.secrets["SUPABASE_PASSWORD"],
            "sslmode":         "require",
            "connect_timeout": 10,
        }
    except Exception:
        # Local: lê do toml
        CONFIG_PATH = Path("folder_gitignore/config_app.toml")
        with open(CONFIG_PATH, "rb") as f:
            config = tomllib.load(f)
        return {
            "host":            config["SUPABASE_HOST"],
            "port":            config.get("SUPABASE_PORT", "6543"),
            "dbname":          config.get("SUPABASE_DBNAME", "postgres"),
            "user":            config.get("SUPABASE_USER", "postgres.qyzfchjuhljfkgmjlwcs"),
            "password":        config["SUPABASE_PASSWORD"],
            "sslmode":         "require",
            "connect_timeout": 10,
        }

DB_CONFIG = get_db_config()

# ─────────────────────────────────────────────
# GERENCIADOR DE CONEXÃO
# ─────────────────────────────────────────────
@contextmanager
def get_connection():
    """Abre e fecha a conexão automaticamente."""
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
        conn.commit()
    except psycopg2.OperationalError as e:
        print(f"[ERRO] Falha na conexão: {e}")
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"[ERRO] Transação revertida: {e}")
        raise
    finally:
        if conn:
            conn.close()



# ─────────────────────────────────────────────
# FUNÇÕES DE LEITURA
# ─────────────────────────────────────────────
def select_all(tabela: str, colunas: list[str] = None) -> list[dict]:
    """Retorna todos os registros de uma tabela como lista de dicionários."""
    cols = ", ".join(colunas) if colunas else "*"
    sql  = f"SELECT {cols} FROM {tabela}"
 
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            colunas_retorno = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
 
    resultado = [dict(zip(colunas_retorno, row)) for row in rows]
    # print(f"[OK] {len(resultado)} registro(s) retornado(s) de '{tabela}'.")
    return resultado

# ─────────────────────────────────────────────
# FUNÇÕES DE INSERT
# ─────────────────────────────────────────────
def insert_one(tabela: str, dados: dict) -> None:
    """Insere ou atualiza um registro baseado em dt_ymd + exercise."""
    def sanitize(val):
        if hasattr(val, 'item'):
            return val.item()
        if pd.isna(val):
            return None
        return val

    dados = {k: sanitize(v) for k, v in dados.items()}

    colunas       = ", ".join(f'"{k}"' for k in dados.keys())
    placeholders  = ", ".join(["%s"] * len(dados))
    updates       = ", ".join(f'"{k}" = EXCLUDED."{k}"' for k in dados.keys() if k not in ("dt_ymd", "exercise"))

    sql = f"""
        INSERT INTO {tabela} ({colunas})
        VALUES ({placeholders})
        ON CONFLICT (dt_ymd, exercise)
        DO UPDATE SET {updates}
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, list(dados.values()))
    print(f"[OK] 1 registro inserido/atualizado em '{tabela}'.")



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

def update_github_json(df):
    try:
        # Configurações
        GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
        OWNER = "xandesantucci"
        REPO = "streamlit_app"
        FILE_PATH = "streamlit_app/gym.json"
        BRANCH = "main"
        # URL do arquivo
        url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILE_PATH}"

        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }

        # 1. Buscar SHA atual do arquivo
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Erro ao localizar arquivo: {response.text}")

        arquivo = response.json()
        sha = arquivo["sha"]

        # Ler conteúdo atual
        conteudo_atual = base64.b64decode(
            arquivo["content"]
        ).decode("utf-8")

        try:
            dados = json.loads(conteudo_atual)

            if isinstance(dados, dict):
                dados = [dados]

        except Exception:
            dados = []

        # Adicionar linhas do dataframe
        for _, linha in df.iterrows():

            registro = linha.to_dict()

            # Converter datas para string
            for k, v in registro.items():

                if pd.isna(v):
                    registro[k] = None

                elif isinstance(
                    v,
                    (
                        pd.Timestamp,
                    )
                ):
                    registro[k] = v.strftime("%Y-%m-%d %H:%M:%S")

                elif hasattr(v, "strftime"):
                    registro[k] = v.strftime("%Y-%m-%d")

            dados.append(registro)

        # 2. Seu novo conteúdo JSON
        # linha = df.iloc[0]

        # novo_json = linha.to_dict()

        conteudo = json.dumps(
            dados,
            ensure_ascii=False,
            indent=4
        )

        conteudo_base64 = base64.b64encode(
            conteudo.encode("utf-8")
        ).decode("utf-8")

        # 3. Atualizar arquivo
        payload = {
            "message": "Atualização automática do JSON",
            "content": conteudo_base64,
            "sha": sha,
            "branch": BRANCH
        }

        response = requests.put(
            url,
            headers=headers,
            json=payload
        )

        print("Status:", response.status_code)
        st.write("Status:", response.status_code)

        print(response.json())

        if response.status_code not in [200, 201]:
            raise Exception(response.text)



        for exercise in df['exercise'].unique():
            st.session_state.saved.append(f'exercise_saved_{exercise}')

        return response.json()

    except Exception as e:
        print("Erro:", str(e))
        st.write("Erro:", str(e))
        return None
    
#####################################################################################
    # try:
    #     with open(file_path, 'w') as f:
    #         json.dump(new_data, f, indent=4)
    #     return True
    # except Exception as e:
    #     print(f"Error updating JSON file: {e}")
    #     return False

# def message_whatsapp(mensagem):
#     kit.sendwhatmsg_instantly("+5521980029229", mensagem)

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