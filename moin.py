import streamlit as st

# Configuração da página
st.set_page_config(page_title="Calculadora MCR 2-6-4", page_icon="🌾")

st.title("🌾 Simulador de Elegibilidade - MCR 2-6-4")
st.write("Análise técnica baseada em produtividade e indicadores do IMEA")

# Dados de Referência atualizados (Foco em polos de soja conforme solicitado)
# Preços e médias devem ser conferidos em: https://www.imea.com.br/imea-site/indicador-soja
dados_imea = {
    "Porto dos Gaúchos (Médio-Norte)": {"prod_media": 61.5, "preco_disponivel": 113.80},
    "Campo Novo dos Parecis (Parecis)": {"prod_media": 63.8, "preco_disponivel": 116.40},
    "Sorriso (Médio-Norte)": {"prod_media": 62.3, "preco_disponivel": 114.80},
    "Nova Mutum (Médio-Norte)": {"prod_media": 62.0, "preco_disponivel": 115.00},
    "Sapezal (Parecis)": {"prod_media": 63.5, "preco_disponivel": 116.00},
    "Sinop (Norte)": {"prod_media": 60.5, "preco_disponivel": 113.20},
    "Rondonópolis (Sudeste)": {"prod_media": 61.2, "preco_disponivel": 118.50}
}

st.subheader("1. Localização e Planejamento")
cidade_ref = st.selectbox("Selecione a Cidade de Referência (IMEA):", list(dados_imea.keys()))

col1, col2 = st.columns(2)
with col1:
    prod_esperada = st.number_input("Produtividade Esperada no Custeio (sc/ha):", value=60.0)
    prod_real = st.number_input("Produtividade Efetiva Colhida (sc/ha):", value=40.0)
with col2:
    preco_contrato = st.number_input("Preço de Trava/Custeio (R$):", value=125.00)
    preco_atual = st.number_input("Preço Atual de Mercado (R$):", value=dados_imea[cidade_ref]['preco_disponivel'])

# Lógica de Cálculo
receita_planejada = prod_esperada * preco_contrato
receita_real = prod_real * preco_atual
quebra_receita = (1 - (receita_real / receita_planejada)) * 100
desvio_regional = (1 - (prod_real / dados_imea[cidade_ref]['prod_media'])) * 100

st.markdown("---")

# Diagnóstico de Elegibilidade
if quebra_receita >= 20:
    st.error(f"🚨 ELEGÍVEL PARA REQUERIMENTO")
    st.write(f"Sua receita bruta apresenta uma quebra de **{quebra_receita:.1f}%** em relação ao planejado.")
    st.write(f"Sua produtividade está **{desvio_regional:.1f}%** abaixo da média regional do IMEA.")
    
    # Link do WhatsApp - Dr. Flavio Lemos Gil
    numero_whats = "5566996626402"
    mensagem = f"Olá Dr. Flavio, fiz a simulação da soja para {cidade_ref}. Minha quebra de receita foi de {quebra_receita:.1f}% e gostaria de analisar a prorrogação pelo MCR 2-6-4."
    link_final = f"https://wa.me/{numero_whats}?text={mensagem.replace(' ', '%20')}"
    
    st.markdown(f'''
        <a href="{link_final}" target="_blank">
            <button style="width:100%; height:60px; background-color:#25D366; color:white; border:none; border-radius:10px; font-weight:bold; font-size:16px; cursor:pointer;">
                🟢 ENVIAR DIAGNÓSTICO PARA DR. FLAVIO
            </button>
        </a>
    ''', unsafe_allow_html=True)
else:
    st.success(f"✅ SITUAÇÃO REGULAR")
    st.write(f"A quebra de receita de {quebra_receita:.1f}% está dentro da margem operacional para prorrogação.")

st.markdown("---")
st.info(f"Fonte de Dados: [IMEA - Indicador Soja](https://www.imea.com.br/imea-site/indicador-soja)")
st.caption("Este simulador é uma ferramenta de apoio técnico e não substitui o laudo agronômico obrigatório.")
