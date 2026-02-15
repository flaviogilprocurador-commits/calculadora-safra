import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Calculadora MCR 2-6-4", page_icon="🌾")

# --- CONEXÃO COM A PLANILHA ---
# Substitua o ID abaixo pelo ID da sua planilha (está no link entre /d/ e /edit)
sheet_id = "COLOQUE_AQUI_O_ID_DA_SUA_PLANILHA"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

@st.cache_data(ttl=3600) # Atualiza os dados a cada 1 hora
def carregar_dados():
    return pd.read_csv(sheet_url)

try:
    df = carregar_dados()
    # Transforma a planilha em um dicionário para o código usar
    dados_imea = df.set_index('Cidade').to_dict('index')
except:
    st.error("Erro ao carregar dados da planilha. Verifique o link e as colunas.")
    st.stop()
# ------------------------------

st.title("🌾 Simulador de Elegibilidade - MCR 2-6-4")
st.write("Análise baseada em dados reais e indicadores regionais.")

st.subheader("1. Localização e Planejamento")
cidade_ref = st.selectbox("Selecione a Cidade de Referência:", list(dados_imea.keys()))

col1, col2 = st.columns(2)
with col1:
    prod_esperada = st.number_input("Produtividade Esperada (sc/ha):", value=60.0)
    prod_real = st.number_input("Produtividade Colhida (sc/ha):", value=40.0)
with col2:
    preco_contrato = st.number_input("Preço Planejado (R$):", value=125.00)
    # Puxa o preço direto da sua Planilha Google
    valor_saca_planilha = float(dados_imea[cidade_ref]['Preço_Atual'])
    preco_atual = st.number_input("Preço Atual IMEA (R$):", value=valor_saca_planilha)

# Lógica de Cálculo
receita_planejada = prod_esperada * preco_contrato
receita_real = prod_real * preco_atual
quebra = (1 - (receita_real / receita_planejada)) * 100

st.markdown("---")

if quebra >= 20:
    st.error(f"🚨 ELEGÍVEL: Quebra de Receita de {quebra:.1f}%")
    numero_whats = "5566996626402"
    mensagem = f"Olá Dr. Flavio, fiz a simulação para {cidade_ref}. Quebra de {quebra:.1f}%."
    link_final = f"https://wa.me/{numero_whats}?text={mensagem.replace(' ', '%20')}"
    
    st.markdown(f'''<a href="{link_final}" target="_blank">
        <button style="width:100%; height:60px; background-color:#25D366; color:white; border:none; border-radius:10px; font-weight:bold; cursor:pointer;">
            🟢 ENVIAR DIAGNÓSTICO PARA DR. FLAVIO
        </button></a>''', unsafe_allow_html=True)
else:
    st.success(f"✅ SITUAÇÃO REGULAR: Quebra de {quebra:.1f}%")

st.info("Os dados acima são sincronizados com a planilha de indicadores oficiais.")
