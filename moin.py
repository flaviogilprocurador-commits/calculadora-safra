import streamlit as st

# Configuração da página
st.set_page_config(page_title="Calculadora MCR 2-6-4", page_icon="🌾")

# Título e cabeçalho
st.title("🌾 Simulador de Elegibilidade - MCR 2-6-4")
st.write("Análise técnica de quebra de safra para produtores de Mato Grosso.")
st.markdown("---")

# 1. ENTRADA DE DADOS
st.subheader("1. Localização e Planejamento")

# Lista de cidades solicitada
cidades = [
    "Juína", "Juara", "Brasnorte", "Campo Novo do Parecis", 
    "Porto dos Gaúchos", "Tapurah", "Itanhangá", "Sorriso", 
    "Nova Mutum", "Lucas do Rio Verde", "Sinop", "Matupá", 
    "Alta Floresta", "Tabaporã"
]

cidade_ref = st.selectbox("Selecione a Cidade:", cidades)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Dados Planejados (Custeio)**")
    prod_esperada = st.number_input("Produtividade Esperada (sc/ha):", value=60.0, step=0.1)
    preco_esperado = st.number_input("Preço Esperado/Trava (R$):", value=125.0, step=0.1)

with col2:
    st.markdown("**Dados Atuais (Realidade)**")
    prod_atual = st.number_input("Produtividade Atual (sc/ha):", value=40.0, step=0.1)
    preco_atual = st.number_input("Preço Atual de Mercado (R$):", value=110.0, step=0.1)

# 2. CÁLCULO DA CAPACIDADE DE PAGAMENTO (RECEITA)
receita_planejada = prod_esperada * preco_esperado
receita_atual = prod_atual * preco_atual

# Cálculo da Quebra de Receita
if receita_planejada > 0:
    quebra_receita = (1 - (receita_atual / receita_planejada)) * 100
else:
    quebra_receita = 0

st.markdown("---")
st.subheader("📊 Resultado da Simulação")

# 3. VEREDITO TÉCNICO
if quebra_receita >= 20:
    st.error(f"🚨 POTENCIALMENTE ELEGÍVEL")
    st.write(f"Identificamos uma quebra de receita de **{quebra_receita:.1f}%** em {cidade_ref}.")
    st.write("Sua capacidade de pagamento está abaixo do limite crítico estipulado pelo Manual de Crédito Rural.")
    
    # Configuração do WhatsApp do Dr. Flavio Lemos Gil
    numero_whats = "5566996626402"
    mensagem = (f"Olá Dr. Flavio, realizei a simulação para {cidade_ref}. "
                f"Minha quebra de receita calculada foi de {quebra_receita:.1f}%. "
                f"Gostaria de uma análise para prorrogação via MCR 2-6-4.")
    
    link_final = f"https://wa.me/{numero_whats}?text={mensagem.replace(' ', '%20')}"
    
    st.markdown(f'''
        <a href="{link_final}" target="_blank">
            <button style="width:100%; height:60px; background-color:#25D366; color:white; border:none; border-radius:10px; font-weight:bold; font-size:16px; cursor:pointer;">
                🟢 ENVIAR PARA ANÁLISE JURÍDICA AGORA
            </button>
        </a>
    ''', unsafe_allow_html=True)
else:
    st.success(f"✅ SITUAÇÃO DENTRO DA MARGEM")
    st.write(f"A quebra de receita de {quebra_receita:.1f}% não atinge os requisitos para o enquadramento no MCR 2-6-4.")

st.markdown("---")
st.caption("Este aplicativo é uma ferramenta de triagem técnica de autoria do Dr. Flavio Lemos Gil.")
