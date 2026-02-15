import streamlit as st
import pandas as pd

# Configuração visual da página
st.set_page_config(page_title="Calculadora MCR 2-6-4", page_icon="🌾", layout="centered")

# --- CONEXÃO COM A SUA PLANILHA GOOGLE ---
# ID da sua planilha fornecido: 1hW-FlQsJA1FPobiFtl7CTjQQvfoYcutTh6mIKDxFMF8
sheet_id = "1hW-FlQsJA1FPobiFtl7CTjQQvfoYcutTh6mIKDxFMF8"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

@st.cache_data(ttl=600) # Atualiza os dados a cada 10 minutos
def carregar_dados():
    try:
        # Lê a planilha e remove espaços extras nos nomes das colunas
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao conectar com a Planilha Google: {e}")
        return None

# Execução do carregamento
df_indicadores = carregar_dados()

# Interface do Usuário
st.title("🌾 Simulador de Elegibilidade - MCR 2-6-4")
st.write("Verifique sua situação de quebra de safra com base nos indicadores do IMEA.")
st.markdown("---")

if df_indicadores is not None:
    # 1. ENTRADA DE DADOS
    st.subheader("1. Localização e Planejamento")
    
    # Lista de cidades direto da sua planilha
    lista_cidades = df_indicadores['Cidade'].unique()
    cidade_ref = st.selectbox("Selecione a Cidade de Referência (IMEA):", lista_cidades)

    # Filtrar dados da cidade selecionada
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

    # 2. CÁLCULOS TÉCNICOS
    # Receita Esperada vs Receita Realizada
    receita_planejada = prod_esperada * preco_contrato
    receita_real = prod_real * preco_atual
    
    # Percentual de Quebra de Receita (Capacidade de Pagamento)
    quebra_receita = (1 - (receita_real / receita_planejada)) * 100
    
    # Desvio em relação à média regional do IMEA (Nexo Causal)
    desvio_regional = (1 - (prod_real / prod_imea)) * 100

    st.markdown("---")
    st.subheader("📊 Diagnóstico de Viabilidade")

    # 3. VEREDITO DE ELEGIBILIDADE (MCR 2-6-4)
    if quebra_receita >= 20:
        st.error(f"🔴 SITUAÇÃO: POTENCIALMENTE ELEGÍVEL")
        st.write(f"**Quebra de Receita:** {quebra_receita:.1f}% abaixo do planejado.")
        st.write(f"**Desvio Regional:** Sua produção está {desvio_regional:.1f}% abaixo da média do IMEA para {cidade_ref}.")
        
        # Botão de Contato Direto
        numero_whats = "5566996626402"
        texto_whats = (f"Olá Dr. Flavio, realizei a simulação para a região de {cidade_ref}. "
                       f"Minha quebra de receita calculada foi de {quebra_receita:.1f}%. "
                       f"Gostaria de uma análise técnica para prorrogação via MCR 2-6-4.")
        
        link_final = f"https://wa.me/{numero_whats
