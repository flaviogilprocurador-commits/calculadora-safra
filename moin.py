import streamlit as st
import pandas as pd

# Configuração visual da página
st.set_page_config(page_title="Calculadora MCR 2-6-4", page_icon="🌾", layout="centered")

# --- CONEXÃO COM A SUA PLANILHA GOOGLE ---
sheet_id = "1hW-FlQsJA1FPobiFtl7CTjQQvfoYcutTh6mIKDxFMF8"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

@st.cache_data(ttl=600)
def carregar_dados():
    try:
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao conectar com a Planilha Google: {e}")
        return None

df_indicadores = carregar_dados()

st.title("🌾 Simulador de Elegibilidade - MCR 2-6-4")
st.write("Verifique sua situação de quebra de safra com base nos indicadores do IMEA.")
st.markdown("---")

if df_indicadores is not None:
    st.subheader("1. Localização e Planejamento")
    
    lista_cidades = df_indicadores['Cidade'].unique()
    cidade_ref = st.selectbox("Selecione a Cidade de Referência (IMEA):", lista_cidades)

    dados_cidade = df_indicadores[df_indicadores['Cidade'] == cidade_ref].iloc[0]
    prod_imea = float(dados_cidade['Produtividade_Media'])
    preco_imea = float(dados_cidade['Preço_Atual'])

    col1, col2 = st.columns(2)
    with col1:
        prod_esperada = st.number_input("Produtividade Planejada no Custeio (sc/ha):", value=60.0)
        prod_real = st.number_input("Quanto você efetivamente colheu (sc/ha):", value=40.0)
    with col2:
        preco_contrato = st.number_input("Preço de Venda Planejado/Trava (R$):", value=125.00)
        preco_atual = st.number_input(f"Preço Atual em {cidade_ref} (R$):", value=preco_imea)

    receita_planejada = prod_esperada * preco_contrato
    receita_real = prod_real * preco_atual
    quebra_receita = (1 - (receita_real / receita_planejada)) * 100
    desvio_regional = (1 - (prod_real / prod_imea)) * 100

    st.markdown("---")
    st.subheader("📊 Diagnóstico de Viabilidade")

    if quebra_receita >= 20:
        st.error(f"🔴 SITUAÇÃO: POTENCIALMENTE ELEGÍVEL")
        st.write(f"**Quebra de Receita:** {quebra_receita:.1f}% abaixo do planejado.")
        st.write(f"**Desvio Regional:** Sua produção está {desvio_regional:.1f}% abaixo da média do IMEA.")
        
        numero_whats = "5566996626402"
        texto_whats = (f"Olá Dr. Flavio, realizei a simulação para {cidade_ref}. "
                       f"Quebra de receita: {quebra_receita:.1f}%. "
                       f"Gostaria de uma análise para prorrogação MCR 2-6-4.")
        
        link_final = f"https://wa.me/{numero_whats}?text={texto_whats.replace(' ', '%20')}"
        
        st.markdown(f'''
            <a href="{link_final}" target="_blank">
                <button style="width:100%; height:60px; background-color:#25D366; color:white; border:none; border-radius:10px; font-weight:bold; font-size:16px; cursor:pointer;">
                    🟢 ENVIAR DIAGNÓSTICO PARA DR. FLAVIO
                </button>
            </a>
        ''', unsafe_allow_html=True)
    else:
        st.success(f"🟢 SITUAÇÃO: REGULAR")
        st.write(f"Quebra de {quebra_receita:.1f}% está dentro da margem.")

st.markdown("---")
st.caption("Fonte: IMEA. Este app é uma ferramenta de triagem técnica.")