import streamlit as st

st.set_page_config(page_title="Calculadora MCR 2-6-4", page_icon="🌾")

st.title("🌾 Simulador de Elegibilidade - MCR 2-6-4")
st.write("Focado em produtividade e preço regional (IMEA)")

# Dados de Referência (Juína e Médio-Norte)
dados_imea = {
    "Noroeste (Juína)": {"prod_media": 58.5, "preco_disponivel": 112.00},
    "Médio-Norte": {"prod_media": 62.3, "preco_disponivel": 114.50},
    "Sudeste": {"prod_media": 61.0, "preco_disponivel": 116.20}
}

# Entrada de Dados
st.subheader("Simulação de Dados")
regiao = st.selectbox("Selecione sua Região (IMEA):", list(dados_imea.keys()))

col1, col2 = st.columns(2)
with col1:
    prod_esperada = st.number_input("Produtividade Esperada (sc/ha):", value=60.0)
    prod_real = st.number_input("Produtividade Colhida (sc/ha):", value=40.0)
with col2:
    preco_contrato = st.number_input("Preço Planejado (R$):", value=125.00)
    preco_atual = st.number_input("Preço Atual IMEA (R$):", value=dados_imea[regiao]['preco_disponivel'])

# Lógica de Cálculo
receita_planejada = prod_esperada * preco_contrato
receita_real = prod_real * preco_atual
quebra = (1 - (receita_real / receita_planejada)) * 100

st.markdown("---")

# Resultado
if quebra >= 20:
    st.error(f"🔴 ELEGÍVEL: Quebra de Receita de {quebra:.1f}%")
    link_whatsapp = f"https://wa.me/5566999999999?text=Oi%20Flavio,%20minha%20calculadora%20deu%20elegivel."
    st.markdown(f"[🟢 CLIQUE AQUI PARA FALAR COM O CONSULTOR]({link_whatsapp})")
else:
    st.success(f"🟢 SITUAÇÃO REGULAR: Quebra de {quebra:.1f}%")